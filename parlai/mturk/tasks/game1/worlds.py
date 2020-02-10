#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
import threading

class WriterOnboardingWorld(MTurkOnboardWorld):
    """Example onboarding world. Sends a message from the world to the
    worker and then exits as complete after the worker uses the interface
    """

    def parley(self):
        ad = {}
        ad['id'] = 'System'
        # TODO: rewrite the text below
        ad['text'] = (
            "Welcome onboard! You'll be playing the role of the writer. "
            "You'll be given a prompt and your task is to write three claims "
            "in relation with this prompt."
        )
        self.mturk_agent.observe(ad)
        # self.mturk_agent.act()
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
        # self.mturk_agent.act()
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
        # import pdb; pdb.set_trace()
        self.writers = [self.writer_0, self.writer_1]
        self.evaluators = [self.evaluator_0, self.evaluator_1]
        self.episodeDone = False
        self.turns = 0
        
        self.prompt = None
        self.hypotheses_0 = None
        self.hypotheses_1 = None
        self.eval_0_ent = None
        self.eval_1_ent = None
        self.eval_0_cont = None
        self.eval_1_cont = None
        self.eval_0_neut = None
        self.eval_1_neut = None

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
                    print(len(self.writers_copy))
                    print(self.hypotheses)

                    if len(self.writers_copy) == 0:
                        self.turns +=1

        if self.turns == 2:
            if self.hypotheses[0]['id'] == "Writer0":
                self.hypotheses_0 = self.hypotheses[0]
                self.hypotheses_1 = self.hypotheses[1]
            else:
                self.hypotheses_0 = self.hypotheses[1]
                self.hypotheses_1 = self.hypotheses[0]

            self.writer0_entail = {'id':'Claim 1', 'text': self.hypotheses_0['text']}
            self.writer0_contradict = {'id':'Claim 1','text': self.hypotheses_0['task_data']}
            self.writer0_neutral = {'id':'Claim 1','text': self.hypotheses_0['task_data2']}

            self.writer1_entail = {'id':'Claim 2','text':  self.hypotheses_1['text']}
            self.writer1_contradict = {'id':'Claim 2','text':  self.hypotheses_1['task_data']}
            self.writer1_neutral = {'id':'Claim 2','text': self.hypotheses_1['task_data2']}


            for evaluator in self.evaluators:
                evaluator.observe({'id':'Label', 'text':'Definitely correct'})
                evaluator.observe(self.writer0_entail)
                evaluator.observe(self.writer1_entail)
            self.turns += 1

        if self.turns == 3:
            semi_turn = 0
            if semi_turn == 0:
                for evaluator in self.evaluators_copy:
                    evaluation = evaluator.act(blocking=False, ranker=True)
                    if evaluation is not None:
                        self.ents.append(evaluation)
                        self.evaluators_copy.remove(evaluator)
                        print(len(self.evaluators_copy))
                        print(self.ents)

                        if len(self.evaluators_copy) == 0:
                            if self.ents[0]['text'] == self.ents[1]['text']:
                                for evaluator in self.evaluators:
                                    evaluator.observe({'id':'Agreement', 'text':'You agreed! Bonus'})
                            self.evaluator_0.observe(self.writer0_contradict)
                            self.evaluator_1.observe(self.writer1_contradict)
                            semi_turn += 1
            if semi_turn == 1:
                for evaluator in self.evaluators_copy_c:
                    evaluation = evaluator.act(blocking=False,ranker=True)
                    if evaluation is not None:
                        self.conts.append(evaluation)
                        self.evaluators_copy_c.remove(evaluator)
                        print(len(self.evaluators_copy_c))
                        print(self.conts)

                        if len(self.evaluators_copy_c) == 0:
                            if self.conts[0]['text'] == self.conts[1]['text']:
                                for evaluator in self.evaluators:
                                    evaluator.observe({'id':'Agreement', 'text':'You agreed! Bonus'})
                            self.evaluator_0.observe(self.writer0_neutral)
                            self.evaluator_1.observe(self.writer1_neutral)
                            semi_turn += 1
            if semi_turn == 2:
                for evaluator in self.evaluators_copy_n:
                    evaluation = evaluator.act(blocking=False)
                    if evaluation is not None:
                        self.neuts.append(evaluation)
                        self.evaluators_copy_n.remove(evaluator)
                        print(len(self.evaluators_copy_n))
                        print(self.neuts)

                        if len(self.evaluators_copy_n) == 0:
                            if self.neuts[0]['text'] == self.neuts[1]['text']:
                                for evaluator in self.evaluators:
                                    evaluator.observe({'id':'Agreement', 'text':'You agreed! Bonus'})
                            self.episodeDone = True

        if self.turns == 4:
            for evaluator in self.evaluators:
                evaluator.observe({'id':'Label', 'text':'Definitely correct'})
                evaluator.observe(self.writer0_contradict)
                evaluator.observe(self.writer1_contradict)
            self.turns += 1

        if self.turns == 5:
            for evaluator in self.evaluators_copy_c:
                evaluation = evaluator.act(blocking=False)
                if evaluation is not None:
                    self.conts.append(evaluation)
                    self.evaluators_copy_c.remove(evaluator)
                    print(len(self.evaluators_copy_c))
                    print(self.conts)

                    if len(self.evaluators_copy_c) == 0:
                        if self.conts[0]['text'] == self.conts[1]['text']:
                            for evaluator in self.evaluators:
                                evaluator.observe({'id':'Agreement', 'text':'You agreed! Bonus'})
                        self.turns +=1

        if self.turns == 6:
            for evaluator in self.evaluators:
                evaluator.observe({'id':'Label', 'text':'Definitely correct'})
                evaluator.observe(self.writer0_neutral)
                evaluator.observe(self.writer1_neutral)
            self.turns += 1

        if self.turns == 7:
            for evaluator in self.evaluators_copy_n:
                evaluation = evaluator.act(blocking=False)
                if evaluation is not None:
                    self.neuts.append(evaluation)
                    self.evaluators_copy_n.remove(evaluator)
                    print(len(self.evaluators_copy_n))
                    print(self.neuts)

                    if len(self.evaluators_copy_n) == 0:
                        if self.neuts[0]['text'] == self.neuts[1]['text']:
                            for evaluator in self.evaluators:
                                evaluator.observe({'id':'Agreement', 'text':'You agreed! Bonus'})
                        self.episodeDone = True


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
            'writer-1': self.hypothesis_1,
            # TODO: add evaluations here
        }
