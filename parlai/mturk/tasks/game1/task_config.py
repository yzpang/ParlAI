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
	<li>Write one sentence that is&nbsp;<strong>definitely incorrect</strong>&nbsp;about the situation or event in the prompt.</li>
	<li>Write one sentence that is&nbsp;<strong>neither</strong> definitely correct nor incorrect about the situation or event in the prompt.</li>
</ul>
<font color="red">We encourage you to write sentences that are creative and require non-trivial kinds of inference.</font> You bonuses will be based on how evaluators rank you, they will be ranking you based on creativity of your sentences.<br>

<p><strong>Evaluators:</strong> you will be shown a prompt and 3 possible hypothesis sentences for the prompt with the same type of entailment label (the hypotheses are written by other MTurk workers who are in the writer pool). The three types of entailment labels---definitely correct, definitely incorrect, and neither---are explained above in the instructions for writers. You will be shown the claims the writers wrote and your first task is to decide if the claim fits the label and the prompt. Then, <font color="red">your task as evaluators is to rank the hypothesis sentences in terms of creativity.</font> Your bonuses will be based on agreement with other evaluators.</p>


<u><strong> Examples </u></strong>
<p>
Prompt: James Jolt moved to London this past summer.
</p><br>

<p>
Label: Definitely correct
Hypothesis: Some months ago James Jolt settled down in England.
<em> Explanation: This example is made more interesting because there are some synonyms used, and the reader needs to know that London is in England.</em>
</p>


<p>
Label: Definitely incorrect
Hypothesis: In spite the Brexit turmoil, James Jolt decided to keep his home and business in London, where they have been for the past decade.
<em>Explanation: From the prompt we know that James just moved to London, and hasn't been there for 10 years. This hypothesis implies that James hasn't just moved to London without discussing moving, making it a more complicated and interesting example.</em>
</p>

<p>
Label: Neither (neither definitely correct nor definitely incorrect)
Hypothesis: James Jolt recently moved across the pond.
<em> Explanation: If James is moving from the United States, then this hyopthesis would be correct, but this may or may not be true given the prompt. Furthermore, the example is made more interesting because the reader needs to know "the pond" is sometimes used to refer to the Atlantic Ocean.</em>
</p><br>

<p>
Prompt: Mother-in-law's tongue is one of the colloquial names for Sansevieria Trifasciata plant. It tolerates most light conditions and doesn't need frequent watering, making it an ideal house plant.
</p><br>

<p>
Label: Definitely correct
Hypothesis: Sansevieria Trifasciatais a good choice for beginners and those who don't want the hassle of a needy plant.
<em> Explanation: This example is made more interesting by making the non-trivial inference that a plant that tolerates all kinds of light and is easy to water must be easy maintain and therefore good for beginners.</em>
</p>


<p>
Label: Definitely incorrect
Hypothesis: Mother in law's tongue doesn't need lots of sunlight but is easy to underwater.
<em>Explanation: The first part of this hypothesis is true and requires a step of inference from the prompt: tolerating lots of lighting conditions means it can tolerate low sunlight. The second part is a contradiction of the prompt and it uses some rephrasing by saying "underwater."</em>
</p>

<p>
Label: Neither (neither definitely correct nor definitely incorrect)
Hypothesis: Mother in law's tongue is easy to maintain, growing quickly under most conditions.
<em> Explanation: The premise doesn't state or directly imply that the plant will grow quickly, only that it will live in most conditions. The subtlety of this example makes it interesting.</em>
</p>

<u><strong> Task Bonuses </u></strong>
<p>
As an evaluator, you will be given bonuses based on how well you agree with other evaluators. You will also be able to talk to other evaluators in between examples.<br>
As a writer, you will be given bonuses based on how your hypothesis sentences are ranked by evaluators.
</p>
<!-- TODO: COMPLETE THIS. ADD BONUS BREAKDOWN -->

For more questions please refer to this <a href="https://woollysocks.github.io/NLI-games-faqs/two-faq.html" target="_blank">FAQ page</a>.
<br>
If you are ready, please click "Accept HIT" to start this task.
'''
