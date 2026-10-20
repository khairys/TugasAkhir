---
title: "Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments"
slug: "12_finetuning_indobert_gambling_social_media"
authors: "IJECSA Research Team"
year: 2026
venue: "International Journal of Engineering and Computer Science Applications (IJECSA), Vol. 5, No. 2, pp. 107–116"
doi: "10.30812/ijecsa.v5i2.xxxx"
category: "Online Gambling (Judol) Detection"
tags: ["indobert", "fine-tuning", "online-gambling", "social-media-comments", "hyperparameters"]
total_pages: 10
character_count: 32978
word_count: 4614
source_file: "Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments.pdf"
extraction_date: "2026-10-20 15:10:06"
---

# Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments

## Metadata & Bibliographic Overview
- **Authors:** IJECSA Research Team
- **Publication Year:** 2026
- **Venue / Journal:** International Journal of Engineering and Computer Science Applications (IJECSA), Vol. 5, No. 2, pp. 107–116
- **DOI / Link:** 10.30812/ijecsa.v5i2.xxxx
- **Category:** Online Gambling (Judol) Detection
- **Original Source File:** `Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments.pdf` (10 pages, ~4,614 words)

## Agent Quick-Scan / Executive Takeaways
> [!NOTE]
> **Relevance to Tugas Akhir / Research Context:**
> Direct guidance for fine-tuning IndoBERT on Indonesian online gambling comments. Validates the training hyperparameters and classification head configuration used in Stage 9 IndoBERT baseline.

### Key Thematic Dimensions
- **Domain:** Online Gambling (Judol) Detection
- **Methodology Focus:** indobert, fine-tuning, online-gambling, social-media-comments, hyperparameters
- **Relevance Anchors in Repo:** Connects to Stage 8 (Data Leakage & Pairing), Stage 9 (Baseline Models), Stage 10 (Adversarial Robustness O1-O4), and Stage 11 (Domain Shift OOD).

---

# Full Extracted Document Text



<!-- PAGE 1 -->

International Journal of Engineering and Computer Science Applications (IJECSA)
V ol. 5, No. 2, September 2026, pp. 107∼116
ISSN: 2828-5611
DOI: 10.30812/IJECSA.v5i2.6664 107
Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in
Indonesian-Language Social Media Comments
Yuri Ariyanto1, Deddy Kusbianto Purwoko Aji1, Chandrasena Setiadi1, Yan Watequlis Syaifudin1, Anggrean Renozonarca2
1Politeknik Negeri Malang, Malang, Indonesia
2Lintas Jejak Nusaraya, Malang, Indonesia
Article Info
Article history:
Received July 14, 2026
Revised August 10, 2026
Accepted September 2, 2026
Keywords:
IndoBERT
Online Gambling Detection
Natural Language Processing
Text Classification
Transformer Fine-Tuning

## Abstract

Online gambling promotion increasingly infiltrates Indonesian social media comments through slang,
misspellings, and character substitutions that slip past keyword filters; these contextual and semantic variations are not captured by static keyword lists and classical term frequency-inverse document
frequency (TF-IDF) classifiers. The aim of this research is to build a text classification model that
automatically distinguishes gambling-related comments from non-gambling ones by fine-tuning IndoBERT, a transformer language model pretrained on a large Indonesian corpus, with a preprocessing
pipeline designed to normalize disguised gambling terminology. This research method is a supervised
fine-tuning approach applied to 10,230 labeled Indonesian YouTube comments from a public Kaggle
repository, split via stratified sampling into 70% training, 15% validation, and 15% testing; the text
is cleaned, case-folded, and normalized to reverse character substitutions, then tokenized with a maximum length of 128 and used to fine-tune the model for up to 3 epochs with an early stopping rule
monitoring validation accuracy. The results of this research are an accuracy of 98.44%, a precision of
98.56%, a recall of 97.63%, and an F1-score of 98.09% for the gambling class, with a macro-average
F1-score of 98.38% on the held-out test set. These findings indicate that IndoBERT's bidirectional
self-attention mechanism effectively detects disguised gambling promotion in informal Indonesian
YouTube comments, and suggest that such a normalization-aware pipeline could support automated
content moderation on Indonesian social media, pending further validation across other platforms and
datasets.
Copyright ©2026 The Authors.
This is an open access article under the CC BY-SA license.
Corresponding Author:
Yuri Ariyanto,
Politeknik Negeri Malang, Malang, Indonesia,
Email: yuri@polinema.ac.id
How to Cite:Y . Ariyanto, D. K. P. Aji, C. Setiadi, Y . W. Syaifudin, & A. Renozonarca, "Fine-Tuning IndoBERT for Detecting
Online Gambling Promotion in Indonesian-Language Social Media Comments,"International Journal of Engineering and Computer
Science Applications (IJECSA), vol. 5, no. 2, pp. 107-116, Sep. 2026. doi: 10.30812/ijecsa.v5i2.6664.
Journal homepage:https://journal.universitasbumigora.ac.id/index.php/ijecsa

---


<!-- PAGE 2 -->

108 ISSN: 2828-5611

## 1. Introduction

Internet penetration in Indonesia continues to grow, and digital technology adoption follows the same trend. This growth brings
a serious side effect: online gambling promotion, known locally as "judi online", now spreads across social media platforms, comment sections, and instant-messaging channels [1]. Perpetrators disguise these advertisements using slang, symbols, and deliberate
misspellings, often replacing letters with numbers to evade simple keyword filters [2]. Traditional content moderation systems rely
on static keyword matching, so they cannot read the real meaning hidden behind an altered sentence. Earlier research has tackled
this problem using classical machine learning methods. Study [3] combined term frequency-inverse document frequency (TF-IDF)
representation with Random Forest, Logistic Regression, and Convolutional Neural Networks (CNN) to detect gambling promotion
on Indonesian Twitter, and the TF-IDF-Random Forest combination reached a recall of 0.958 and a precision of 0.966. TF-IDF,
however, only counts word frequency and ignores word order and context [4]. This weakness makes such models vulnerable to
obfuscated or informally written text. Researchers have therefore turned to hybrid architectures that combine BERT-style representations with recurrent layers such as Bidirectional Long Short-Term Memory (BiLSTM) or Bidirectional Gated Recurrent Unit
(BiGRU) for Indonesian text classification, and these hybrid models generally outperform purely statistical baselines [5].
Pretrained transformer models have changed this picture in recent years. Bidirectional Encoder Representations from Transformers (BERT) and its Indonesian variant, IndoBERT, now outperform earlier methods across many Indonesian NLP tasks. Researchers have applied IndoBERT to hoax and fake-news detection [6], hate-speech identification [7], aspect-based sentiment analysis [8], toxic-comment multilabel classification [9], and multilabel classification of customer reviews [10]. Its bidirectional selfattention mechanism connects every word to every other word in a sentence regardless of position, so the model can catch semantically
disguised gambling promotion that keyword filters and shallow classifiers usually miss.
Several studies are closely related to the present work. Study [11, 12] fine-tuned IndoBERT on Indonesian YouTube comments
and reported 98.26% accuracy for online gambling promotion detection, a result numerically close to the 98.44% accuracy obtained
in this study; this narrow margin indicates that the present work extends, rather than substantially surpasses, the accuracy already
achieved by closely related research. Study [3] built a text mining pipeline to detect gambling advertisements on Indonesian Twitter,
while Study [1] applied semi-supervised IndoBERT classification to Indonesian YouTube comments, raising accuracy from 0.953
with labeled data alone to 0.986 after pseudo labeling the unlabeled portion of the dataset. Study [2] extended this line of work
into the visual domain, detecting hidden gambling promotion embedded in watermarked advertising images through a cross-modal
attention framework. Most existing studies, however, either rely on classical pipelines that struggle with spelling obfuscation or
apply IndoBERT without a preprocessing step tailored to disguised spellings such as "sl0t", "c4sino", and "m4xwin". The present
study's distinguishing element is therefore this preprocessing step rather than a claim of superior raw accuracy, though its individual
contribution has not yet been isolated through a controlled ablation study comparing the pipeline with and without word-variation
normalization.
Previous work has overlooked some gaps, such as a preprocessing step that normalizes disguised spellings (e.g., "sl0t",
"c4sino") and a controlled evaluation of its individual contribution. The difference between this research and the previous one is
that this study integrates obfuscation-aware normalization directly into the IndoBERT fine-tuning pipeline and pairs it with a perclass, confusion-matrix-based error analysis. The objective of this research is to build and evaluate a fine-tuned IndoBERT model,
based on the pretrainedindolem/indobert-base-uncasedcheckpoint, on 10,230 labeled Indonesian YouTube comments, using accuracy, precision, recall, F1-score, and confusion matrix analysis. The contribution of this research to the development of science lies in
this normalization-aware pipeline and its transparent per-class error analysis, which can inform future automated content moderation
systems for Indonesian-language social media. Section 2 explains the theory behind IndoBERT; Section 3 describes the dataset and
training method; Section 4 reports the experimental results; and Section 5 concludes the paper.
2. RESEARCH METHOD
2.1. Indobert Algorithm
IndoBERT builds on the BERT architecture and is pretrained on a large Indonesian-language corpus [6, 13]. This pretraining
enables IndoBERT to capture Indonesian linguistic traits, including regional word variation, more accurately than multilingual models [14-16]. Unlike older recurrent models, IndoBERT processes the entire input sequence in parallel via a self-attention mechanism;
every token attends to every other token, and this design yields a genuinely bidirectional representation [17, 18]. Four computational
stages together explain this encoding process.
International Journal of Engineering and Computer Science Applications (IJECSA)
V ol. 5, No. 2, September 2026: 107 - 116

---


<!-- PAGE 3 -->

International Journal of Engineering and Computer Science Applications (IJECSA) 109
1. Token Embedding and Positional Encoding
Each input token is first converted into a numerical vector representation. The model builds this vector by summing three
embedding types for every token: word embedding, position embedding, and segment embedding, as Equation (1) shows. The
resulting 768-dimensional vector, formed by this summation, constitutes the representation subsequently passed to the encoder layers.
Ei=Etoken+Eposition+Esegment(1)
2. Multi-Head Self-Attention
After embedding, the model computes token relationships via scaled dot-product self-attention, as shown in Equation (2). In
this formula,Q,K, andVrepresent the query, key, and value matrices, andd k denotes the dimension of the key vectors. IndoBERT
extends this idea through multi-head attention: it runs the attention operation in parallel acrosshseparate heads, as Equation (3)
shows. This parallel design lets each of the 12 encoder layers capture a different kind of contextual relationship, and the resulting
representations grow more abstract and more informative as they move through deeper layers.
Attention(Q, K, V) = softmax
(︄
QK T
√dk
)︄
V(2)
M ultiHead(Q, K, V) = Concat (head 1, . . . , headh)W O (3)
3. Feed-Forward Network
Following the attention sub-layer, each token representation undergoes an additional, independent transformation via a positionwise feed-forward network, as defined in Equation (4). This network applies the same non-linear transformation to every token
position, using the shared parametersW 1,b 1,W 2, andb 2, and it lets the model learn deeper and more complex feature interactions.
F F N(x) = max (0, xW 1 +b 1)W 2 +b 2 (4)
4. Classification Output
Once the input sequence passes through all 12 encoder layers, the model reads the hidden-state vector attached to the special
classification token [CLS], which sits at the front of every input sequence, and this vector represents the entire sentence. A pooling
layer and a linear classification layer with softmax activation then process this vector, as shown in Equation (5). Here,hCLS denotes the
final-layer hidden state of the [CLS] token, andyrepresents the predicted probability distribution over the target classes, namely "judi"
(gambling) and "non judi" (non-gambling). Section 3 builds its fine-tuning procedure directly on this classification mechanism [19].
y= softmax
(︁
W·h [CLS] +b
)︁
(5)
The methodology adopted in this study follows a supervised fine-tuning workflow comprising five principal stages: dataset collection,
text preprocessing, tokenization, model fine-tuning, and model evaluation, as depicted in Figure 1.
Figure 1. Research stages for fine-tuning IndoBERT
2.2. Dataset
This study draws on a publicly available Indonesian-language dataset named "judionline", obtained from Kaggle [20], which
contains 10,230 Indonesian YouTube comments labeled into two categories: "judi" (gambling-related) and "nonjudi" (non-gambling).
These labels were inherited exactly as distributed by the dataset's original publisher rather than produced by the present authors;
consequently, the number of annotators, the annotation guidelines, the procedure used to resolve labeling disagreements, and any
inter-annotator agreement score are not documented by the publisher and cannot be reported here-a limitation that follows directly
International Journal of Engineering and Computer Science Applications (IJECSA)

---


<!-- PAGE 4 -->

110 ISSN: 2828-5611
from relying on a secondary, pre-labeled dataset rather than conducting first-party annotation. To preserve consistent class proportions across all subsets, the dataset was partitioned via stratified sampling into 70% for training (7,161 samples), 15% for validation
(1,534 samples), and 15% for testing (1,535 samples), which together account for the full 10,230 comments, as illustrated in Figure 2.
This stratified approach was adopted specifically to prevent the model from developing a bias toward the majority class.
With respect to ethical use of the data, all comments were already publicly visible on YouTube at the time of collection;
no additional personal information beyond what commenters had already made public was gathered, and no attempt was made to
further identify, contact, or de-anonymize individual commenters. Usernames retained in the dataset appear exactly as published
by the original commenters and were neither altered nor cross-referenced by the authors. The dataset is distributed under Kaggle's
standard public-dataset terms of use [20], and the word-variation normalization dictionary, the preprocessing scripts, and the trained
model checkpoint developed for this study are available from the corresponding author upon reasonable request for academic, noncommercial use.
Figure 2. Dataset split into training, validation, and testing subsets
2.3. Text Preprocessing
Every comment passes through three preprocessing steps before tokenization, applied in a fixed order so that each step receives
the input it depends on. The first step, text cleaning, removes URLs, mentions, hashtags, emojis, and punctuation, and applies Unicode
normalization; it targets only non-alphanumeric symbols and deliberately leaves digits embedded within word tokens untouched,
since the third step depends on detecting them. The second step, case folding, converts all text to lowercase, preventing the model from
treating capitalization variants such as "slot", "SLOT", and "slot" as separate tokens. The third step, word-variation normalization,
runs after case folding and targets the digit-for-letter substitutions common in disguised gambling terms, converting forms such as
"sl0t", "c4sino", and "m4xwin" into "slot", "casino", and "maxwin" through a mapping dictionary and regular expression matching;
any digit that does not match a known substitution pattern is discarded at the end of this step. Table 1 shows an example of this
three-step pipeline.
Table 1. Example of Text Preprocessing Stages
Stage Input Output
Text cleaning "Daftar SEKARANG!!! @SlotGacor #Maxwin 100%
 " "Daftar SEKARANG SlotGacor Maxwin"
Case folding "Daftar SEKARANG SlotGacor Maxwin" "daftar sekarang slotgacor maxwin"
Word-variation normalization "sl0t", "c4sino", "m4xwin", "t0gel" "slot", "casino", "maxwin", "togel"
After normalization, the AutoTokenizer from the pretrainedindolem/indobert-base-uncasedmodel tokenizes the cleaned text.
The tokenizer adds the special tokens [CLS] and [SEP] to the start and end of each sequence, and padding and truncation ensure that
every sequence is fixed to a maximum length of 128 tokens. The process also produces an attention mask alongside the token IDs,
where a value of 1 indicates a real token, and a value of 0 indicates a [PAD] token that the model should ignore.
International Journal of Engineering and Computer Science Applications (IJECSA)
V ol. 5, No. 2, September 2026: 107 - 116

---


<!-- PAGE 5 -->

International Journal of Engineering and Computer Science Applications (IJECSA) 111
2.4. IndoBERT Model Architecture
The classification model loads the pretrainedindobert-base-uncasedcheckpoint through the AutoModelForSequenceClassification class, and this configuration supports binary classification with two output labels: "judi" and "non judi". Figure 3 shows the
full architecture. A BertEmbeddings layer first maps each token into a 768-dimensional vector, drawing from a vocabulary of 31,923
subword tokens across a maximum position range of 512. Twelve stacked BertEncoder layers, a BertPooler layer (a768×768linear
transformation with Tanh activation), and a final linear classification layer complete the architecture. This study experimentally evaluates only the fine-tuned IndoBERT configuration described above; no keyword filtering, TF-IDF-based, or other classical machine
learning baselines were implemented or retrained on the same dataset and split for direct comparison. Accordingly, the performance
figures attributed to such methods elsewhere in this paper are drawn from results reported in the cited literature on their own respective datasets, and any comparison against those figures should be read as an indicative reference point rather than a controlled,
dataset-matched benchmark; establishing such a baseline is identified as a direction for future work.
Figure 3. IndoBERT model architecture used for binary text classification
2.5. Fine-Tuning Configuration
Fine-tuning runs on the training subset for a maximum of 3 epochs. At the end of each epoch, the model evaluates itself on
the validation subset, and this step continuously tracks its progress. An early stopping mechanism with a patience of 2 epochs was
configured to guard against overfitting, monitoring validation accuracy and automatically halting training whenever no improvement
was observed for 2 consecutive epochs. Because the total training schedule was capped at 3 epochs, this patience setting left only
a narrow window in which the mechanism could actually trigger, a configuration choice that is acknowledged here as a limitation
rather than a fully validated stopping criterion. Table 2 reports the training loss, validation loss, and validation accuracy recorded at
the end of each epoch: validation loss reached its lowest value after epoch 1 and rose slightly thereafter, while validation accuracy
continued to improve through epoch 3, a divergence consistent with the onset of mild overfitting that the chosen patience window
was too narrow to fully characterize.
Table 2. Training and Validation Metrics Logged Epoch
Epoch Training Loss Validation Loss Validation Accuracy
1 0.2274 0.0888 97.33%
2 0.0830 0.1047 97.78%
3 0.0331 0.1011 98.17%
2.6. Evaluation Metrics
The testing subset provides the basis for model evaluation, and a confusion matrix, together with four standard metrics, measures performance: accuracy, precision, recall, and F1-score. Equations (6) through (9) define these four metrics. In these formulas,
T P,T N,F P, andF Ncorrespond to the counts of true positive, true negative, false positive, and false negative predictions, respecInternational Journal of Engineering and Computer Science Applications (IJECSA)

---


<!-- PAGE 6 -->

112 ISSN: 2828-5611
tively, with the "judi" class designated as the positive class.
Accuracy= T P+T N
T P+T N+F P+F N (6)
P recision= T P
T P+F P (7)
Recall= T P
T P+F N (8)
F1−Score= 2× (P recision x Recall)
(P recision+Recall) (9)
3. RESULT AND ANALYSIS
The findings of this research are organized across 3 subsections: Section 4.1 reports the confusion matrix obtained on the
held-out testing subset, Section 4.2 derives the corresponding evaluation metrics from that matrix, and Section 4.3 discusses these
findings in light of related work. The results of this research are in line with, or supported by, prior state-of-the-art studies that
applied IndoBERT and comparable transformer-based approaches to Indonesian gambling promotion and related text classification
tasks; Section 4.3 examines this alignment in detail, along with the observed error patterns and the limitations that qualify these
findings.
3.1. Confusion Matrix
The testing subset contains 1,535 samples: 903 "non judi" comments and 632 "judi" comments. The fine-tuned IndoBERT
model classifies all 1,535 samples, and Table 3 reports the resulting confusion matrix. Figure 4 visualizes the same matrix as a
heatmap.
Table 3. Confusion Matrix of the Fine-Tuned IndoBERT Model
Analysis Predicted Gambling Predicted Non-Gambling
Actual Gambling 617 (TP) 15 (FN)
Actual Non-Gambling 9 (FP) 894 (TN)
Figure 4. Confusion matrix heatmap of the IndoBERT model on the testing subset
3.2. Evaluation Metrics
Table 3 shows the values of the confusion matrix; Equations (6)-(9) transform these values into the 4 evaluation metrics.
The resulting scores are summarized in Table 4 and Figure 5. Figure 5 shows the 5 important metrics from Table 4 as a bar chart,
providing an overview of the overall performance profile at a glance. The 5 bars are tightly clustered in a narrow band from about
97.6% to 98.6%. This suggests that the model is performing well across accuracy, precision, recall, and F1-score, not just in one
dimension. The bottom-most bar represents the gambling class recall at 97.63%, the lowest recall figure, indicating a slight residual
International Journal of Engineering and Computer Science Applications (IJECSA)
V ol. 5, No. 2, September 2026: 107 - 116

---


<!-- PAGE 7 -->

International Journal of Engineering and Computer Science Applications (IJECSA) 113
gap in detecting all true gambling comments. The other 4 bars are all above 98%. The close grouping and the macro-average F1-score
being close to the individual class-level F1-scores visually validate that the model's strong performance is not biased toward any one
metric or class but is uniformly distributed across classes.
Table 4. Evaluation Results of the Fine-Tuned IndoBERT Model
No. Metric Value Interpretation
1 Accuracy 98.44% The model correctly classified 1,511 of 1,535 testing comments into their true category.
2 Precision (Non-Gambling) 98.35% Of comments predicted as non-gambling, 98.35% truly were
non-gambling; the rest were missed gambling comments.
3 Precision (Gambling) 98.56% Of comments flagged as gambling, 98.56% truly were gambling, keeping false alarms low.
4 Recall (Non-Gambling) 99.00% The model correctly identified 99.00% of all actual nongambling comments, missing about 1%.
5 Recall (Gambling) 97.63% The model caught 97.63% of all actual gambling comments,
missing roughly 2.4%.
6 F1-Score (Non-Gambling) 98.68% A balanced precision-recall score for the non-gambling class,
confirming consistently strong performance.
7 F1-Score (Gambling) 98.09% A balanced precision-recall score for the gambling class, the
primary class of interest.
8 Macro Avg F1-Score 98.38% The unweighted average of both F1-scores, confirming strong
performance is not driven by class imbalance.
Figure 5. Evaluation performance of the fine-tuned IndoBERT model
3.3. Discussion
The accuracy of the IndoBERT model after fine-tuning is 98.44%. This score indicates that the model correctly classifies 1,511
out of 1,535 test samples. The precision for the "judi" class is 98.56%, indicating that most comments predicted as gambling-related
are actually gambling-related. The result maintains a low false-positive rate, protecting valid users from unwarranted disturbances.
The model was capable of retrieving almost all real gambling comments in the test data, achieving a recall of 97.63%. The 2 metrics
give an F1-score of 98.09% for the "judi" class, and a macro-average F1-score of 98.38%. Both numbers indicate a relatively balanced
performance of the model across the 2 classes, at least on this 1 test split.
The numerical results are similar to those of study [11], which reported 98.26% accuracy for IndoBERT on a similar task of
identifying online gambling promotions in Indonesian YouTube comments. This closeness, despite variations in dataset composition,
is consistent with, but not proof of, the assertion that IndoBERT does a reasonable job of detecting gambling in Indonesian. Classical
machine learning approaches, such as TF-IDF combined with Random Forest, for detecting gambling promotion on Twitter achieved
a precision of 0.966 and a recall of 0.958 on a different dataset [13], which are close to but not higher than the metrics achieved in this
study. This comparison is based on a different dataset and has not been re-run under the same experimental conditions as this study; it
International Journal of Engineering and Computer Science Applications (IJECSA)

---


<!-- PAGE 8 -->

114 ISSN: 2828-5611
should therefore be interpreted as an indicative reference point rather than a controlled benchmark. Similarly, study [1] found that in
a semi-supervised setting, IndoBERT alone achieved an accuracy of 0.953, and when combined with pseudo-labeled data, it achieved
an accuracy of 0.986, which is consistent with the fact that transformer-based models benefit from richer training signals, but again
in a separate experimental setup.
The confusion matrix is shown in Table 3, where 9 false positives and 15 false negatives are observed from 1,535 testing
samples. Recall of the "non judi" class is a little higher (99.00%) than recall of the "judi" class (97.63%). This may be because
there are more samples in the "non judi" testing subset (903) than in the "judi" testing subset (632), or because the model has more
knowledge of non-gambling language structures. We have not statistically isolated this observation and cannot exclude alternative
explanations. Future work can explore this gap further, e.g., by using class-balancing techniques such as minority-class oversampling
or class-weighted loss functions. The low overall error rate is consistent with the preprocessing pipeline that normalizes disguised
gambling terms prior to tokenization and supports IndoBERT's self-attention mechanism in detecting disguised promotional content.
One limitation is that the study only reports aggregate counts of false positives and false negatives but not a qualitative inspection of
individual misclassified comments.
4. CONCLUSION
This study fine-tunes the IndoBERT algorithm, specifically theindolem/indobert-base-uncasedcheckpoint, to detect online
gambling promotion hidden inside informal Indonesian-language social media comments. The proposed model pairs a preprocessing
pipeline built for obfuscated gambling terminology with IndoBERT's bidirectional self-attention mechanism, and this combination
delivers strong classification performance on a 1,535-sample testing subset: 98.44% accuracy, 98.56% precision, 97.63% recall, and
a 98.09% F1-score for the gambling class, alongside a 98.38% macro-average F1-score. These results confirm that transformer-based
contextual representations outperform static keyword filtering by a clear margin, and they match or exceed the classical machine
learning baselines reported in related studies. Future work could narrow the class imbalance between the "judi" and "non judi"
categories through oversampling or class-weighted training, and could enhance the model's robustness by incorporating additional
obfuscation patterns, multi-platform datasets, and real-time deployment for continuous content moderation.
ACKNOWLEDGEMENTS
The authors thank the Ministry of Higher Education, Science, and Technology of Indonesia, Politeknik Negeri Malang, and
its Research and Community Service Center for the financial support and laboratory facilities. Special thanks are also given to the
Applied Informatics Laboratory for the technical infrastructure and academic support that was critical to the success of this research.

## References

[1] S. P. Santika et al., "Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification,"Procedia Computer Science, vol. 269, pp. 1269-1278, 2025.DOI: 10.1016/j.procs.2025.09.068
[2] A. A. Ajhari et al., "A cross-modal attention for detecting hidden online gambling promotion in multilingual multimodal
watermarked advertising images,"Journal of King Saud University Computer and Information Sciences, vol. 38, no. 5, p. 313,
Jul. 2026.DOI: 10.1007/s44443-026-00725-3
[3] R. B. Perdana et al., "Detecting Online Gambling Promotions on Indonesian Twitter Using Text Mining Algorithm,"International Journal of Advanced Computer Science and Applications, vol. 15, no. 8, 2024.DOI: 10.14569/IJACSA.2024.0150893
[4] E. D. Madyatmadja, B. N. Yahya, and C. Wijaya, "Contextual Text Analytics Framework for Citizen Report Classification: A
Case Study Using the Indonesian Language,"IEEE Access, vol. 10, pp. 31 432-31 444, 2022.DOI: 10.1109/ACCESS.2022.
3158940
[5] H. Ahmadian et al., "Hybrid Models for Emotion Classification and Sentiment Analysis in Indonesian Language,"Applied
Computational Intelligence and Soft Computing, vol. 2024, no. 1, A. Haldorai, Ed., p. 2 826 773, Jan. 2024.DOI: 10.1155/
2024/2826773
[6] D. Y . Yefferson, V . Lawijaya, and A. S. Girsang, "Hybrid model: IndoBERT and long short-term memory for detecting Indonesian hoax news,"IAES International Journal of Artificial Intelligence (IJ-AI), vol. 13, no. 2, p. 1913, Jun. 1, 2024.DOI:
10.11591/ijai.v13.i2.pp1913-1924
International Journal of Engineering and Computer Science Applications (IJECSA)
V ol. 5, No. 2, September 2026: 107 - 116

---


<!-- PAGE 9 -->

International Journal of Engineering and Computer Science Applications (IJECSA) 115
[7] P. A. Mufva et al., "Performance comparison of deep learning approaches for Indonesian twitter hate speech detection using
IndoBERTweet embedding,"Procedia Computer Science, vol. 269, pp. 1663-1671, 2025.DOI: 10.1016/j.procs.2025.09.109
[8] A. Jazuli, Widowati, and R. Kusumaningrum, "Optimizing Aspect-Based Sentiment Analysis Using BERT for Comprehensive
Analysis of Indonesian Student Feedback,"Applied Sciences, vol. 15, no. 1, p. 172, Dec. 28, 2024.DOI: 10.3390/app15010172
[9] G. Z. Nabiilah et al., "Indonesian multilabel classification using IndoBERT embedding and MBERT classification,"International Journal of Electrical and Computer Engineering (IJECE), vol. 14, no. 1, p. 1071, Feb. 1, 2024.DOI: 10.11591/ijece.
v14i1.pp1071-1078
[10] N. K. Nissa and E. Yulianti, "Multi-label text classification of Indonesian customer reviews using bidirectional encoder representations from transformers language model,"International Journal of Electrical and Computer Engineering (IJECE),
vol. 13, no. 5, p. 5641, Oct. 1, 2023.DOI: 10.11591/ijece.v13i5.pp5641-5652
[11] K. Kamdan et al., "Performance Analysis of IndoBERT for Detection of Online Gambling Promotion in YouTube Comments,"
inThe 7th International Global Conference Series on ICT Integration in Technical Education &amp; Smart Society, MDPI,
Sep. 2, 2025, p. 66.DOI: 10.3390/engproc2025107066
[12] Y . D. Novandian et al., "IndoBERT-based Indonesian Cyberbullying Detection with Multi-stage Labeling," in2024 International Seminar on Application for Technology of Information and Communication (iSemantic), Semarang, Indonesia: IEEE,
Sep. 21, 2024, pp. 515-521.DOI: 10.1109/iSemantic63362.2024.10762553
[13] A. Bello, S.-C. Ng, and M.-F. Leung, "A BERT Framework to Sentiment Analysis of Tweets,"Sensors, vol. 23, no. 1, p. 506,
Jan. 2, 2023.DOI: 10.3390/s23010506
[14] A. Riyadi et al., "IndoGovBERT: A Domain-Specific Language Model for Processing Indonesian Government SDG Documents,"Big Data and Cognitive Computing, vol. 8, no. 11, p. 153, Nov. 9, 2024.DOI: 10.3390/bdcc8110153
[15] D. G. Mandhasiya, H. Murfi, and A. Bustamam, "The hybrid of BERT and deep learning models for Indonesian sentiment
analysis,"Indonesian Journal of Electrical Engineering and Computer Science, vol. 33, no. 1, p. 591, Jan. 1, 2024.DOI:
10.11591/ijeecs.v33.i1.pp591-602
[16] F. Muftie and M. Haris, "IndoBERT Based Data Augmentation for Indonesian Text Classification," in2023 International
Conference on Information Technology Research and Innovation (ICITRI), Jakarta, Indonesia: IEEE, Aug. 16, 2023, pp. 128132.DOI: 10.1109/ICITRI59340.2023.10250061
[17] J. Yang et al., "An Empirical Analysis of Text Segmentation for BERT Classification in Extended Documents," in2023
IEEE International Conference on Big Data (BigData), Sorrento, Italy: IEEE, Dec. 15, 2023, pp. 2793-2797.DOI: 10.1109/
BigData59044.2023.10386783
[18] C. Eang and S. Lee, "Improving the Accuracy and Effectiveness of Text Classification Based on the Integration of the Bert
Model and a Recurrent Neural Network (RNN Bert Based),"Applied Sciences, vol. 14, no. 18, p. 8388, Sep. 18, 2024.DOI:
10.3390/app14188388
[19] N. J. Prottasha et al., "Transfer Learning for Sentiment Analysis Using BERT Based Supervised Fine-Tuning,"Sensors, vol. 22,
no. 11, p. 4157, May 30, 2022.DOI: 10.3390/s22114157
[20] Yaemico,Judi Online: Indonesian Online Gambling Promotion at YouTube Dataset, Kaggle, 2023.
International Journal of Engineering and Computer Science Applications (IJECSA)

---


<!-- PAGE 10 -->

116 ISSN: 2828-5611
[This page intentionally left blank.]
International Journal of Engineering and Computer Science Applications (IJECSA)
V ol. 5, No. 2, September 2026: 107 - 116
