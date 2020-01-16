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
            if agent.demo_role == 'Writer':
                # TODO: make number of writers a variable
                self.writer_0 = agent
                self.writer_1 = agent
                self.writers = [self.writer_0, self.writer_1]
            # elif agent.demo_role == 'Ranker':
                # self.ranker = agent
            else:  # 'Evaluator'
                # TODO: make number of evaluators a variable
                self.evaluator_0 = agent
                self.evaluator_1 = agent
                self.evaluators = [self.evaluator_0, self.evaluator_1]
        self.episodeDone = False
        self.turns = 0
        # self.questions = []
        # self.answers = []
        self.prompt = None
        self.entail_0 = None
        self.entail_1 = None
        self.contradict_0 = None
        self.contradict_1 = None
        self.neutral_0 = None
        self.neutral_1 = None

        self.ent_acc_0 = None
        self.ent_acc_1 = None
        self.cont_acc_0 = None
        self.cont_acc_1 = None
        self.neut_acc_0 = None
        self.neut_acc_1 = None

        self.ent_rate_0 = None
        self.ent_rate_1 = None
        self.cont_rate_0 = None
        self.cont_rate_1 = None
        self.neut_rate_0 = None
        self.neut_rate_1 = None

    def parley(self):
        prompt = {
                'id': 'System',
                'text': "Prompt: " + "This is a placeholder prompt"
            }

        if self.turns == 0:
            # NLI writing
            # TODO: make prompt into a variable based on input data

            # prompt = {
            #     'id': 'System',
            #     'text': "Prompt: " + "This is a placeholder prompt"
            # }
            entail = {
                'id': 'System',
                'text': "Please write a claim that is definitely true given the prompt."
            }
            contradict = {
                'id': 'System',
                'text': "Please write a claim that is definitely false given the prompt."
            }
            neutral = {
                'id': 'System',
                'text': "Please write a claim that is neither definitely true nor definitely false given the prompt."
            }

            # TODO: fix below to be better code. all in single for loop.
            for writer in self.writers:
                writer.observe(prompt) 
                writer.observe(entail)
            self.entail_0 = self.writer_0.act()
            self.entail_1 = self.writer_1.act()

            for writer in self.writers:
                writer.observe(contradict)
            self.contradict_0 = self.writer_0.act()
            self.contradict_1 = self.writer_1.act()

            for writer in self.writers:
                writer.observe(neutral)
            self.neutral_0 = self.writer_0.act()
            self.neutral_1 = self.writer_1.act()

            self.turns += 1

        if self.turns == 1:
            ad = {'id': 'System', 'text': "Given the prompt and label, please decide if the claim is appropriate, mark it as Invalid if the claim doesn't fit the label or is completely unrelated to the prompt."}
            # TODO: add additional step for validity testing of each hypothesis/claim?
            for evaluator in self.evaluators:
                evaluator.observe(ad)
                evaluator.observe(prompt)
                # TODO: break this up. evluate one hypothesis at a time.
                evaluator.observe(self.entail_0)
                evaluator.observe(self.entail_1)
            self.ent_acc_0 = self.evaluator_0.act()
            self.ent_acc_1 = self.evaluator_1.act()

            for evaluator in self.evaluators:
                evaluator.observe(self.contradict_0)
                evaluator.observe(self.contradict_1)
            self.cont_acc_0 = self.evaluator_0.act()
            self.cont_acc_1 = self.evaluator_1.act()

            for evaluator in self.evaluators:
                evaluator.observe(self.neutral_0)
                evaluator.observe(self.neutral_1)
            self.neut_acc_0 = self.evaluator_0.act()
            self.neut_acc_1 = self.evaluator_1.act()

            self.turns += 1

        if self.turns == 2:
            ad = {'id': 'System', 'text': "Given the prompt and label, please rank the claims based on creativity, complexity, and relevance. Optionally, add an explanation of your ranking to help other evaluators understand your reasoning."}
            # TODO: add additional step for validity testing of each hypothesis/claim?
            for evaluator in self.evaluators:
                evaluator.observe(ad)
                evaluator.observe(prompt)
                # TODO: break this up. evluate one hypothesis at a time.
                evaluator.observe(self.entail_0)
                evaluator.observe(self.entail_1)
            self.ent_rate_0 = self.evaluator_0.act()
            self.ent_rate_1 = self.evaluator_1.act()

            for evaluator in self.evaluators:
                evaluator.observe(self.contradict_0)
                evaluator.observe(self.contradict_1)
            self.cont_rate_0 = self.evaluator_0.act()
            self.cont_rate_1 = self.evaluator_1.act()

            for evaluator in self.evaluators:
                evaluator.observe(self.neutral_0)
                evaluator.observe(self.neutral_1)
            self.neut_rate_0 = self.evaluator_0.act()
            self.neut_rate_1 = self.evaluator_1.act()

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
            'presie': self.questions,
            'answers': self.answers,
            'evaluation': self.accepted,
        }
