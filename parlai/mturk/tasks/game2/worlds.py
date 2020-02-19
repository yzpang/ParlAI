#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
import threading
import random
import copy
import time
import itertools

class OnboardingWorld(MTurkOnboardWorld):
    """Example onboarding world. Sends a message from the world to the
    worker and then exits as complete after the worker uses the interface
    """

    def parley(self):
        ad = {}
        ad['id'] = 'System'
        ad['text'] = (
            "Welcome onboard! You've been paired with another person. "
            "You'll both be writing claims for one prompt "
            "and evaluating for another prompt."
        )
        self.mturk_agent.observe(ad)
        self.episodeDone = True

class WriterOnboardingWorld(MTurkOnboardWorld):
    """Example onboarding world. Sends a message from the world to the
    worker and then exits as complete after the worker uses the interface
    """

    def parley(self):
        ad = {}
        ad['id'] = 'System'
        ad['text'] = (
            "Welcome onboard! You'll be playing the role of the writer. "
            "You'll be given a prompt and your task is to write three claims "
            "in relation with this prompt."
        )
        self.mturk_agent.observe(ad)
        self.episodeDone = True


class EvaluatorOnboardingWorld(MTurkOnboardWorld):
    """Example onboarding world. Sends a message from the world to the
    worker and then exits as complete after the worker uses the interface
    """

    def parley(self):
        ad = {}
        ad['id'] = 'System'
        ad['text'] = (
            "Welcome onboard! You'll be playing the evaluator. You'll "
            "be shown a prompt, a label, and a set of possible claims. Your task is to  "
            "rank the claims based on creativity, complexity, and relevance."
        )
        self.mturk_agent.observe(ad)
        self.episodeDone = True


class MultiRoleAgentWorld(MTurkTaskWorld):
    """
    World to demonstrate workers with assymetric roles. This task amounts
    to three rounds and then an evaluation step. It is purposefully created
    as a task to demo multiple views and has no other purpose.
    """

    collector_agent_id = 'Moderator'

    def __init__(self, opt, task, mturk_agents):
        self.task = task
        self.mturk_agents = mturk_agents
        self.num_agents = len(mturk_agents)
        # We require even number of agents for this game
        assert self.num_agents % 2 == 0, "We have "+str(self.num_agents)+" agents. Need an even number of agents for this game."

        self.agents = [None for i in range(len(mturk_agents))]
        for agent in mturk_agents:
            num = int(agent.demo_role[-1]) # number form Person1 etc.
            self.agents[num-1] = agent
                # if agent.demo_role == 'Person1':
                #     # TODO: make number of writers a variable
                #     self.agent_1 = agent
                # elif agent.demo_role == 'Person2':
                #     self.agent_2 = agent
                # elif agent.demo_role == 'Person3':
                #     self.agent_3 = agent
                # else:
                #     self.agent_4 = agent
        self.sets = {} # [None for i in range(len(mturk_agents)/2)]
        for i in range(int(self.num_agents/2)):
            self.sets[i] = self.agents[i*2 : (i+1)*2]
        self.episodeDone = False
        self.max_meta_turns = 2
        self.meta_turn = 0
        self.interim_data = []
        self.turns = 0
        
        self.prompt = None # To-do import data
        self.noflip = {'Claim 1':'Claim 1', 'Claim 2':'Claim 2'}
        self.yesflip = {'Claim 1':'Claim 2', 'Claim 2':'Claim 1'}
        self.writer_bonus = 0.3
        self.ranker_bonus = 0.1

    def parley(self):
        if self.meta_turn < self.max_meta_turns:
            if self.turns == 0:
                # Get prompt and limit to one sentence
                self.prompts = []
                for i in range(int(self.num_agents/2)):
                    squad_example = self.task.act()
                    premise = '\n'.join(squad_example['text'].split('\n')[:-1])
                    premise = premise.split(".", 1)[0] + "." # Todo: preprocess sentence segmentation. This is a janky fix
                    prompt = {
                            'id': 'Prompt',
                            'text': premise
                        }
                    self.prompts.append(prompt)

                    # Assign writing prompts to sets of agents
                    for agent in self.sets[i]:
                        agent.observe(prompt)

                # Make copies of objects of workers, we need this to have
                # concurrent work on HITs
                self.writers_copy = self.agents.copy()
                self.evaluators_copy = self.agents.copy()
                # self.evaluators_copy_n = self.agents.copy()
                # self.evaluators_copy_c = self.agents.copy()
                
                # Lists where we will store responses
                self.hypotheses = []
                # Todo: make self.evals into a dict for neater code
                self.ents = []
                self.conts = []
                self.neuts = []
                self.evals =[self.ents, self.conts, self.neuts]

                self.turns += 1

            if self.turns == 1:
                # Hypothesis writing
                for agent in self.writers_copy:
                    hypothesis = agent.act(blocking=False)
                    if hypothesis is not None:
                        self.hypotheses.append(hypothesis)
                        self.writers_copy.remove(agent)

                        if len(self.writers_copy) == 0:
                            self.turns +=1

            if self.turns == 2:
                # Collect all the hypothesis and pass the first set to the rankers

                # Sort out hypotheses: assign hypothesis to correct worker
                self.hypotheses_collect = {}
                for i in range(len(self.hypotheses)):
                    for agent in self.agents:
                        if self.hypotheses[i]['id'] == agent.demo_role:
                            num = int(agent.demo_role[-1])
                            self.hypotheses_collect[num-1] = self.hypotheses[i]

                # Writers observe the other writer's hypotheses
                for i in range(len(self.sets)):
                    showme = [self.hypotheses_collect[(i*2)+1], self.hypotheses_collect[(i*2)]] # 1,3 / 0,2
                    for j in range(2):
                        self.sets[i][j].observe({'id':'Other writer\'s claims', 'text':'\nDef. Correct: ' + showme[j]['text'] + '\nDef. incorrect: ' + showme[j]['task_data'] + '\nNeither: ' + showme[j]['task_data2']}) #1,3
                # Pause to read claims
                time.sleep(10)

                # Sort out hypotheses according to label and writer
                self.entailments, self.contradictions, self.neutrals  = {}, {}, {}
                self.map_entail, self.map_contradict, self.map_neutral = {}, {}, {} # to store flip maps
                for i in range(self.num_agents):
                    self.entailments[i] = {'id':'Claim '+str((i%2)+1), 'text': self.hypotheses_collect[i]['text'], 'task_data': {'respond_with_form': [{
                            'type': 'choices',
                            'question': 'This is filler',
                            'choices': [i for i in range(0, 10)]
                        }]}}
                    self.contradictions[i] = {'id':'Claim '+str((i%2)+1),'text': self.hypotheses_collect[i]['task_data']}
                    self.neutrals[i] = {'id':'Claim '+str((i%2)+1),'text': self.hypotheses_collect[i]['task_data2']}

                # Show agents the prompt from the other set
                # And the claims for that prompt
                for agent in self.agents:
                    agent.observe({'id':'Phase 2', 
                                   'text':'Thank you for writing your claims. Now please read a new prompt and rank claims written by other people,'})
                label = 'Definitely correct'
                # Round robin exchange of prompts and claims for ranking
                setnum = itertools.cycle(range(len(self.sets)))
                next(setnum)
                for i in range(len(self.sets)):
                    num = next(setnum)
                    prompt = self.prompts[num]
                    # for agent in self.sets[i]:
                    #     prompt = self.prompts[num]
                    #     agent.observe(prompt)
                    #     label = 'Definitely correct'
                    #     agent.observe({'id':'Label', 'text':'Definitely correct'})
                    self.map_entail[i] = self.observe_hypotheses(prompt, label, self.sets[i], self.entailments[num*2], self.entailments[(num*2)+1])
                            
                self.turns += 1

            if self.turns in range(3,6):
                # Ranking entailments
                for agent in self.evaluators_copy:
                    evaluation = agent.act(blocking=False)
                    if evaluation is not None:
                        self.evals[self.turns-3].append(evaluation)
                        self.evaluators_copy.remove(agent)

                        if len(self.evaluators_copy) == 0:
                            # Show contradictions
                            if self.turns == 3:
                                label = 'Definitely incorrect'
                            elif label == 4:
                                label = 'Neither definitely correct nor definitely incorrect'
                            else:
                                pass
                            # for agent in self.agents:
                            #     agent.observe({'id':'Label', 'text':'Definitely incorrect'})
                            if self.turns < 5:
                                setnum = itertools.cycle(range(len(self.sets)))
                                next(setnum)
                                for i in range(len(self.sets)):
                                    num = next(setnum)
                                    prompt = self.prompts[num]
                                    # for agent in self.sets[i]:
                                    #     agent.observe(self.prompts[num])
                                    self.map_contradict[i] = self.observe_hypotheses(prompt, label, self.sets[i], self.contradictions[num*2], self.contradictions[(num*2)+1])
                                # Make another copy of evaluators
                                self.evaluators_copy = self.agents.copy()
                            self.turns +=1

            """
            if self.turns == 3:
                # Rankers rank all 3 sets of hypotheses
                semi_turn = 0
                if semi_turn == 0:
                    for evaluator in self.evaluators_copy:
                        evaluation_e = evaluator.act(blocking=False)
                        if evaluation_e is not None:
                            self.ents.append(evaluation_e)
                            self.evaluators_copy.remove(evaluator)

                            if len(self.evaluators_copy) == 0:
                                for agent in self.set1:
                                    agent.observe(self.prompt)
                                    agent.observe({'id':'Label', 'text':'Definitely incorrect'})
                                self.map_contradict = self.observe_hypotheses(self.writer0_contradict, self.writer1_contradict)
                                semi_turn += 1
                
                if semi_turn == 1:
                    # The (nested) while loops below are a hack
                    # The system stops querying the HIT for messages without these loops
                    # To-do: investigate root cause and fix

                    evaluation0_c, evaluation1_c = None, None
                    # Continuously query both rankers
                    while evaluation0_c is None and evaluation1_c is None:
                        evaluation0_c = self.evaluators_copy_c[0].act(blocking=False)
                        evaluation1_c = self.evaluators_copy_c[1].act(blocking=False)
                    # Query remaining ranker
                    if evaluation0_c or evaluation1_c is not None:
                        while evaluation0_c is None:
                            evaluation0_c = self.evaluators_copy_c[0].act(blocking=False)
                        while evaluation1_c is None:
                            evaluation1_c = self.evaluators_copy_c[1].act(blocking=False)
                        if evaluation0_c is not None and evaluation1_c is not None:
                            self.conts.append(evaluation0_c)
                            self.conts.append(evaluation1_c)
                            self.evaluators_copy_c = []
                            for evaluator in self.evaluators:
                                evaluator.observe(self.prompt)
                                evaluator.observe({'id':'Label', 'text':'Neither definitely correct nor definitely incorrect'})
                            self.map_neutral = self.observe_hypotheses(self.writer0_neutral, self.writer1_neutral)
                            semi_turn += 1
                
                if semi_turn == 2:
                    # The (nested) while loops below are a hack
                    # The system stops querying the HIT for messages without these loops
                    # To-do: investigate root cause and fix

                    evaluation0_n, evaluation1_n = None, None
                    # Continuously query both rankers
                    while evaluation0_n is None and evaluation1_n is None:
                        evaluation0_n = self.evaluators_copy_n[0].act(blocking=False)
                        evaluation1_n = self.evaluators_copy_n[1].act(blocking=False)
                    # Query remaining ranker
                    if evaluation0_n or evaluation1_n is not None:
                        while evaluation0_n is None:
                            evaluation0_n = self.evaluators_copy_n[0].act(blocking=False)
                        while evaluation1_n is None:
                            evaluation1_n = self.evaluators_copy_n[1].act(blocking=False)
                        if evaluation0_n is not None and evaluation1_n is not None:
                            self.neuts.append(evaluation0_n)
                            self.neuts.append(evaluation1_n)
                            self.evaluators_copy_n = []
                            self.turns += 1
            """

            if self.turns == 6:
                # Give feedback to rankers and writers
                # Currently not checking for validaton agreement

                label_types = ['Definitely Correct', 'Definitely Incorrect', 'Neither']
                maps = [self.map_entail, self.map_contradict, self.map_neutral]
                eval0_justifications = []
                eval1_justifications = []
                import pdb; pdb.set_trace()
                for i, rankings in enumerate([self.ents, self.conts, self.neuts]):
                    label = label_types[i]
                    writer_bonus_message = {'id': 'Bonus for ' + label, 'text': 'You ranked 1st! Bonus = $' + str(self.writer_bonus) +'.'}
                    writer_nobonus_message = {'id':'Bonus', 'text':'Unfortunately you ranked 2nd on all 3 claims.'}
                    agrm_bonus_message = {'id': 'Bonus for ' + label, 'text': 'You agreed with the other evaluators! Bonus = $' + str(self.ranker_bonus) + '.'}
                    noagrm_bonus_message = {'id': 'Bonus for ' + label, 'text': 'The evaluators did not agree. Bonus = $' + str(self.writer_bonus/2) + '.'}

                    # Map the selected choices to "unflip" the ordering
                    # and collect ranker justifications
                    if rankings[1]['id'] == "Evaluator1":
                        rankings[1]['text'] = maps[i][rankings[1]['text']]
                        # justifications
                        if rankings[0]['task_data'] is not '':
                            eval0_justifications.append(label + ': ' + rankings[0]['task_data'])
                        if rankings[1]['task_data'] is not '':
                            eval1_justifications.append(label + ': ' + rankings[1]['task_data'])
                    else:
                        rankings[0]['text'] = maps[i][rankings[0]['text']]
                        # justifications
                        if rankings[0]['task_data'] is not '':
                            eval1_justifications.append(label + ': ' + rankings[0]['task_data'])
                        if rankings[1]['task_data'] is not '':
                            eval0_justifications.append(label + ': ' + rankings[1]['task_data'])

                    # Show messages about bonuses
                    w0_rank = 0
                    w1_rank = 0
                    if rankings[0]['text'] == rankings[1]['text']:
                        for evaluator in self.evaluators:
                            evaluator.observe(agrm_bonus_message)
                        if rankings[0]['text'] == 'Claim 1':
                            self.writer_0.observe(writer_bonus_message)
                            w0_rank += 1
                        else:
                            self.writer_1.observe(writer_bonus_message)
                            w1_rank += 1
                    else:
                        # Rankers did not agree
                        for writer in self.writers:
                            writer.observe(noagrm_bonus_message)
                            w0_rank += 1
                            w1_rank +=1
                        pass
                    if w0_rank == 0:
                        self.writer_0.observe(writer_nobonus_message)
                    elif w1_rank == 0:
                        self.writer_1.observe(writer_nobonus_message)


                self.interim_data.append(self.get_intermediate_task_data())

                # Show rankers partner's justifications
                # and show writer's both sets of justifications 
                if len(eval1_justifications) != 0:
                    self.evaluator_1.observe({'id':'Justifications from other evaluator', 'text': "\n"+"\n".join(eval0_justifications)})
                    for writer in self.writers:
                        writer.observe({'id':'Evaluator 1\'s explanations', 'text': "\n"+"\n".join(eval0_justifications)})
                if len(eval0_justifications) != 0:
                    self.evaluator_0.observe({'id':'Justifications from other evaluator', 'text': "\n"+"\n".join(eval1_justifications)})
                    for writer in self.writers:
                        writer.observe({'id':'Evaluator 2\'s explanations', 'text': "\n"+"\n".join(eval1_justifications)})


                # Pause before showing next prompt
                if (len(eval0_justifications) + len(eval1_justifications)) != 0:
                    time.sleep(4)
                time.sleep(3)
                self.meta_turn += 1
                self.turns = 0
                # import pdb; pdb.set_trace()

                # # Organize data for ease
                # label_types = ['entailment', 'contradiction', 'neutral']
                # for i in enumerate(2):
                #     self.ents[i]['type'] = label_types[0]
                #     self.conts[i]['type'] = label_types[1]
                #     self.neuts[i]['type'] = label_types[2]
                # tmp = pd.DataFrame(self.ents + self.conts + self.neuts)
                # self.rankings = tmp.to_dict() # so we don't require pickling

                # # Give feedback to writers
                # for label in label_types:
                #     rank_writer0, rank_writer1 = 0, 0
                #     rank = tmp.loc[tmp['type'] == label]['text']
                #     rank_writer0 += len(rank.loc[rank == 'Claim 1'])
                #     rank_writer1 += len(rank.loc[rank == 'Claim 2'])
                #     if rank_writer0 == 2:
                #         self.writer_0.observe({'id':'Def. correct rank:', 'text': 'You got the higher rank! Your bonus is $'+str(0.5)+'.'})
                #     elif rank_writer1 == 2:
                #         self.writer_1.observe(sameeee)
                #     else:
                #         # both writers observe no clear ranking?
                #         pass

        else:
            self.episodeDone = True

    def observe_hypotheses(self, prompt, label, agents, hyp0, hyp1):
        """
        Flip a coin and switch order of claims if flip=1
        Agents observe relevant prompt, label, and hypotheses
        Returns the mapping of flip
        
        To-do: cleanup code
        """
        flip = random.randint(0,1)
        if flip == 0:
            mappy = self.noflip
            for agent in agents:
                # agent.observe(hyp0)
                # agent.observe(hyp1)
                if hyp0['task_data']:
                    agent.observe({'id':'Prompt', 'text': prompt['text'] + 
                                                '\nLabel: '+ label +
                                                '\n'+hyp0['id']+': '+hyp0['text'] + 
                                                '\n'+hyp1['id']+': '+hyp1['text'],
                                                'task_data': hyp0['task_data']})
                else:
                    agent.observe({'id':'Prompt', 'text':prompt['text'] + 
                                                '\nLabel: '+ label +
                                                '\n'+hyp0['id']+': '+hyp0['text'] + 
                                                '\n'+hyp1['id']+': '+hyp1['text']})
        else:
            mappy = self.yesflip
            flip0 = copy.deepcopy(hyp0)
            flip1 = copy.deepcopy(hyp1)
            flip0['id'] = 'Claim 2'
            flip1['id'] = 'Claim 1'

            if hyp0['task_data']:
                agents[0].observe({'id':'Prompt', 'text': prompt['text'] + 
                                            '\nLabel: '+ label +
                                            '\n'+hyp0['id']+': '+hyp0['text'] + 
                                            '\n'+hyp1['id']+': '+hyp1['text'],
                                            'task_data': hyp0['task_data']})
            else:
                agents[0].observe({'id':'Prompt', 'text':prompt['text'] + 
                                            '\nLabel: '+ label +
                                            '\n'+hyp0['id']+': '+hyp0['text'] + 
                                            '\n'+hyp1['id']+': '+hyp1['text']})

            if flip0['task_data']:
                agents[1].observe({'id':'Prompt', 'text': prompt['text'] + 
                                            '\nLabel: '+ label +
                                            '\n'+flip1['id']+': '+ flip1['text'] + 
                                            '\n'+flip0['id']+': '+ flip0['text'],
                                            'task_data': flip0['task_data']})
            else:
                agents[1].observe({'id':'Prompt', 'text': prompt['text'] + 
                                            '\nLabel: '+ label +
                                            '\n'+flip1['id']+': '+ flip1['text'] + 
                                            '\n'+flip0['id']+': '+ flip0['text']})
            # for agent in agents:
            #     agent.observe(prompt)
            #     agent.observe({'id':'Label', 'text':label})
            # agents[0].observe(writer0_hyp)
            # agents[0].observe(writer1_hyp)
            # agents[1].observe(flip1)
            # agents[1].observe(flip0)
        return mappy

    def get_intermediate_task_data(self):
        # brings important data together for the task, to later be used for
        # creating the dataset. If data requires pickling, put it in a field
        # called 'needs-pickle'.
        return {
            'sub-hit': self.meta_turn,
            'premise': self.prompt['text'],
            'writer-0': self.hypotheses_0,
            'writer-1': self.hypotheses_1,
            'rank-e': self.ents,
            'rank-c': self.conts,
            'rank-n': self.neuts,
        }

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        # Parallel shutdown of agents
        def shutdown_agent(agent):
            try:
                agent.shutdown(timeout=None)
            except Exception:
                agent.shutdown()  # not MTurkAgent

        threads = []
        for agent in self.mturk_agents:
            t = threading.Thread(target=shutdown_agent, args=(agent,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def review_work(self):
        # Can review the work here to accept or reject it
        pass

    def get_custom_task_data(self):
        # brings important data together for the task, to later be used for
        # creating the dataset. If data requires pickling, put it in a field
        # called 'needs-pickle'.
        return {
            'hit-data': self.interim_data,
        }
