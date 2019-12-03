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
task_config['hit_title'] = 'Textual Entailment Game'


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

<u><strong> Textual Entailment Task </strong></u><br>
<p><strong>Writers:</strong> you will be shown a prompt that describes a situation or event. Using only this description and what you know about the world, please write</p>
<ul>
	<li>Write one sentence that is <strong>definitely correct</strong><em>&nbsp;</em>about the situation or event in the prompt.</li>
	<li>Write one sentence that <strong>might&nbsp;be correct</strong> about the situation or event in the prompt.</li>
	<li>Write one sentence that is&nbsp;<strong>definitely incorrect</strong>&nbsp;about the situation or event in the prompt.</li>
</ul>
<font color="red">We encourage you to write sentences that are creative and require non-trivial kinds of inference.</font> You bonuses will be based on how evaluators rank you, they will be ranking you based on creativity of your sentences.

<p><strong>Evaluators:</strong> you will be shown a prompt and 3 possible hypothesis for the prompt with the same type of entailment relation (the hypotheses are written by other MTurk workers who are in the writer pool). The three types of entialment relations---definitely correct, might be correct, and definitely incorrect---are explained above in the instructions for writers. <font color="red">Your task as evaluators is to rank the hypothesis sentences in terms of creativity.</font> You bonuses will be based on agreement with other evaluators.</p>


<u><strong> Examples </u></strong>
<!-- TODO: COMPLETE THIS. ADD EXAMPLES -->
<p>
Prompt: James Jolt moved to London this past summer. <br>
Label: Defintiely correct
Hypothesis: Some months ago James Jolt settled down in England.
<em> Explanation: There are some synonyms used here, and the reasder needs to know that London is in England.</em>
</p>

<p>
Prompt: James Jolt moved to London this past summer. <br>
Label: Maybe correct
Hypothesis: James Jolt recently moved across the pond.
<em> Explanation: If James is moving from the United States, then this hyopthesis would be true. The reader needs to know "the pond" is sometimes used to refer to the Atlantic Ocean.</em>
</p>

<p>
Prompt: James Jolt moved to London this past summer. <br>
Label: Definitely incorrect
Hypothesis: In spite the Brexit turmoil, James Jolt decided to keep his home and business in London, where they have been for the past decade.
<em>Explanation: TODO.</em>
</p>

<u><strong> Task Bonuses </u></strong>
<p>
As an evaluator, you will be given bonuses based on how well you agree with other evaluators. You will also be able to talk to other evaluators in between examples.<br>
As a writer, you will be given bonuses based on how your hypothesis sentences are ranked by evaluators.
</p>
<!-- TODO: COMPLETE THIS. ADD BONUS BREAKDOWN -->

If you are ready, please click "Accept HIT" to start this task.
'''
