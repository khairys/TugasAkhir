---
title: "Generation-Based Parallel Particle Swarm Optimization for Adversarial Text Attacks"
slug: "14_parallel_pso_adversarial_text_attacks"
authors: "Xinghao Yang, Yupeng Qi, Honglong Chen, Baodi Liu, Weifeng Liu"
year: 2023
venue: "Information Sciences (Elsevier), Vol. 644, Art. 119237"
doi: "10.1016/j.ins.2023.119237"
category: "Adversarial NLP & Attacks"
tags: ["adversarial-attacks", "particle-swarm-optimization", "text-perturbation", "black-box-attacks"]
total_pages: 14
character_count: 58567
word_count: 8952
source_file: "Generation-based parallel particle swarm optimization for.pdf"
extraction_date: "2026-10-20 15:10:10"
---

# Generation-Based Parallel Particle Swarm Optimization for Adversarial Text Attacks

## Metadata & Bibliographic Overview
- **Authors:** Xinghao Yang, Yupeng Qi, Honglong Chen, Baodi Liu, Weifeng Liu
- **Publication Year:** 2023
- **Venue / Journal:** Information Sciences (Elsevier), Vol. 644, Art. 119237
- **DOI / Link:** 10.1016/j.ins.2023.119237
- **Category:** Adversarial NLP & Attacks
- **Original Source File:** `Generation-based parallel particle swarm optimization for.pdf` (14 pages, ~8,952 words)

## Agent Quick-Scan / Executive Takeaways
> [!NOTE]
> **Relevance to Tugas Akhir / Research Context:**
> Theoretical analysis of automated adversarial text generation algorithms. Illustrates how targeted heuristic and metaheuristic attacks systematically exploit classifier decision boundaries.

### Key Thematic Dimensions
- **Domain:** Adversarial NLP & Attacks
- **Methodology Focus:** adversarial-attacks, particle-swarm-optimization, text-perturbation, black-box-attacks
- **Relevance Anchors in Repo:** Connects to Stage 8 (Data Leakage & Pairing), Stage 9 (Baseline Models), Stage 10 (Adversarial Robustness O1-O4), and Stage 11 (Domain Shift OOD).

---

# Full Extracted Document Text



<!-- PAGE 1 -->

Information Sciences 644 (2023) 119237
Available online 1 June 2023
0020-0255/© 2023 Elsevier Inc. All rights reserved.
Contentslistsavailableat ScienceDirect
Information Sciences
journal homepage: www.elsevier.com/locate/ins
Generation-based parallel particle swarm optimization for 
adversarial text attacks
XinghaoYang,  YupengQi,  HonglongChen,  BaodiLiu,  WeifengLiu ∗
College of Control Science and Engineering, China University of Petroleum (East China), Qingdao 266580, Shandong, PR China
A R T I C L E I N F O A B S T R A C T
Keywords:
Natural language processing
Adversarial machine learning
Text attack
Parallel computation
Text adversarial attack is an effective strategy to investigate the vulnerability of Natural Language 
Processing (NLP) models. Most of text attack studies focus on word-level attacks with static or 
dynamic optimization algorithms. However, they are hard to balance (1) attack performance (i.e., 
attack success rate, word substitution rate) and (2) attack efficiency. Generally, static optimization 
is fast but suffers from low attack performance, and the dynamic adversary improves the attacking 
quality but is time-consuming. To address these challenges, a Generation-based Parallel Particle 
Swarm Optimization (GP2SO) is proposed for the adversarial text attack. Specifically, the GP2SO 
employs an adaptive strategy to determine the word modification priority, which produces a 
high attack performance owing to the aggressive objective function. To achieve time efficiency, 
we parallelize the PSO on multiple pipelines in a generation-overlapping manner. Extensive 
experiments on four public text recognition datasets are conducted by attacking four deep models 
to evaluate the effectiveness of the GP2SO. Experimental results manifest that the proposed 
GP2SO averagely improves the time efficiency by 272% with only 0.3% success rate reduction 
compared to the PSO. Besides, the GP2SO also shows superiorities in adversarial training and 
transferability compared with baselines. The code is provided to ensure reproducibility https://
github .com /OutdoorManofML /GPPSO.

## 1. Introduction

Modern Natural Language Processing (NLP) models have shown vulnerabilities towards adversarial text examples [1]. Generally, 
adversarial text examples refer to the legitimate input with some minor modifications. These modifications are usually too stealthy to 
distinguish by human readers but can cause catastrophic results on well-optimized language models, e.g., BERT [2]. This phenomenon 
brings great challenges to the secure application of modern language models, especially in some security-sensitive tasks, such as 
medical detection [3], spam filtering [4], web phishing [5], etc. To investigate the properties of NLP models and improve their 
robustness before implementation, several groups of adversarial text attack studies have been proposed and applied at character, 
word, and sentence granularities [6].
Firstly, the character-level attack strategies aim to fool a target model by inserting (𝑛𝑜𝑖𝑠𝑒 →𝑛𝑜𝑜𝑖𝑠𝑒), erasing (𝑛𝑜𝑖𝑠𝑒 →𝑛𝑜𝑠𝑒), or 
scrambling (𝑛𝑜𝑖𝑠𝑒 →𝑛𝑜𝑠𝑖𝑒) characters [7,8]. However, these manipulations usually lead to misspelled words and can be easily detected by a spell check machine. Secondly, the sentence-level attack methods train a sentence paraphrase model with a syntactic 
controller so that the adversarial sentence follows the specified syntax yet keeps the sentence meaning unchanged [9,10]. Never-
* Corresponding author.
E-mail address:liuwf@upc.edu.cn(W.Liu).
https://doi.org/10.1016/j.ins.2023.119237
Received 30 October 2022; Received in revised form 4 April 2023; Accepted 23 May 2023

---


<!-- PAGE 2 -->

Information Sciences 644 (2023) 119237
2
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
theless, the paraphrase models ignore the downstream applications during training, so it is hard to ensure a high attack success 
rate. To circumvent these problems, most of recent researches focus on word-level attack, which replaces the input words with their 
semantically close candidates. The major challenges of word-level attack are: (1) how to collect substitution candidates for each 
input word and (2) how to determine the word modification priority.
To address the first problem and improve the semantic consistency, the substitution candidates are typically selected from word 
embedding space [11,12], human-annotated thesauri [13,14], or pre-trained language models [15,16]. Early works [11]search  substitution candidates from the count-based GloVe embedding space, which represents the word distance according to the co-occurrence 
probability [17]. However, the embedding distance is not equal to the semantic distance -some  frequently co-occurring words, e.g., 
{𝑒𝑥𝑝𝑒𝑛𝑠𝑖𝑣𝑒, 𝑐ℎ𝑒𝑎𝑝}and {𝑤𝑒𝑠𝑡, 𝑒𝑎𝑠𝑡}, are semantically opposite. Therefore, a counter-fitting post-processing is often necessary [18]. To 
avoid this problem, Ren etal.  [13]search  synonym candidates from WordNet, which groups words by their conceptual-semantic and 
lexical relations. Zang etal.  [14]show  that the sememe-based1 HowNet can provide much more suitable candidates than WordNet. 
For example, the word "pie" has no synonym found in WordNet, but it has more than 60 substitutes in HowNet. Recently, Li etal.  
[16]a n d Garg et al. [15]t a k e the advantage of BERT Masked Language Model (BERT-MLM) to predict context-aware substitution 
candidates to improve the fluency of adversarial texts. However, the BERT-MLM can not ensure the semantic coherence, as predicting 
the [MASK] as 'good' or 'bad' in the sentence 'the food was [MASK]' is equally fluent but results in different semantics.
In the second step, designing a proper word replacement sequence can significantly enhance the attack success rate and reduce 
the perturbation cost. A variety of methods have been proposed to optimize the word replacement order, which can be roughly 
categorized into static [12,13]a n d dynamic optimizations [11,14,19]. The static methods usually define a Word Important Score 
(WIS) and proceed with the attack by following the WIS descending order. A straightforward method is iteratively removing each 
input word and calculating the prediction change before and after the word deletion [20,12,15]. This method employs some incomplete sentences to evaluate the word importance, which may lead to a biased estimation. Alternatively, Ren etal.  [13]and  Li etal.  
[16] measure the word importance by replacing every word with a special symbol, i.e., [MASK], and check how much the output 
probability shifted. Once the WIS is determined, these attack algorithms will replace the input words one by one, following the WIS 
descending order. The dynamic methods usually apply heuristic optimizations to determine the word modification priority, such as 
Genetic Algorithm (GA) [11]a n d Particle Swarm Optimization (PSO) [14]. Specifically, the GA randomly initializes some possible 
word replacements as a generation and defines the fitness function as the target label probability. With the iteration of crossover 
and mutation, fitter solutions can be gradually selected to achieve the targeted attack. In [14], Zang etal.  build a discrete space to 
optimize the particle's position, where each particle denotes a possible adversarial candidate. Similar to GA, the PSO evaluates the 
position quality by the target label score, but updates the velocity and position according to not only the individual best position but 
also the global best position. Yang etal.  [19]presented  the bigram and unigram based word substitution strategy to avoid breaking 
the phrases, while the computational efficiency of the monotonic heuristic search also needs improvements.
In general, prior static attacks and dynamic attacks exist a trade-off between the attack performance and the efficiency of attack time. For static attacks, no matter how the WIS is defined, the static sequence is generally not going to be the optimal order. 
The reason is that the input sentence is continuously changed with the word replacement going, so the word importance is also 
dynamically varied. Therefore, replacing words with a static WIS often leads to a low attack success rate and word over-substitution. 
For the dynamic attacks, the major merit of the dynamic strategy lies in the fitness of objective function changing with the word 
altering. So the substitution order can better fit the objective function and thus improves the attacking quality, i.e., attack success rate, word substitution rate, semantic consistency, and sentence fluency. But they usually need a large number of queries 
to the victim model, which significantly increases the computation cost and consumes much more time on average to complete 
attacks.
In this paper, a novel method named Generation-based Parallel Particle Swarm Optimization (GP2SO) is proposed to yield high 
quality adversarial text sentences and simultaneously improve the attack time efficiency. Specifically, the GP2SO selects sememeconsistent candidates from HowNet in the first stage, which can provide sufficient options and avoid the polyseme problem. This 
means only the candidates that share at least one common sememe with the original word can be selected. In the second stage, 
a generation-based parallel particle swarm optimization is employed to improve the attack efficiency. Traditional population-level 
parallelism divides the population into several sub-populations and deploys them on multiple machines (or machines with multiple 
cores), which must wait for all sub-routines to complete before starting the next generation. In the generation-based parallel execution, some particles are allowed to go to the next generation once they have finished their local evolution, even though the current 
generation has not finished. This can greatly save optimization time with only a slight loss of attack success rate. Besides, the GP2SO 
employs the industrial pipeline technique, which enables it to run with only one CPU core on multiple virtual pipelines. In other 
words, the proposed GP2SO does not rely on multiple core machines to ensure the parallel optimization. The major contributions of 
this paper are summarized into the following three areas.
•W e search the substitution candidates from sememe-based HowNet space. Compared with the candidates from word embedding 
space [11,12]and  pre-trained language models [16], the sememe-based candidates can provide sufficient modification options 
and avoid the polyseme problem.
1 Sememe: the minimum semantic unit in linguistics.

---


<!-- PAGE 3 -->

Information Sciences 644 (2023) 119237
3
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
•W e design a dynamic attack method named Generation-based Parallel PSO (GP2SO) to reduce the attack time compared with 
the previous dynamic attacks [11,14]. Moreover, the proposed GP2SO can produce higher quality adversarial text examples than 
the baselines.
•W e evaluate the effectiveness of the GP2SO on both sentiment analysis and language inference tasks by comparing with static 
baselines [13,12,16,21]and  dynamic baselines [11,14]. Experimental results show that the GP2SO generates high quality adversarial text samples (evaluated by four metrics) and also reduces the attack time.
The rest of this paper is organized as below. Section 2 reviews some related works, including both word-level attack methods 
and parallel strategies. Section 3 discusses the proposed attack algorithm in detail. Experimental settings and results are analyzed 
in Section 4. Further study including adversarial training, transferability and the discussion on the uncertainty and sensitivity are 
evaluated in Section5. Finally, Section6concludes this paper and points out potential future directions.

## 2. Related Work

In this section, we discuss the related works from two aspects, including the word-level text adversarial attack methods and the 
parallel computation for the PSO.
2.1. Word-level textual adversarial attack
The word-level attack methods can be categorized into static attacking and dynamic (heuristic) attacking methods according to 
how they optimize the word modification priority. The static attacking methods perform the word perturbation by a fixed sequence, 
which is usually defined by Word Importance Score (WIS) or following the original word input order. For example, in order to find 
the vulnerable words of the original input sentence, Jin et al. [12] delete each word of the input sentence iteratively and calculate 
the prediction change before and after deleting the word as the importance score. Li et al. [16]u t i l i z e a special symbol [MASK] to 
replace each original word in the input sentence and calculate the logit output change of the victim model as the WIS. Ren et al. 
[13]e m p l o y the Probability Weighted Word Saliency (PWWS) to measure the sensitivity degree of the victim model towards each 
input word. Liu et al. [21]c o n s i d e r that crafting adversarial examples is equal to selecting a subset from all combinations of the 
candidates, and the selection is according to three modifications to the candidates, i.e., insertion, deletion, and exchange. However, 
these predefined attack sequences usually lead to incorrect combinations, as the input sentence is constantly changed after each 
modification.
Intuitively, the rational solution should dynamically determine the next perturbed word after each modification. The heuristic 
attacking method employs meta heuristic algorithm to craft adversarial examples as a combinatorial problem. Alzantot et al. [11]
apply genetic algorithm (GA) in the count-based GloVe embedding space to optimize the attack performance. Specifically, the 
initial generation of GA is generated by repeating the Perturb subroutine S times, where the Perturb subroutine modifies a word by 
maximizing the target label score. Every next generation is optimized by crossover and mutation, imitating the natural selection, 
until the classifier is misled to the target label. Zang et al. [14] apply particle swarm optimization (PSO) to optimize the attack 
performance and search candidates from HowNet. Unlike GA, the PSO initializes a particle's position by replacing the input word in 
a random manner instead of by maximizing the target label's confidence. The first generation can be obtained by randomly running 
this procedure for many times, and the particles' velocity is gradually optimized according to the individual best position and global 
best position. The common part of these two methods is that they need to perturb the input sentence many times at first to get a set 
of modified text examples as the initial generation, and then the generation quality is improved by iteratively optimizing the fitness 
function in a heuristic manner. Therefore, one drawback for GA and PSO is that both of them are computationally expensive and 
require a large amount of time for the optimization steps. To make a fair comparison for the optimization algorithm, Yoo etal.  [22]
conducted comprehensive experiments by constraining the same search method of candidates. As the conclusion of their study, PSO 
has a higher attack success rate than GA, and the heuristic optimization greatly improves the attack success rate and reduces the 
word substitution rate compared to the static counterparts.
2.2. Parallel strategies
Existing parallelisms for PSO can be divided into data parallelism and task parallelism according to the parallel approach for 
data or the fitness function. For example, Lalwani et al. [23] divide the implementation of parallelism PSO (PPSO) into two ways: 
synchronous and asynchronous. If the velocity and position of each particle are updated by the end of one iteration, the PPSO 
algorithm is synchronous; otherwise, the PPSO is regarded as asynchronous. Fu et al. [24] propose a fast neighbor search method 
while each particle has to wait for updates at the end of an iteration. Ali Alouache [25]s p l i t s the population into 𝑀 groups and 
evolves all the groups simultaneously by using multiple processors. Inspired by the industrial pipeline technique, Li etal.  [26]firstly  
attempt to introduce the pipeline idea into PSO and propose a generation-level PPSO, which belongs to an asynchronous implement 
of PPSO. Based on the local version of particle swarm optimization (LPSO), a generation-level PPSO allows some particles to perform 
their evolutions in the current generation, while some other particles can simultaneously go to the next generation to carry out the 
new evolutions. So, it is substantially accelerated on the evolutionary speed without extra waiting for updating at the end of an 
iteration.

---


<!-- PAGE 4 -->

Information Sciences 644 (2023) 119237
4
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Fig. 1.The framework of the GP2SO. To be clear, five particles are employed to illustrate the steps to produce textual adversarial examples. Each sentence is regarded 
as a particle, and a generation-level parallel updating strategy is utilized to optimize particles until producing a successful attack.

## 3. Methodology

In this section, we firstly review the objective of word-level textual adversarial attacks. Then the proposed GP2SO is carefully 
discussed, including how to select the substitution candidates and how to determine word modification priority. The procedure of 
GP2SO to craft adversarial examples is shown in Fig.1.
3.1. Objective of word-level textual attack
Given a black-box classifier 𝐹 and an input sequence 𝑋 ={𝑤1, 𝑤2, ⋯ , 𝑤𝑛}with label 𝑌𝑡𝑟𝑢𝑒, where 𝑤𝑖 is the 𝑖-th word. For all the 
possible outputs of 𝐿labels  ={𝑌1, 𝑌2, ⋯ , 𝑌𝐿}, a correct classification can be defined as
argmax
𝑌𝑖∈
𝐹(𝑌𝑖 ∣ X)= 𝑌𝑡𝑟𝑢𝑒 (1)
Textual adversarial attack aims to craft an adversarial example 𝑋∗ with an imperceptible perturbation Δ𝑋, i.e., 𝑋∗ =𝑋 +Δ𝑋, so 
that the well-optimized classifier F is misled to an erroneous prediction
argmax
𝑌𝑖∈
𝐹(𝑌𝑖 ∣𝑋∗) ≠𝑌𝑡𝑟𝑢𝑒 (2)
For word-level textual attacks, the adversarial example 𝑋∗ is usually crafted by the replacement of one or more original words 
in 𝑋 with their synonyms. Therefore, 𝑋∗ is the combination of the original words and the perturbed words by the replacements. 
To ensure the adversarial example is imperceptible to a human, the adversarial perturbation needs to satisfy lexical correctness, 
grammatical correctness and semantic similarity.
Suppose the DNN model can correctly recognize the sentiment of the input sentence X as negative. The aim of achieving a 
successful attack is to replace several words in Xto craft the adversarial example 𝑋∗ so that the classifier makes a wrong prediction, 
i.e., positive.

---


<!-- PAGE 5 -->

Information Sciences 644 (2023) 119237
5
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Fig. 2. As "Intern" and "Medico" share the common sememes, i.e., "Occupation", "Medical", "Doctor", and "Human". They can be interchangeable when crafting 
adversarial examples.
3.2. Sememe-based candidates
The sememe is defined as the minimum unit of human languages in linguistics. In the field of Natural Language Processing, the 
sememe can be used as the semantic label of words. HowNet is a well-known language knowledge base, which represents words with 
a sememe tree (as shown in Fig.2). In this work, the original words are substituted by the candidates who share at least one common 
sememe label with them. For example, the word "Intern" in HowNet can be represented with the sememes "human", "occupation", 
"medical", "doctor", while the word "medico" has the same sememes as the word "Intern", therefore they are interchangeable when 
crafting adversarial examples without semantic loss. In order to meet lexical, grammatical, and semantic constraints, only the nouns, 
verbs, adjectives and adverbs can be replaced with their sememe candidates. Besides, the synonyms are restricted that must have 
the same part-of-speech (POS) tags as the original words to reduce grammar errors. Let 𝑃𝑂𝑆𝐹𝑖𝑙𝑡𝑒𝑟 denote the filter function for POS 
tags. Considering different forms of a word, e.g., the word in the plural, a 𝐿𝑒𝑚𝑚𝑎𝑡𝑖𝑧𝑒 function is defined to conduct lemmatization 
to find more substitute words, and use a 𝐷𝑒𝑙𝑒𝑚𝑚𝑎𝑡𝑖𝑧𝑒 function to perform delemmatization before the final modification to ensure 
grammatical correctness.
After the above operations, a discrete search space of the original words and their candidates can be obtained. Let 𝕊(𝑤𝑖)denote 
the set of high quality synonyms substitutes for 𝑤𝑖. A rational adversary attacker aims to mislead the well-trained classifier by 
optimizing the word modification priority, so the fixed classifier is the victim model in the attacker's optimization problem. That is 
to say, the next step for the GP2SO is to optimize the combination of original words and their synonyms in the discrete search space.
3.3. Generation-based parallel particle swarm optimization (GP2 SO)
The classifier is optimized in advance and remains unchanged during the optimization of word replacement priority, i.e., the attacking optimization. To improve the optimization efficiency, a Generation-based Parallel Particle Swarm Optimization (GP2SO) 
is presented, where PSO is a heuristic algorithm to simulate the predation behavior of a flock of birds. Specifically, given a 
swarm with 𝑁 particles, each particle has a position vector as 𝑋𝑗 ={ 𝑤𝑗,1, 𝑤𝑗,2, ⋯ , 𝑤𝑗,𝑛 |𝑗 =1  ⋯ 𝑁}, and a velocity vector as 
𝑉𝑗 ={𝑣𝑗,1, 𝑣𝑗,2, ⋯ , 𝑣𝑗,𝑛 |𝑗 =1  ⋯ 𝑁}, where 𝑛 is the dimension of the problem and 𝑗 is the 𝑗-th particle. Each position in the search 
space corresponds to a solution, and the objective function 𝐽(⋅)is defined as the fitness of each position. Additionally, with the evolution going, each particle records its historical highest optimization score with a position vector 𝑋𝑗,𝐻 ={𝑤𝑗,𝐻1, 𝑤𝑗,𝐻2, ⋯ , 𝑤𝑗,𝐻𝑛}and 
the swarm records the best position among all particles during a generation, i.e., 𝑋𝐺 ={𝑤𝐺,1, 𝑤𝐺,2, ⋯ 𝑤𝐺,𝑛}. The concept of local best 
position 𝑋𝑙𝑜𝑐𝑎𝑙 is employed in order to speed up the optimization, which means the best position among the 𝑗-th particle's neighbors 
instead of the whole generation. In the text adversarial attack problem, each position corresponds to a sentence, and each dimension 
corresponds to a word. This means 𝑋𝑗 ={𝑤𝑗,1, ⋯ 𝑤𝑗,𝑑, ⋯ 𝑤𝑗,𝑛}is the 𝑗-th particle, and 𝑤𝑗,𝑑 is the variable corresponding to the 𝑑-th 
dimension. The fitness function 𝐽(⋅)is defined as the target label's prediction probability to conduct a targeted attack
𝐽(𝑋𝑗)= 𝐹 (𝑌𝑡𝑎𝑟𝑔𝑒𝑡 |𝑋𝑗
) (3)
Intuitively, a higher objective value is preferred to produce a successful targeted attack.
The optimization includes four steps, i.e., initialization, record, updating, and termination. Following Zang et al. [14], the four 
steps are discretized and a probabilistic method is applied to update the position of a particle to the best positions so that it can adapt 
to discrete search space to craft word-level adversarial examples.
Initialization: given the input sentence, one word is randomly substituted for creating the initial particle, and repeat this procedure for 𝑁 times to obtain the initial generation. Record: with the continuous position moving, each particle's historical best 
position 𝑋𝑗,𝐻 and the local best position 𝑋𝑙𝑜𝑐𝑎𝑙 can be recorded according to the objective function. Update: for the 𝑗-th particle, 
the velocity is updated according to the recorded historical best position 𝑋𝑗,𝐻 and local best position 𝑋𝑙𝑜𝑐𝑎𝑙 weighted by an inertia 
parameter 𝑤
𝑉𝑡+1
𝑗 =𝑤×𝑉𝑡
𝑗 +(1− 𝑤)×[ 𝑠𝑖𝑔𝑛(𝑋𝑡
𝑗,𝐻,𝑋𝑡
𝑗)+ 𝑠𝑖𝑔𝑛(𝑋𝑡
𝑙𝑜𝑐𝑎𝑙,𝑋𝑡
𝑗)] (4)
where the inertia is restricted to 0 <𝑤𝑚𝑖𝑛 <𝑤  <𝑤𝑚𝑎𝑥 <1, and the value is designed to decrease with the increase of iterations times 𝑡
before the iteration upper bound 𝑇

---


<!-- PAGE 6 -->

Information Sciences 644 (2023) 119237
6
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
𝑤=(𝑤𝑚𝑎𝑥 −𝑤𝑚𝑖𝑛)× 𝑇 −𝑡
𝑇 +𝑤𝑚𝑖𝑛 (5)
The 𝑠𝑖𝑔𝑛(𝑥, 𝑦)is defined as
𝑠𝑖𝑔𝑛(𝑥,𝑦)=
{ 1,𝑥 =𝑦,
−1,𝑥 ≠𝑦.
(6)
Then a two-step probabilistic method is utilized to update the particle to the best position. Particularly, the historical movement 
probability 𝑃𝐻 decides whether the particle moves to its historical best position, and the local movement probability 𝑃𝑙𝑜𝑐𝑎𝑙 determines 
if the particle approaches to the local best position. These two probabilities are changed with iteration going as below
𝑃𝐻 = 𝑃𝑚𝑎𝑥 − 𝑡
𝑇 ×(𝑃𝑚𝑎𝑥 −𝑃𝑚𝑖𝑛)
𝑃𝑙𝑜𝑐𝑎𝑙 = 𝑃𝑚𝑎𝑥 + 𝑡
𝑇 ×(𝑃𝑚𝑎𝑥 −𝑃𝑚𝑖𝑛)
(7)
where 0 <𝑃𝑚𝑖𝑛 <𝑃𝑚𝑎𝑥 <1. Eq.(7)enables  the particles to tend to their individual best solution at the early stage and then gradually 
move to the local best position with 𝑡 increase. Once the movement direction is determined (towards the historical best or local 
best), one of the particle's dimensions will be selected according to the probability of velocity, i.e., 𝑠𝑖𝑔𝑚𝑜𝑖𝑑(𝑣𝑗,𝑑). Then the selected 
dimension/word will be updated to the corresponding destination word.
Termination: after the position updating, the victim model is queried to judge whether the new adversarial example can lead 
to a wrong prediction or the number of iterations up to 𝑇. If yes, the optimization will be terminated and return the adversarial 
example. Otherwise, some particles will be selected by a probability 𝑃𝑀 to perform a 𝑀𝑈𝑇𝐴𝑇𝐸 step, i.e., randomly substitute one 
word to enhance the diversity
𝑃𝑀 =1− 𝑚𝐷(𝑋,𝑋𝑘)
𝑛
(8)
where 𝑚 is a positive constant, 𝐷 measures the number of different words between the original input sentence 𝑋 and the crafted 
sentence 𝑋𝑘.
Generation-based P2SO. Traditional PSO runs the four stages sequentially one generation by another, which is inefficient in 
adversarial text optimization. In this work, a generation-based parallel technique is utilized to speed up the four stages. Particularly, 
the GP2SO allows some particles, who finished the local best position updating, to start the next generation in advance, without 
waiting for all particles' global best position. The local best position of a particle depends on the positions of its neighbor particles. 
Intuitively, the more time a particle waits for the positions of its neighbor particles, the less time efficiency of the GP2SO is. Therefore, 
the local best position should be selected from the closest two particles to balance the performance and efficiency. For example, in 
Fig. 1, the second generation can be started when the particle 2 obtains its local best position according to the neighbor particles 
(1 and 3), unnecessary to wait for all particles to complete position updating. Therefore, in the generation-based parallel execution, 
the particle 2 is pushed to the next generation by starting a new thread at the beginning of updating particle 4. The two threads will 
simultaneously update the local best position of particle 2 and the historical best position of particle 4. The rest generations can be 
optimized in the same way to achieve generation-level parallelism.
Algorithm 1 shows the workflow of the proposed GP2SO. Firstly, initialize the iteration times 𝑡 =0, three global variables 
𝑁𝑒𝑖𝑔ℎ𝑏𝑜𝑟 =3, 𝐺 =0, and 𝑅 =0 as shown in line 1 of Algorithm 1. The global variable 𝐺 indicates the generation of each particle, 𝑅 denotes the index of the particle to be updated, and 𝑁𝑒𝑖𝑔ℎ𝑏𝑜𝑟 is the least number of particles to calculate the local optimal 
position. Next, for the given input sentence 𝑋, find substitution candidates for each input word as shown in lines 2-7. Then, repeat 
the one word random replacement procedure for 𝑁 times to get the initial generation {𝑋0
1, 𝑋0
2, ⋯ , 𝑋0
𝑁} as shown in line 8. In the 
beginning, only one thread is working, each particle goes through Recordand Updatingas shown in lines 13 and 14, respectively. 
After position updating, the particle queries the victim model to check if the adversarial examples can achieve a successful attack 
(line 15). Then, to enhance the search ability, a 𝑀𝑈𝑇𝐴𝑇𝐸 step is applied to some particles as aforementioned in lines 18-19. When 
there are enough neighbor particles to calculate the local optimal position 𝑋𝑡
𝑙𝑜𝑐𝑎𝑙 of particle 𝑋𝑡
𝑅, a new thread will be activated to 
start a new generation. The new thread will update the position, velocity of particle 𝑋𝐺
𝑅 and its subsequent particles in line 24. For 
each generation in different threads, 𝐺 denotes which generation is updating. The optimization will stop if a successful adversarial 
example is found or the iteration reaches the upper bound.

## 4. Experiments and Results

In this section, we evaluate the proposed GP2SO on sentiment analysis and natural language inference tasks. Six typical word-level 
text attack methods are selected as the baselines for empirical evaluation.
4.1. Baseline methods
• BEAT:BERT Attack (BEAT) [16]replaces  each of the original words by a dummy symbol [MASK] and calculates the difference of 
the victim model's outputs to find the sensitive words. Based on Bytes-Pair-Encoding (BPE), BEAT collects the top-K candidates 
of all the sub-words by BERT Masked Language Model.

---


<!-- PAGE 7 -->

Information Sciences 644 (2023) 119237
7
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Algorithm 1: Generation based GP2SO.
Input:Original sample 𝑋, target label 𝑦
Input:Victim model 𝐹(⋅)
Output:Adversarial example 𝑋𝑎𝑑𝑣
1 Parameter initialization: The iteration times 𝑡 =0, global variables 𝐺=0 and 𝑅 =0, 𝑁𝑒𝑖𝑔ℎ𝑏𝑜𝑟 =3;
/* Sememe Candidates Selection */
2 for 𝑤𝑖 in 𝑋 do
3 𝑤𝑖 ←𝐿𝑒𝑚𝑚𝑎𝑡𝑖𝑧𝑒(𝑤𝑖);
4 𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝑠  ←Generate with HowNet;
5 𝑠𝑢𝑏𝑠𝑡𝑖𝑡𝑢𝑡𝑒𝑠 ←𝐷𝑒𝑙𝑒𝑚𝑚𝑎𝑡𝑖𝑧𝑒(𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝑠);
6 𝕊(𝑤𝑖) ←𝑃𝑂𝑆𝐹𝑖𝑙𝑡𝑒𝑟 (𝑠𝑢𝑏𝑠𝑡𝑖𝑡𝑢𝑡𝑒𝑠)
7 end
8 Initialize the first generation {𝑋0
1, 𝑋0
2, ⋯ , 𝑋0
𝑁};
/* Parallel Optimization Starts */
9 while t < 𝑇 do
10 𝑗 =1; ⊳Particle index
11 Set up 𝑤, 𝑃𝐻, 𝑃𝑙𝑜𝑐𝑎𝑙 by Eq.(5)and  Eq.(7);
12 while j < N do
13 Record the fitness score 𝐽(𝑋𝑡
𝑗)via Eq.(3);
14 Update the position and velocity via Eq.(4);
15 if 𝐹(𝑋𝑡
𝑗) ==𝑌𝑡𝑎𝑟𝑔𝑒𝑡 then
16 return 𝑋𝑎𝑑𝑣 ←𝑋𝑡
𝑗
17 end
18 Calculate the mutating probability 𝑃𝑀;
19 𝑀𝑈𝑇𝐴𝑇𝐸 ( 𝑋𝑡
𝑗, 𝑃𝑀);
20 Update 𝑋𝑡
𝑗,𝐻 of 𝑋𝑡
𝑗;
21 if 𝑗>𝑁𝑒 𝑖 𝑔ℎ 𝑏 𝑜 𝑟then
22 𝑅 =𝑗 −𝑁𝑒𝑖𝑔ℎ𝑏𝑜𝑟 +1;
/* Pipeline technique */
23 Update local best position of 𝑋𝑡
𝑅;
24 Activate a new thread to update 𝑋𝐺
𝑅 and its subsequent particles;
25 𝐺=𝐺+1;
26 end
27 𝑗 =𝑗 +1;
28 end
29 𝑡 =𝐺+1;
30 end
31 return 𝑁𝑜𝑛𝑒
• TextFooler: TextFooler [12]m o d i fi e s words by a predefined word importance ranking and searches substitution candidates 
from GloVe-based counter-fitting word embedding space.
• PWWS: Probability Weighted Word Saliency (PWWS) [13]i s another static optimization method, which considers both word 
saliency and probability change to determine the replacement order. And PWWS collects the candidate words from WordNet.
• LS:Local Search [21](LS)  selects a subset from all combinations of candidates, and a local search algorithm is applied to greedily 
determine the word combinations according to three modifications of candidates, i.e., insertion, deletion and exchange. For a 
fair comparison, LS applies HowNet to build the set of substitution words.
• GA: Genetic Algorithm (GA) [11]i s a dynamic optimization method to determine the word replacement priority. The search 
space is defined as the counter-fitting word embedding. Besides, it utilizes Google's 1 billion words language model to filter out 
words that do not fit the context. However, the Google's language model needs abundant time which could cause an unfair time 
efficiency comparison, so the Google's language model is not applied to this baseline method.
• PSO:Particle Swarm Optimization (PSO) [14]treats  word-level attacking as a multivariate combinatorial optimization problem. 
It employs discrete PSO to find the final modified sentence in the HowNet sememe space.
4.2. Datasets and victim models
For the sentiment analysis task, we evaluate our method with two datasets including SST-2 [27]a n d Movie Review (MR) [28]. 
Both of them have two labels, i.e., {𝑝𝑜𝑠𝑖𝑡𝑖𝑣𝑒, 𝑛𝑒𝑔𝑎𝑡𝑖𝑣𝑒}. Besides, the Question Natural Language Inference (QNLI) [29]and  the Stanford 
Natural Language Inference (SNLI) [30]a r e selected for the natural language inference evaluation. QNLI is a binary classification 
dataset, which is used to determine whether the context contains the answer to a specific question. And SNLI is a tripartite classification dataset to deduce the logical relationship between a pair of text sequences, i.e., entailment, contradiction and neutral. The 
average number of words of sentences in these datasets and dataset partitions are summarized in Table1.
Four victim models are applied for the proposed attacking method, including CNN, BERT [2], DistilBERT [31], and RoBERTa 
[32]. The CNN is built by a 1-D convolutional layer, containing 150 filters with filter sizes of 3 ×4  ×5. The embedding layer is 
200-dimension and the maximum sequence length is 128. The well-trained BERT (bert-base-uncased), DistilBERT (distilbert-base-

---


<!-- PAGE 8 -->

Information Sciences 644 (2023) 119237
8
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Table 1
Statistics of datasets. Avg.W denotes the average number of word 
for each sentence.
Dataset Avg.W Class #Train #Test #Valid
MR 18.64 2 8,530 1,066 1,066
SST-2 17.40 2 67,349 1,821 872
QNLI 38.31 2 104,743 5,463 5,463
SNLI 20.27 3 550,152 10,000 10,000
Table 2
Model accuracy.
Dataset BERT DistilBERT RoBERTa CNN
MR 83.8% 83.4% 88.3% 76.8%
SST-2 92.4% 90.0% 94.0% 82.7%
QNLI 90.4% 86.0% 91.7% -
uncased, distilbert-base-cased) and RoBERTa (roberta-base) are downloaded from the Transformer model hub HuggingFace.2 For 
BERT, DistilBERT and RoBERTa, the tokens are embedded into a vector space with 768 dimensions. Note that, in order to have 
the same experimental scenario as [21], the BERT model is only used for the attack experiment of the SNLI dataset. The original 
classification accuracy of these victim models is summarized in Table2.
4.3. Experimental settings
In order to evaluate the attack performance of the victim model, 1000 examples are randomly selected from the test set for the 
attack experiments. For the parameters selected by the user in the GP2SO, 𝑤𝑚𝑖𝑛 and 𝑤𝑚𝑎𝑥 are set to 0.2 and 0.8, 𝑃𝑚𝑖𝑛 and 𝑃𝑚𝑎𝑥 are 
also set to 0.2 and 0.8. As for the positive constant 𝑚 in the random mutation step, it is set to 2 as same as Zang et al. [14]. The 
maximum iteration 𝑇 is set to 20, and the number of the swarm 𝑁 is set to 60, which is the same as the dynamic attacks [11,14]. 
All experiments are carried out on Ubuntu 18.04.5 LTS with Intel (R) Xeon (R) Silver 4214R 2.40GHz CPU, Tesla V100s-PCIE-32GB 
GPU, and 376GB RAM. For other baselines, their authors recommended parameter values are employed for the comparison. Except 
for the attack experiment of LS, all experiments are implemented on the TextAttack framework [33]. The attack experiment of LS is 
conducted by the author-provided code, and only the attack success rate, average perturbed words, and attacking time are calculated 
as same as [21].
4.4. Evaluation metrics
We evaluate the attacking method with the following automatic metrics:
• Attacking Success Rate (ASR):The ratio of the successful attacks to the total number of attacks. Note that the input sentences 
which are wrongly classified by the victim model have been skipped. The higher ratio of successful attacks, the stronger the 
attacking method.
• Average Perturbed Words (APW):The percentage of words substituted compared with the original input sentence. For static 
attacking methods, it indicates the effectiveness of WIS. For heuristic attacking methods, it indicates the search ability of the 
heuristic algorithm. Lower APW indicates better attack performance.
• Attacking Time (AT):The average time consuming for conducting an attack. Notice that, the time consuming of skipped input 
sentences which are wrongly classified before conducting the attack are excluded.
• Semantic Similarity (SIM): The semantic similarity between the original input and adversarial example. Following Jin et al. 
[12], the universal sentence encoder (USE) [34]is  applied to calculate the semantic similarity between two sentences. A higher 
USE score is desired in terms of generating semantic consistency textual adversarial examples.
• Perplexity (PPL):This measures the fluency of generated adversarial examples. The perplexity is calculated using GPT-2 [35]. 
The lower PPL score indicates a smoother sentence.
4.5. Attack performance
Fig.3shows the attack success rate, average perturbed words, and attacking time of LS, PSO, and the proposed GP2SO. Obviously, 
the GP2SO slightly reduces the attack success rate compared with PSO by 0.88%, but it perturbs the least number of words and greatly 
improves the attacking efficiency. Table 3 lists the attack results of the other five baselines and the GP2SO in terms of ASR. From 
Table 3 can be seen that the GP2SO achieves the highest or second-highest attack success rate compared with the five baselines. 
2 Models can be found here: https://huggingface .co /models.

---


<!-- PAGE 9 -->

Information Sciences 644 (2023) 119237
9
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Fig. 3. The ASR, APW, and AT on the SNLI dataset by attacking BERT using LS, PSO, and the GP2SO. To construct the substitute candidates, LS, PSO, and GP2SO all 
employ the HowNet.
Table 3
The attack success rate of the six attack methods on three datasets by attacking four victim 
models. The best results are highlighted in bold, and DisBERT is short for DistilBERT.
Dataset Victim AttackingSuccessRate(%)
Model TextFooler BEAT PWWS GA PSO GP 2SO
MR
CNN 86.98 88.02 94.01 88.67 96.48 96.48
DisBERT 76.14 78.91 85.85 85.71 91.81 91.81
BERT 67.90 64.68 81.15 82.72 91.65 91.65
RoBERTa 70.10 74.52 83.47 69.54 92.75 92.87
SST2
CNN 87.10 88.63 93.90 88.49 96.95 96.95
DisBERT 79.87 74.27 87.52 79.11 92.99 92.99
BERT 73.82 75.43 86.60 69.57 91.69 91.44
RoBERTa 71.46 72.68 84.63 68.90 92.32 92.07
QNLI
DisBERT 79.65 88.72 88.60 89.30 91.86 90.58
BERT 81.42 86.95 90.27 87.72 91.92 91.15
RoBERTa 73.61 85.39 85.61 79.50 89.09 88.22
Specifically, the proposed GP2SO outperforms static attacking methods (i.e., TextFooler, BEAT, PWWS) and the dynamic strategy 
(i.e., GA) by a large margin. Compared with PSO, the GP2SO also attains comparable performance, i.e., only lower by 0.3% on 
average. This validates that adapting the local optimal position is sufficient to guide very close attack performance to the global best 
position. Table4shows the experimental results of attacking time. As shown in Table4, the static methods, especially for TextFooler 
and PWWS, consume less time. Although BEAT belongs to a static attacking method, the exponential combination of sub-words leads 
to low time efficiency. Compared with heuristic algorithms PSO and GA, the GP2SO improves the average efficiency of attack time 
by 272% and 1085%, respectively. This strongly validates the superiority of the generation-based parallel strategy in time saving.
To evaluate the quality of adversarial examples, the SIM and PPL are calculated for 1000 adversarial sentences selected from 
MR and SST-2 datasets. These adversarial examples are generated by attacking BERT model, and results are given in Table 5. The 
results in Table 5 show that the GP2SO generates the most fluent adversarial examples and preserves the original semantics of 
input sentences to the greatest extent. These properties are significant in keeping human reader's decisions unchanged. Additionally, 
Table6lists the APW of various attack methods.

---


<!-- PAGE 10 -->

Information Sciences 644 (2023) 119237
10
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Table 4
The average time consuming of baselines and our GP2SO for attacking four victim models on 
three datasets.
Dataset Victim AttackingTime(seconds)
Model TextFooler BEAT PWWS GA PSO GP 2SO
MR
CNN 5.43 29.84 2.86 74.21 16.25 5.01
DisBERT 7.87 47.10 7.06 267.24 45.53 20.43
BERT 7.51 109.70 7.12 373.10 65.06 25.73
RoBERTa 6.19 87.70 6.55 152.98 62.15 20.50
SST2
CNN 5.42 22.57 2.82 73.22 13.68 3.58
DisBERT 6.75 34.59 5.43 122.58 35.26 14.58
BERT 7.03 103.45 5.84 410.25 46.72 17.60
RoBERTa 5.14 96.01 4.16 150.69 51.78 16.14
QNLI
DisBERT 9.31 40.88 11.71 192.08 156.88 71.50
BERT 10.06 27.19 15.95 295.93 232.79 99.29
RoBERTa 7.96 46.12 10.22 156.91 152.15 68.04
Table 5
Similarity and perplexity of the GP2SO and the five baselines on MR dataset. ↑and ↓indicate 
higher is better and lower is better, respectively.
Dataset TextFooler BEAT PWWS GA PSO GP 2SO
PPL ↓ MR 129.25 125.69 133.73 137.76 138.50 111.31
SST-2 112.22 114.02 125.17 130.94 130.41 99.62
SIM ↑ MR 0.84 0.82 0.84 0.84 0.82 0.85
SST-2 0.83 0.82 0.83 0.83 0.79 0.84
Table 6
The average number of perturbed words of various attack methods on three datasets by 
attacking the four victim models.
Dataset Victim AveragePerturbedWords(%)
Model TextFooler BEAT PWWS GA PSO GP 2SO
MR
CNN 13.26 17.44 13.14 16.25 16.10 11.56
DisBERT 15.02 17.93 13.85 18.45 17.53 12.24
BERT 15.92 19.22 14.51 16.59 18.00 12.11
RoBERTa 16.41 19.46 16.02 17.54 19.81 13.06
SST2
CNN 13.57 17.63 13.08 16.45 17.81 11.64
DisBERT 15.54 17.62 14.62 17.91 19.85 12.62
BERT 16.15 19.87 15.98 17.83 21.01 13.00
RoBERTa 17.21 19.46 16.58 19.24 21.64 13.57
QNLI
DisBERT 7.60 12.67 9.19 10.05 12.65 7.51
BERT 7.66 11.25 8.36 9.12 12.11 7.09
RoBERTa 7.40 11.72 9.22 8.79 12.77 7.39
These results show that the local best position is helpful to reduce the number of word replacements. The reason should be that 
multiple local best solutions provide more combinations than a single global best in one generation. Therefore, it is easier to get to 
the optimum and craft an adversarial sample. For qualitative comparison, several adversarial examples are listed in Table 7. The 
original sentence is correctly classified as positive by BERT, and only three attack algorithms (PWWS, PSO, and GP2SO) can produce 
a successful attack. Intuitively, the GP2SO can generate more natural adversarial text examples with fewer word perturbations 
compared with PWWS and PSO. Therefore, the proposed GP2SO generates high quality adversarial examples. Overall, the GP2SO 
achieves the highest or second-highest attack success rate and the lowest average perturbed words compared with the six baselines 
and it is the most efficient for the comparison of dynamic attacks. Furthermore, the semantic similarity and perplexity of the GP2SO 
are clearly superior to other baselines which shows that adversarial examples generated by the GP2SO achieve the highest quality.
5. Further study
In this section, we firstly conduct the adversarial training experiment to investigate if the adversarial examples crafted by the 
GP2SO are helpful to improve the models' robustness. Then, the transferability of adversarial examples generated by the GP2SO and 
the baselines are further verified.

---


<!-- PAGE 11 -->

Information Sciences 644 (2023) 119237
11
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Table 7
Adversarial example for intuitive comparison.
Original:Label →Positive(100%)
there's...tremendousenergyfromthecast,asenseofplayfulnessandexcitementthatseemsappropriate
BEAT:Positive(100%) →FAILED
TextFooler:Positive(100%) →FAILED
PWWS:Positive(100%) →Negative(98%)
there's...awfulget-up-and-gofromtheroll,asenseofplayfulnessandexcitementthatseemsappropriate.
GA:Positive(100%) →FAILED
PSO:Positive(100%) →Negative(100%)
there's...terriblezapfromtheproject,awarrantoffunandfunthatseemsvenal.
GP2SO:Positive(100%) →Negative(100%)
there's...strainedenergyfromthecast,asenseofplayfulnessandexcitementthatseemsvenal.
Table 8
The ASR and APW changes of various attack methods before and after adversarial training.
Attacking Beforeretraining Afterretraining △
Method ASR(%) APW(%) ASR(%) APW(%) ASR(%) APW(%)
TextFooler 70.94 17.01 65.80 20.51 -5.14 3.50
BEAT 70.20 23.24 66.40 22.25 -3.8 -0.99
PWWS 87.58 14.56 87.58 19.24 0 4.68
GA 78.36 17.68 76.00 23.24 -2.36 5.56
PSO 96.39 18.62 92.20 26.98 -4.19 8.36
GP2SO 95.99 11.13 89.20 16.27 -6.79 5.14
5.1. Adversarial training
Adversarial training is a typical strategy to enhance the immunity of the model, which trains the target model by joining the 
adversarial examples to the clean training set. To verify this, the BERT (base) model on MR dataset is fine-tuned and obtains 83.80% 
test accuracy as the victim model. Then 500 adversarial examples are added to the training set of the MR dataset for adversarial 
training. Following Zang etal.  [14], the changes of ASR are recorded before and after retraining, where larger ASR decrease signifies 
greater robustness improvement. Besides, the APW changes are also reported to demonstrate if the model becomes easier or harder 
to cheat after retraining. The more APW increase means the harder the victim model can be fooled. Table 8shows the adversarial 
training results of the GP2SO and the five counterparts. As shown in Table8, after the adversarial training, the GP2SO achieves the 
most ASR reduction (6.79%) with relatively more word modifications (5.14%). This indicates that the adversarial examples crafted 
by the GP2SO are effective in improving the model robustness.
5.2. Transferability
The transferability of an attack method usually means that the adversarial examples generated by fooling the victim model 𝐹1 can 
also mislead an unseen model 𝐹2. In this part, the BERT model is selected as the victim model, and 1000 adversarial examples are 
generated on the MR dataset. Then the transferability is evaluated by feeding them to three unknown models, i.e., CNN, DistilBERT, 
and Roberta. Fig.4shows the classification accuracy of various attack methods with and without the transfer attack. Note that the 
lower accuracy represents the higher transferability of adversarial examples. The results show that the proposed GP2SO generates 
adversarial examples with overall high transferability (second highest) compared with the five baselines.
5.3. Discussion on the uncertainty and sensitivity
The target label's prediction probability output of the victim model is the only information required for the GP2SO to craft text 
adversarial examples. Hence, the proposed GP2SO is still practicable when the victim model and dataset are unknown. The value 
of the fitness function in Eq. (3)i s altering with particle updating. The historical best position and the local best position will 
guide the updated particle to a higher fitness position which can easier mislead the victim model and the particle swarm converges 
gradually. Furthermore, the variance of attack results on different datasets and victim models are reported in Table 9 to validate 
the robustness of the GP2SO to tackle uncertainties, i.e., the text length and the structure of victim models. Intuitively, the proposed 
GP2SO is relatively robust compared with the five baselines in tackling uncertainties. Moreover, the swarm number 𝑁 and the 
positive constant 𝑚 are adjusted on the MR dataset to investigate the sensitivity of the GP2SO by attacking CNN. Fig. 5 shows the 
changes of ASR and APW with the change for computational parameters. The results show that the GP2SO is relatively sensitive

---


<!-- PAGE 12 -->

Information Sciences 644 (2023) 119237
12
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
Fig. 4. Transferability test on MR dataset by transferring the adversarial examples generated on BERT to other three unknown models, i.e., DistilBERT, RoBERTa, and 
CNN. 'NoAttack' denotes the test accuracy on original 1000 samples. Lower accuracy indicates higher transferability (the lower the better).
Table 9
The variance of ASR and APW on different datasets and victim models.
TextFooler BEAT PWWS GA PSO GP 2SO
ASR 38.16 60.47 14.91 60.73 4.5 5.65
APW 11.65 9.64 7.87 14.15 10.6 5.58
Fig. 5. The ASR and APW variation of the proposed GP2SO for attacking CNN model. The positive constant 𝑚(upper) and the swarm number 𝑁 (bottom) are justed 
on the MR dataset.

---


<!-- PAGE 13 -->

Information Sciences 644 (2023) 119237
13
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
when 10 <𝑚  <30 and 𝑁< 60. On the other hand, the stable trend of ASR and APW in Fig.5suggests the benign convergence for 
the GP2SO.
6. Conclusion
In this paper, a Generation-based Parallel Particle Swarm Optimization (GP2SO) is proposed to improve the text attack time 
efficiency while keeping the attack quality. The GP2SO utilizes HowNet to select sememe-consistency substitution candidates, which 
is helpful in keeping the semantic similarity. Then a generation-based P2SO is presented to optimize the word replacement priority, 
which is significant to make a successful attack with few word replacements. We evaluate the effectiveness of GP2SO by comparing 
it with representative baselines on popular text classification datasets. Experimental results show that the proposed GP2SO achieves 
the high attack success rate with the least word modifications. The generated adversarial sentences also show high quality in terms 
of semantic similarity and fluency. Besides, the GP2SO also exhibits superiorities in adversarial retraining and transfer attack experiments. Exploring efficient heuristic optimization algorithms and improving the robustness of deep learning models in the text 
domain are potential research directions.
CRediT authorship contribution statement
Xinghao Yang: Conceptualization, Methodology, Writing - review & editing. Yupeng Qi: Data curation, Software, Writing - 
original draft. Honglong Chen:Investigation, Visualization. Baodi Liu:Validation. Weifeng Liu:Supervision.
Declaration of competing interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to 
influence the work reported in this paper.
Data availability
The code is provide with a Github link.
Acknowledgements
This work was supported by the Natural Science Foundation of Qingdao, the National Natural Science Foundation of China (Grant 
No. 61671480), the Outstanding Youth Science Foundation Project of Shandong Province (Overseas) (Grant No. 2023HWYQ-070), 
and the Independent Innovation Research Project (Grant No. 22CX06059A).

## References

[1] N. Papernot, P. McDaniel, A. Swami, R. Harang, Crafting adversarial input sequences for recurrent neural networks, in: MILCOM 2016-2016 IEEE Military 
Communications Conference, IEEE, 2016, pp.49-54.
[2] J. Devlin, M.-W. Chang, K. Lee, K. Toutanova, BERT: pre-training of deep bidirectional transformers for language understanding, in: Proceedings of the 2019 
Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), 
Association for Computational Linguistics, Minneapolis, Minnesota, 2019, pp.4171-4186,  https://aclanthology .org /N19 -1423.
[3] A. Borjali, M. Magnéli, D. Shin, H. Malchau, O.K. Muratoglu, K.M. Varadarajan, Natural language processing with deep learning for medical adverse event 
detection from free-text medical narratives: a case study of detecting total hip replacement dislocation, Comput. Biol. Med. 129 (2021) 104140.
[4] E.G. Dada, J.S. Bassi, H. Chiroma, A.O. Adetunmbi, O.E. Ajibuwa, et al., Machine learning for email spam filtering: review, approaches and open research 
problems, Heliyon 5(6)  (2019) e01802.
[5] G. Varshney, M. Misra, P.K. Atrey, A survey and classification of web phishing detection schemes, Secur. Commun. Netw. 9(18)  (2016) 6266-6284.
[6] W.E. Zhang, Q.Z. Sheng, A. Alhazmi, C. Li, Adversarial attacks on deep-learning models in natural language processing: a survey, ACM Trans. Intell. Syst. 
Technol. 11(3)  (2020) 1-41.
[7] Y. Belinkov, Y. Bisk, Synthetic and natural noise both break neural machine translation, in: International Conference on Learning Representations, 2018.
[8] S. Eger, G.G. ¸Sahin, A. Rücklé, J.-U. Lee, C. Schulz, M. Mesgar, K. Swarnkar, E. Simpson, I. Gurevych, Text processing like humans do: visually attacking 
and shielding NLP systems, in: Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human 
Language Technologies, Volume 1 (Long and Short Papers), Association for Computational Linguistics, Minneapolis, Minnesota, 2019, pp.1634-1647,  https://
aclanthology .org /N19 -1165.
[9] K.-H. Huang, K.-W. Chang, Generating syntactically controlled paraphrases without using annotated parallel pairs, in: Proceedings of the 16th Conference of the 
European Chapter of the Association for Computational Linguistics: Main Volume, 2021, pp.1022-1033.
[10] M. Iyyer, J. Wieting, K. Gimpel, L. Zettlemoyer, Adversarial example generation with syntactically controlled paraphrase networks, in: Proceedings of the 2018 
Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), 2018, 
pp.1875-1885.
[11] M. Alzantot, Y. Sharma, A. Elgohary, B.-J. Ho, M. Srivastava, K.-W. Chang, Generating natural language adversarial examples, in: Proceedings of the 2018 
Conference on Empirical Methods in Natural Language Processing, 2018, pp.2890-2896.
[12] D. Jin, Z. Jin, J.T. Zhou, P. Szolovits, Is bert really robust? A strong baseline for natural language attack on text classification and entailment, in: Proceedings of 
the AAAI Conference on Artificial Intelligence, vol.34,  2020, pp.8018-8025.
[13] S. Ren, Y. Deng, K. He, W. Che, Generating natural language adversarial examples through probability weighted word saliency, in: Proceedings of the 57th 
Annual Meeting of the Association for Computational Linguistics, 2019, pp.1085-1097.
[14] Y. Zang, F. Qi, C. Yang, Z. Liu, M. Zhang, Q. Liu, M. Sun, Word-level textual adversarial attacking as combinatorial optimization, in: Proceedings of the 58th 
Annual Meeting of the Association for Computational Linguistics, 2020, pp.6066-6080.

---


<!-- PAGE 14 -->

Information Sciences 644 (2023) 119237
14
X .Y a n g ,Y .Q i ,H .C h e ne ta l .
[15] S. Garg, G. Ramakrishnan, BAE: BERT-based adversarial examples for text classification, in: Proceedings of the 2020 Conference on Empirical Methods in Natural 
Language Processing (EMNLP), 2020, pp.6174-6181.
[16] L. Li, R. Ma, Q. Guo, X. Xue, X. Qiu, BERT-ATTACK: adversarial attack against BERT using BERT, in: Proceedings of the 2020 Conference on Empirical Methods 
in Natural Language Processing (EMNLP), 2020, pp.6193-6202.
[17] J. Pennington, R. Socher, C. Manning, GloVe: global vectors for word representation, in: Proceedings of the 2014 Conference on Empirical Methods in Natural 
Language Processing (EMNLP), Association for Computational Linguistics, Doha, Qatar, 2014, pp.1532-1543,  https://aclanthology .org /D14 -1162.
[18] N. Mrkši´c, D.O. Séaghdha, B. Thomson, M. Gaši´c, L. Rojas-Barahona, P.-H. Su, D. Vandyke, T.-H. Wen, S. Young, Counter-fitting word vectors to linguistic 
constraints, in: The 15th Annual Conference of the North American Chapter of the Association for Computational Linguistics, 2016, pp.142-148.
[19] X. Yang, W. Liu, J. Bailey, D. Tao, W. Liu, Bigram and unigram based text attack via adaptive monotonic heuristic search, in: Proceedings of the AAAI Conference 
on Artificial Intelligence, vol.35,  2021, pp.706-714.
[20] J. Gao, J. Lanchantin, M.L. Soffa, Y. Qi, Black-box generation of adversarial text sequences to evade deep learning classifiers, in: 2018 IEEE Security and Privacy 
Workshops (SPW), 2018, pp.50-56.
[21] S. Liu, N. Lu, C. Chen, K. Tang, Efficient combinatorial optimization for word-level adversarial textual attack, IEEE/ACM Trans. Audio Speech Lang. Process. 30 
(2021) 98-111.
[22] J.Y. Yoo, J. Morris, E. Lifland, Y. Qi, Searching for a search method: benchmarking search algorithms for generating nlp adversarial examples, in: Proceedings 
of the Third BlackboxNLP Workshop on Analyzing and Interpreting Neural Networks for NLP, 2020, pp.323-332.
[23] S. Lalwani, H. Sharma, S.C. Satapathy, K. Deep, J.C. Bansal, A survey on parallel particle swarm optimization algorithms, Arab. J. Sci. Eng. 44 (4) (2019) 
2899-2923.
[24] L. Fu, Z. Ji, X.Y. Hu, N.A. Adams, Parallel fast-neighbor-searching and communication strategy for particle-based methods, Eng. Comput. (2019).
[25] A. Alouache, Parallel particle swarm optimization algorithm for classification of very high resolution images based on mathematical morphology, in: 2021 IEEE 
International Geoscience and Remote Sensing Symposium IGARSS, IEEE, 2021, pp.4952-4955.
[26] J.-Y. Li, Z.-H. Zhan, R.-D. Liu, C. Wang, S. Kwong, J. Zhang, Generation-level parallelism for evolutionary computation: a pipeline-based parallel particle swarm 
optimization, IEEE Trans. Cybern. 51(10)  (2021) 4848-4859.
[27] R. Socher, A. Perelygin, J. Wu, J. Chuang, C.D. Manning, A.Y. Ng, C. Potts, Recursive deep models for semantic compositionality over a sentiment treebank, in: 
Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, 2013, pp.1631-1642.
[28] B. Pang, L. Lee, Seeing stars: exploiting class relationships for sentiment categorization with respect to rating scales, in: Proceedings of the 43rd Annual Meeting 
of the Association for Computational Linguistics (ACL'05), 2005, pp.115-124.
[29] P. Rajpurkar, J. Zhang, K. Lopyrev, P. Liang, Squad: 100,000+ questions for machine comprehension of text, in: Proceedings of the 2016 Conference on Empirical 
Methods in Natural Language Processing, 2016, pp.2383-2392.
[30] S. Bowman, G. Angeli, C. Potts, C.D. Manning, A large annotated corpus for learning natural language inference, in: Proceedings of the 2015 Conference on 
Empirical Methods in Natural Language Processing, 2015, pp.632-642.
[31] V. Sanh, L. Debut, J. Chaumond, T. Wolf, Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter, preprint, arXiv :1910 .01108, 2019.
[32] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, V. Stoyanov, Roberta: a robustly optimized bert pretraining approach, 
preprint, arXiv :1907 .11692, 2019.
[33] J. Morris, E. Lifland, J.Y. Yoo, J. Grigsby, D. Jin, Y. Qi Textattack, A framework for adversarial attacks, data augmentation, and adversarial training in nlp, in: 
Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, 2020, pp.119-126.
[34] D. Cer, Y. Yang, S.-y. Kong, N. Hua, N. Limtiaco, R.S. John, N. Constant, M. Guajardo-Cespedes, S. Yuan, C. Tar, et al., Universal sentence encoder, preprint, 
arXiv :1803 .11175, 2018.
[35] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever, Language models are unsupervised multitask learners, OpenAI Blog 1(8)  (2019) 9.
