# On LLMs planning ability

Can LLM plan? This important question has caught a lot of attention in recent times. At the center of the debate is the discussion of whether LLMs actually can reason (over-optimism -Kambhampati, et all, 2024) or they are merely translators that can turn some problems specifications from one form to another (over-pessimism). In this post we will explore this discussion and provide some examples of how LLMs can be used in a planning framework as a powerful assistant.

## Solving a planing task

The literature on planning solver is vast and rich. The field of AI planning has been around for a long time and has produced many powerful tools and algorithms. The most common approach to solving a planning task is to use a search algorithm to find a sequence of actions that will lead from the initial state to the goal state. The search algorithm can be based on a variety of techniques, such as heuristic search, graph search, or constraint satisfaction. The search algorithm can also be guided by domain-specific knowledge, such as the causal relationships between actions, the resource constraints, and the timeline constraints.

Acording to Kambhampati et al. (2024), the planning task can be divided into two main components: knowledge and reasoning. The knowledge component includes the domain knowledge, the model of the world, and the hierarchical recipies. The reasoning component includes the ensemble of the above knowledge into executable actions with constraints.

This division can be summarized as follows:

a. Knowledge
    - Domain knowledge, 
    - A model of the world (from which causal correctness, timeline correctness, resource constraint correctness are derived), and
    - Hierarchical recipies.
b. Reasoning
    - ensemble the above knowledge into executable actions with constraints

## LLMs and planning

The strong argument against the LLM's reasoning ability is that both training and operation in LLMs are not associated with applying general principle to solve problems (reason here is related to practical judgment) but rather with the statistical treatment of language, in the form of a prediction task. 

> Even from a pure engineering perspective, a system that takes constant time to produce the next token cannot possibly be doing principled reasoning on its own. (Kambhampati et al., 2024)

That is not to say that LLMs are not useful in planning tasks. 

If neural networks are well described as 'universal function approximators', then LLMs -wich are big neural nets- could be seen too as 'universal knowledge approximators', trained on human level knowledge. They can approximate knowledge that is present in the training data, but they can't guarantee the truth of it claims, as many has pointed out they are 'non-veridical' generators.

In this sense, LLMs can be seen as a powerful assistant in planning tasks, by being able to generate plausible (but not guaranteed to be correct) plan heuristics/suggestions for many situations.








