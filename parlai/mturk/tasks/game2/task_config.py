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
In this task, we have two types of roles: <b>writers and evaluators</b>. Please read the full instructions regardless of what role you are assigned since this will help you with doing well at the task. <br><br>

<h4><u> Writers </u></h4>
<p> You will be shown a prompt that describes a situation or event. Using only this description and what you know about the world, please write</p>
<ul>
	<li>One claim that is <strong>definitely correct</strong><em>&nbsp;</em>about the situation or event in the prompt.</li>
	<li>One claim that is&nbsp;<strong>definitely incorrect</strong>&nbsp;about the situation or event in the prompt.</li>
	<li>One claim that is&nbsp;<strong>neither</strong> definitely correct nor incorrect about the situation or event in the prompt.</li>
</ul>
<font color="red">We encourage you to write claims that are creative and require non-trivial kinds of reasoning.</font> Your bonuses will be based on how evaluators rank you, they will be ranking you based on creativity of your claim.<br>

<h4><u> Evaluators </u></h4>
<p> You will be shown a prompt and then once the writers are done composing their claims, you will shown a label and 2 possible claims. The three types of labels---definitely correct, definitely incorrect, and neither---are explained above in the instructions for writers. For each label you will be asked to do the following,</p>
<ul>
	<li> You will be given the label and the two claims written by different people. Your first task is to <font color="red">decide if the claims fit the label and the prompt.</font></li>
	<li> Then, your task is to <font color="red">rank the claim in terms of creativity and complexity of reasoning.</font></li>
	<li> You have the option to leave a justification for your ranking in a text box. Anything you write here will be shown to the other evaluator at the end of ranking for the current prompt. We encourage you to use this text box generously!</li>
</ul>
Your bonuses will be based on agreement with the other evaluators on the HIT. <br>

<h4><u> Examples </u></h4>
<p>
Prompt: James Jolt moved to London this past summer.
</p>
<ul>
<li><p>
Label: Definitely correct<br>
Hypothesis: Some months ago James Jolt settled down in England.<br>
<em> Explanation: This example is made more interesting because there are some synonyms used, and the reader needs to know that London is in England.</em>
</p></li>
<li><p>
Label: Definitely incorrect<br>
Hypothesis: In spite the Brexit turmoil, James Jolt decided to keep his home and business in London, where they have been for the past decade.<br>
<em>Explanation: From the prompt we know that James just moved to London, and hasn't been there for 10 years. This hypothesis implies that James hasn't just moved to London without discussing moving, making it a more complicated and interesting example.</em>
</p></li>
<li><p>
Label: Neither (neither definitely correct nor definitely incorrect)<br>
Hypothesis: James Jolt recently moved across the pond.<br>
<em> Explanation: If James is moving from the United States, then this hyopthesis would be correct, but this may or may not be true given the prompt. Furthermore, the example is made more interesting because the reader needs to know "the pond" is sometimes used to refer to the Atlantic Ocean.</em>
</p></li>
</ul>

<p>
Prompt: Mother-in-law's tongue is one of the colloquial names for Sansevieria Trifasciata plant. It tolerates most light conditions and doesn't need frequent watering, making it an ideal house plant.
</p>
<ul>
<li><p>
Label: Definitely correct<br>
Hypothesis: Sansevieria Trifasciatais a good choice for beginners and those who don't want the hassle of a needy plant.<br>
<em> Explanation: This example is made more interesting by making the non-trivial inference that a plant that tolerates all kinds of light and is easy to water must be easy maintain and therefore good for beginners.</em>
</p></li>
<li><p>
Label: Definitely incorrect<br>
Hypothesis: Mother in law's tongue doesn't need lots of sunlight but is easy to underwater.<br>
<em>Explanation: The first part of this hypothesis is true and requires a step of inference from the prompt: tolerating lots of lighting conditions means it can tolerate low sunlight. The second part is a contradiction of the prompt and it uses some rephrasing by saying "underwater."</em>
</p></li>
<li><p>
Label: Neither (neither definitely correct nor definitely incorrect)<br>
Hypothesis: Mother in law's tongue is easy to maintain, growing quickly under most conditions.<br>
<em> Explanation: The premise doesn't state or directly imply that the plant will grow quickly, only that it will live in most conditions. The subtlety of this example makes it interesting.</em>
</p></li>
</ul>


<!-- TODO: COMPLETE THIS. ADD BONUS BREAKDOWN -->
<h4><u> Task Bonuses (TBD) </u></h4>
<p>
As an evaluator, you will be given bonuses based on how well you agree with other the other evaluator. We encourage you to use the text box to help communicate your reasoning to the other evaluator.<br>
As a writer, you will be given bonuses based on how your claims are ranked by evaluators.
</p><br>

<p>
For more questions please refer to this <a href="https://woollysocks.github.io/NLI-games-faqs/two-faq.html" target="_blank">FAQ page</a>.
<br>
Finally, if you are ready, please click "Accept" to start this task.
</p>
'''
