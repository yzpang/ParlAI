#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
import threading
import random
import copy
# import pandas as pd

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

    def __init__(self, opt, mturk_agents):
        self.mturk_agents = mturk_agents
        for agent in mturk_agents:
            if agent.demo_role == 'Writer0':
                # TODO: make number of writers a variable
                self.writer_0 = agent
            elif agent.demo_role == 'Writer1':
                self.writer_1 = agent
            elif agent.demo_role == 'Evaluator0':
                self.evaluator_0 = agent
            else:  # 'Evaluator'
                self.evaluator_1 = agent
        self.writers = [self.writer_0, self.writer_1]
        self.evaluators = [self.evaluator_0, self.evaluator_1]
        self.episodeDone = False
        self.turns = 0
        
        self.prompt = None
        self.hypotheses_0 = None
        self.hypotheses_1 = None

        self.noflip = {'Claim 1':'Claim 1', 'Claim 2':'Claim 2'}
        self.yesflip = {'Claim 1':'Claim 2', 'Claim 2':'Claim 1'}
        self.writer_bonus = 0.3
        self.ranker_bonus = 0.1

    def parley(self):
        if self.turns == 0:
            prompt = {
                    'id': 'Prompt',
                    'text': "Norman architecture typically stands out as a new stage in the architectural history of the regions they subdued. They spread a unique Romanesque idiom to England and Italy, and the encastellation of these regions with keeps in their north French style fundamentally altered the military landscape. Their style was characterised by rounded arches, particularly over windows and doorways, and massive proportions.'}, {'qas': [{'question': 'What architecture type came after Norman in England?"
                }
            for writer in self.writers:
                writer.observe({'id':'Role: ', 'text': 'Writer'})

            for evaluator in self.evaluators:
                evaluator.observe({'id':'Role: ', 'text': 'Ranker'})

            for agent in self.mturk_agents:
                agent.observe(prompt)

            self.writers_copy = self.writers.copy()
            self.evaluators_copy = self.evaluators.copy()
            self.evaluators_copy_n = self.evaluators.copy()
            self.evaluators_copy_c = self.evaluators.copy()
            
            self.hypotheses = []
            self.ents = []
            self.neuts = []
            self.conts = []

            self.turns += 1

        if self.turns == 1:
            # Hypothesis writing
            for writer in self.writers_copy:
                hypothesis = writer.act(blocking=False)
                if hypothesis is not None:
                    self.hypotheses.append(hypothesis)
                    self.writers_copy.remove(writer)

                    if len(self.writers_copy) == 0:
                        self.turns +=1

        if self.turns == 2:
            # Collect all the hypothesis and pass the first set to the rankers

            # Ensure index 0 is for Writer0 and 1 for Writer 1
            if self.hypotheses[0]['id'] == "Writer0":
                self.hypotheses_0 = self.hypotheses[0]
                self.hypotheses_1 = self.hypotheses[1]
            else:
                self.hypotheses_0 = self.hypotheses[1]
                self.hypotheses_1 = self.hypotheses[0]

            # Sort out hypotheses according to label and writer
            self.writer0_entail = {'id':'Claim 1', 'text': self.hypotheses_0['text']}
            self.writer0_contradict = {'id':'Claim 1','text': self.hypotheses_0['task_data']}
            self.writer0_neutral = {'id':'Claim 1','text': self.hypotheses_0['task_data2']}

            self.writer1_entail = {'id':'Claim 2','text':  self.hypotheses_1['text']}
            self.writer1_contradict = {'id':'Claim 2','text':  self.hypotheses_1['task_data']}
            self.writer1_neutral = {'id':'Claim 2','text': self.hypotheses_1['task_data2']}

            # Show evaluators the first set of hypothesis sentences
            for evaluator in self.evaluators:
                evaluator.observe({'id':'Label', 'text':'Definitely correct'})
            self.map_entail = self.observe_hypotheses(self.writer0_entail, self.writer1_entail)
                        
            self.turns += 1

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
                            for evaluator in self.evaluators:
                                evaluator.observe({'id':'Label', 'text':'Definitely incorrect'})
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

        if self.turns == 4:
            # Give feedback to rankers and writers
            # Currently not checking for validaton agreement

            label_types = ['Definitely Correct', 'Definitely Incorrect', 'Neither']
            maps = [self.map_entail, self.map_contradict, self.map_neutral]
            for i, rankings in enumerate([self.ents, self.conts, self.neuts]):
                label = label_types[i]
                writer_bonus_message = {'id': 'Bonus for ' + label, 'text': 'You ranked 1st! Bonus = $' + str(self.writer_bonus) +'.'}
                agrm_message = {'id': 'Bonus for ' + label, 'text': 'You agreed with the other ranker! Bonus = $' + str(self.ranker_bonus) + '.'}

                # Map the selected choices to "unflip" the ordering
                if rankings[1]['id'] == "Evaluator1":
                    rankings[1]['text'] = maps[i][rankings[1]['text']]
                else:
                    rankings[0]['text'] = maps[i][rankings[0]['text']]

                # Show messages about bonuses
                if rankings[0]['text'] == rankings[1]['text']:
                    for evaluator in self.evaluators:
                        evaluator.observe(agrm_message)

                    if rankings[0]['text'] == 'Claim 1':
                        self.writer_0.observe(writer_bonus_message)
                    else:
                        self.writer_1.observe(writer_bonus_message)
                else:
                    # Rankers did not agree
                    pass

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

            self.episodeDone = True

    def observe_hypotheses(self, writer0_hyp, writer1_hyp):
        # Flip a coin and switch order of claims if flip=1
        flip = random.randint(0,1)
        if flip == 0:
            mappy = self.noflip
            for evaluator in self.evaluators:
                evaluator.observe(writer0_hyp)
                evaluator.observe(writer1_hyp)
        else:
            mappy = self.yesflip
            flip0 = copy.deepcopy(writer0_hyp)
            flip1 = copy.deepcopy(writer1_hyp)
            flip0['id'] = 'Claim 2'
            flip1['id'] = 'Claim 1'

            self.evaluator_0.observe(writer0_hyp)
            self.evaluator_0.observe(writer1_hyp)
            self.evaluator_1.observe(flip1)
            self.evaluator_1.observe(flip0)

        return mappy

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
            'premise': self.prompt,
            'writer-0': self.hypotheses_0,
            'writer-1': self.hypotheses_1,
            'rank-e': self.ents,
            'rank-c': self.conts,
            'rank-n': self.neuts,
        }
