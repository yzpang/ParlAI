#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

task_config = {}


task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Textual Entialment Game'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config[
    'hit_description'
] = 'As a writer: Given the prompt sentence write three sentences related to the prompt.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'textual entailment,nli,rte,entailment,sentence creation,writing'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config[
    'task_description'
] = '''
In this task, we have two types of roles: writers and evaluators. Please read the full instructions regardless of what role you are assigned since this will help you with doing well at the task.

<p>
As an evaluator, you will be given bonuses based on how well you agree with other evaluators. You will also be able to talk to other evaluators in between examples.<br>
As a writer, you will be given bonuses based on how your hypothesis sentences are ranked by evaluators.
</p>

<u><strong> Textual Entailment Task </strong></u><br>
<p><strong>Writers:</strong> you will be shown a prompt that describes a situation or event. Using only this description and what you know about the world, please write</p>
<ul>
	<li>Write one sentence that is <strong>definitely correct</strong><em>&nbsp;</em>about the situation or event in the prompt.</li>
	<li>Write one sentence that <strong>might&nbsp;be correct</strong> about the situation or event in the prompt.</li>
	<li>Write one sentence that is&nbsp;<strong>definitely incorrect</strong>&nbsp;about the situation or event in the prompt.</li>
</ul>

<p><strong>Evaluators:</strong> you will be shown a prompt and 3 possible hypothesis for the prompt (the hypothesis are written by other MTurk workers who are in the writer pool). Your task is to rank the hypothesis sentences in terms of creativity.</p>

<!-- COMPLETE THIS. ADD EXAMPLES -->

If you are ready, please click "Accept HIT" to start this task.
'''
