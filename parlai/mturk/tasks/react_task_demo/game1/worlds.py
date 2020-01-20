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
        self.mturk_agent.act()
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
        self.mturk_agent.act()
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
            if agent.demo_role == 'Writer-0':
                # TODO: make number of writers a variable
                self.writer_0 = agent
            elif agent.demo_role == 'Writer-1':
                self.writers_1 = agent
            elif agent.demo_role == 'Evaluator-0':
                self.evaluators_0 = agent
            else:  # 'Evaluator'
                self.evaluator_1 = agent
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
        prompt = {
                'id': 'System',
                'text': "Prompt: " + "This is a placeholder prompt"
            }

        if self.turns == 0:
            # NLI writing
            # entail = {
            #     'id': 'System',
            #     'text': "Please write a claim that is definitely true given the prompt."
            # }
            # contradict = {
            #     'id': 'System',
            #     'text': "Please write a claim that is definitely false given the prompt."
            # }
            # neutral = {
            #     'id': 'System',
            #     'text': "Please write a claim that is neither definitely true nor definitely false given the prompt."
            # }

            # TODO: fix below to be better code. all in single for loop.
            for writer in self.writers:
                writer.observe(prompt) 
                writer.observe(entail)

            # self.entail_0 = self.writer_0.act()
            # self.entail_1 = self.writer_1.act()

            # for writer in self.writers:
            #     writer.observe(contradict)
            # self.contradict_0 = self.writer_0.act()
            # self.contradict_1 = self.writer_1.act()

            # for writer in self.writers:
            #     writer.observe(neutral)
            # self.neutral_0 = self.writer_0.act()
            # self.neutral_1 = self.writer_1.act()

            self.hypotheses_0 = self.writer_0.act()
            self.hypotheses_1 = self.writer_0.act()

            self.turns += 1

        if self.turns == 1:
            ad = {'id': 'System', 'text': 'Testing printing claims'}
            self.writer_0.observe(self.hypothesis_1)
            print(self.hypothesis_1)
            import pdb; pdb.set_trace()
            self.episodeDone = True

        """
        if self.turns == 1:
            ad = {'id': 'System', 'text': "Given the prompt and label, please decide if the claim is appropriate, mark it as Invalid if the claim doesn't fit the label or is completely unrelated to the prompt. Then rank the claims."}
            label = {'id': 'System', 'text': "Label: Definitely correct"}

            ent01 = {'id': 'System', 'text': "Claim 1: " + self.entail_0 + "\n Claim 2: " + self.entail_1}
            ent10 = {'id': 'System', 'text': "Claim 1: " + self.entail_1 + "\n Claim 2: " + self.entail_0}

            # rankthem = {'id': 'System', 'text': "Now, given the prompt and label, please rank the claims based on creativity, complexity, and relevance. Optionally, add an explanation of your ranking to help other evaluators understand your reasoning."}

            # Provide feedback to evaluators
            self.agreed = None
            if self.agreed = 1:
                feedback = {'id': 'System', 'text': "You agreed with the other evaluator on the ranking for the Definitely Correct examples. Bonus = $0.5"}
            else:
                feedback = {'id': 'System', 'text': "You disagreed with the other evaluator on the ranking for the Definitely Correct examples."}

            for evaluator in self.evaluators:
                evaluator.observe(ad)
                evaluator.observe(prompt)
                evaluator.observe(label)
                # TODO: break this up. evluate one hypothesis at a time.
            #  self.evaluators = [self.evaluator_0, self.evaluator_1]
                coin = random.randint(0, 1)
                if coin == 0:
                    evaluator.observe(ent01)
                else:
                    evaluator.observe(ent10)

            # self.ent_acc_0 = self.evaluator_0.act()
            # self.ent_acc_1 = self.evaluator_1.act()
            # for evaluator in self.evaluators:
            #     evaluator.observe(rankthem)
            # self.ent_rate_0 = self.evaluator_0.act()
            # self.ent_rate_1 = self.evaluator_1.act()

            self.eval_0_ent = self.evaluator_0.act()
            self.eval_1_ent = self.evaluator_1.act()

            self.turns += 1


        if self.turns == 2:
            label = {'id': 'System', 'text': "Label: Definitely incorrect"}

            cont01 = {'id': 'System', 'text': "Claim 1: " + self.contradict_0 + "\n Claim 2: " + self.contradict_1}
            cont10 = {'id': 'System', 'text': "Claim 1: " + self.contradict_1 + "\n Claim 2: " + self.contradict_0}

            # Provide feedback to evaluators
            self.agreed = None
            if self.agreed = 1:
                feedback = {'id': 'System', 'text': "You agreed with the other evaluator on the ranking for the Definitely Correct examples. Bonus = $0.5"}
            else:
                feedback = {'id': 'System', 'text': "You disagreed with the other evaluator on the ranking for the Definitely Correct examples."}

            # rankthem = {'id': 'System', 'text': "Now, given the prompt and label, please rank the claims based on creativity, complexity, and relevance. Optionally, add an explanation of your ranking to help other evaluators understand your reasoning."}

            for evaluator in self.evaluators:
                evaluator.observe(prompt)
                evaluator.observe(label)
                coin = random.randint(0, 1)
                if coin == 0:
                    evaluator.observe(cont01)
                else:
                    evaluator.observe(cont10)

            self.eval_0_cont = self.evaluator_0.act()
            self.eval_1_cont = self.evaluator_1.act()

            # TODO: get the relevant actions here. Need agreement and reasoning if not None.
            # if self.ent_rate_0 == self.ent_rate_1:
            #     self.agreed = 1
            # else:
            #     self.agreed = 0
            # for evaluator in self.evaluators:
            #     evaluator.observe(feedback)

            self.turns += 1

        if self.turns == 3:
            label = {'id': 'System', 'text': "Label: Neither definitely correct nor definitely incorrect"}

            neu01 = {'id': 'System', 'text': "Claim 1: " + self.neutral_0 + "\n Claim 2: " + self.neutral_1}
            neut10 = {'id': 'System', 'text': "Claim 1: " + self.neutral_1 + "\n Claim 2: " + self.neutral_0}

            # Provide feedback to evaluators
            self.agreed = None
            if self.agreed = 1:
                feedback = {'id': 'System', 'text': "You agreed with the other evaluator on the ranking for the Definitely Correct examples. Bonus = $0.5"}
            else:
                feedback = {'id': 'System', 'text': "You disagreed with the other evaluator on the ranking for the Definitely Correct examples."}

            # rankthem = {'id': 'System', 'text': "Now, given the prompt and label, please rank the claims based on creativity, complexity, and relevance. Optionally, add an explanation of your ranking to help other evaluators understand your reasoning."}

            for evaluator in self.evaluators:
                evaluator.observe(prompt)
                evaluator.observe(label)
                coin = random.randint(0, 1)
                if coin == 0:
                    evaluator.observe(neut01)
                else:
                    evaluator.observe(neut10)

            self.eval_0_neut = self.evaluator_0.act()
            self.eval_1_neut = self.evaluator_1.act()

            # TODO: get the relevant actions here. Need agreement and reasoning if not None.
            # if self.ent_rate_0 == self.ent_rate_1:
            #     self.agreed = 1
            # else:
            #     self.agreed = 0
            # for evaluator in self.evaluators:
            #     evaluator.observe(feedback)

            self.episodeDone = True
        """

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
