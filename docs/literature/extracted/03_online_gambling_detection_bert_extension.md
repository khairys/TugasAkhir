---
title: "An Intelligent System for Detecting Online Gambling Promotion on Social Media Based on BERT and Adaptive Browser Extension"
slug: "03_online_gambling_detection_bert_extension"
authors: "Gilbert F. Situmorang, et al."
year: 2025
venue: "Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), Vol. 14, No. 3, pp. 679-691"
doi: "10.29207/resti.v14i3.xxxx"
category: "Online Gambling (Judol) Detection"
tags: ["online-gambling", "judol", "indonesian-social-media", "bert", "browser-extension"]
total_pages: 13
character_count: 49015
word_count: 6756
source_file: "AN INTELLIGENT SYSTEM FOR DETECTING ONLINE GAMBLING PROMOTION ON SOCIAL MEDIA BASED ON BERT AND ADAPTIVE BROWSER EXTENSION.pdf"
extraction_date: "2026-10-20 15:09:53"
---

# An Intelligent System for Detecting Online Gambling Promotion on Social Media Based on BERT and Adaptive Browser Extension

## Metadata & Bibliographic Overview
- **Authors:** Gilbert F. Situmorang, et al.
- **Publication Year:** 2025
- **Venue / Journal:** Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), Vol. 14, No. 3, pp. 679-691
- **DOI / Link:** 10.29207/resti.v14i3.xxxx
- **Category:** Online Gambling (Judol) Detection
- **Original Source File:** `AN INTELLIGENT SYSTEM FOR DETECTING ONLINE GAMBLING PROMOTION ON SOCIAL MEDIA BASED ON BERT AND ADAPTIVE BROWSER EXTENSION.pdf` (13 pages, ~6,756 words)

## Agent Quick-Scan / Executive Takeaways
> [!NOTE]
> **Relevance to Tugas Akhir / Research Context:**
> Direct state-of-the-art prior work focusing on Indonesian online gambling (judol) promotion on social media using BERT. Demonstrates real-world deployment challenges and the need for high inference precision.

### Key Thematic Dimensions
- **Domain:** Online Gambling (Judol) Detection
- **Methodology Focus:** online-gambling, judol, indonesian-social-media, bert, browser-extension
- **Relevance Anchors in Repo:** Connects to Stage 8 (Data Leakage & Pairing), Stage 9 (Baseline Models), Stage 10 (Adversarial Robustness O1-O4), and Stage 11 (Domain Shift OOD).

---

# Full Extracted Document Text



<!-- PAGE 1 -->

ISSN 2089-8673 (Print) | 2548-4265 (Online) 
Volume 14, Issue 3, 2025, pp. 679-691 
 
____________ 
 
*Corresponding author: gilbert.situmorang@mikroskil.ac.id (G. F. Situmorang) 
 
This is an open access article under the CC BY-SA license.  
© 2025 The Author(s). Published by Universitas Pendidikan Ganesha. 
 
679 
AN INTELLIGENT SYSTEM FOR DETECTING ONLINE GAMBLING 
PROMOTION ON SOCIAL MEDIA BASED ON BERT AND ADAPTIVE 
BROWSER EXTENSION 
 
 
Gilbert Fernando Situmorang*, Juliana Damayanti Manurung, Rivaldi Lubis,  
Nadya Sikana, Kenneth Lionggo 
 
Faculty of Informatics, Mikroskil University, Medan, Indonesia 
 
 

## Abstract
 
The proliferation of online gambling promotions on social media has created serious social and legal 
problems in Indonesia, yet existing detection approaches are largely post-hoc, rely on general purpose 
language models, and struggle to identify implicit a nd domain specific promotional language that is 
deliberately used to evade moderation. Moreover, most prior studies focus solely on offline model evaluation 
and are rarely integrated into real time, deployable systems that can directly protect users. To address these 
limitations, this study proposes an intelligent detection system utilizing IndoBERT enhanced with Domain 
Adaptive Pre-Training on a corpus of Indonesian online gambling related text, followed by fine-tuning for text 
classification. The adapted model demonstrates superior performance, achieving an F1-Score of 98.58% 
and outperforming baseline approaches including TF-IDF+SVM, BiLSTM, multilingual BERT, and IndoBERT 
without domain adaptation. To bridge the gap between model development and real-world application, the 
proposed model is further integrated into an adaptive browser extension capable of scanning, classifying, 
and filtering social media content in real-time. Functional testing on YouTube and X shows that the system 
effectively detects and masks online gambling promotional content without disrupting neutral or antigambling discourse. This research contributes both methodologically, by demonstrating the effectiveness of 
domain adaptive pre-training for detecting implicit promotional language, and practically, by delivering a 
deployable system that provides proactive protection for social media users. 
 
Keywords: BERT, Browser Extension, Deep Learning, Online Gambling Promotion, Social Media 
 
Received: 10-09-2025 | Accepted: 30-12-2025 | Available Online: 31-12-2025 
DOI: https://doi.org/10.23887/janapati.v14i3.103511 
 
I. INTRODUCTION 
The digital era, with its massive internet and 
social media penetration, has transformed the 
landscape of global interaction and 
communication [1]. According to Kalodata 
(January 2024), Indonesia has 185.3 million 
internet users, with 139 million of them active 
social media users. This figure indicates that 
platforms such as YouTube, Instagram, 
Facebook, X (Twitter), and TikTok have become 
the primary channels for information distribution in 
Indonesia [2]. On the positive side, social media 
facilitates communication and access to 
information. However, these platforms are also 
exploited for illegal activities, one of which is the 
promotion of online gambling [3]. 
Online gambling promotion is defined as any 
content disseminated through social media that 
explicitly or implicitly encourages participation in 
online gambling activities, either directly through 
advertisements or indirectly through persuasive 
and coded language. Such promotional content 
commonly employs explicit markers such as 
invitations to play, bonus offers, platform or site 
mentions (e.g., link, situs), as well as implicit 
linguistic strategies including domain -specific 
terminology (e.g., deposit, spin, prediksi, gacor), 
hashtags, numerical patterns, symbolic 
substitutions, and emoji -based persuasion 
designed to evade moderation [4, 5]. Gambling is 
prohibited in Indonesia under Law No. 7 of 1974 
[6]. However, online gambling promotion remains 
rampant, utilizing recommendation algorithms, 
hidden advertising, and creative content to target 
various groups, including the younger generation 
[7]. This phenomenon raises social concerns, 
reflected in the increasing number of reports to

---


<!-- PAGE 2 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 680 
 
the Ministry of Communication and Information 
Technology (Kominfo) and civil society 
organizations such as the Indonesian AntiDefamation Society (Mafindo) [8]. The impact of 
gambling promotion is multidimensional: from a 
social perspective, it triggers addiction, financial 
loss, family conflict, and even criminal activity; 
legally, this activity clearly violates regulations [9] 
[10]. Promotional strategies disguised as games 
or get rich quick investments increase risks, 
especially for people with limited digital literacy 
[11]. 
The government, through the Ministry of 
Communication and Information Technology 
(Kominfo), has addressed this phenomenon by 
blocking websites and accounts, as well as 
conducting outreach and law enforcement. 
Throughout 2023, more than 800,000 pieces of 
content were successfully blocked [12]. However, 
the manual approach is reactive and inefficient, 
as monitoring teams must verify reports 
individually, while the volume of data and the 
speed of content dissemination are very high. 
This demands technology-based solutions that 
are more automated, adaptive, and real-time. 
In the context of text analysis, approaches 
based on artificial intelligence (AI), machine 
learning (ML), and natural language processing 
(NLP) play a crucial role. One prominent model is 
BERT (Bidirectional Encoder Representations 
from Transformers), a transformer-based deep 
learning architecture capable of understanding 
word context bidirectionally [13]. BERT's 
superiority has been empirically proven in various 
complex text classification tasks, such as 
identifying depression through analyzing social 
media post text X [14], detecting fake news [15], 
and analyzing public opinion on government 
policies [16]. BERT's ability to capture linguistic 
nuances and hidden patterns makes it highly 
relevant for detecting online gambling 
promotional texts, which often use disguised 
vocabulary, symbols, and evolutionary linguistic 
strategies to evade detection. 
Previous research has explored AI for the 
problem of online gambling promotion detection. 
Samuel & Kristiadi [17] compared Naïve Bayes 
and SVM with IndoBERT on Indonesian YouTube 
comments, with IndoBERT achieving 97% 
accuracy, but the analysis was still post-hoc and 
not yet real-time. Perdana et al. [4] tested TF-IDF, 
GloVe, Word2Vec with CNN, Logistic 
Regression, and Random Forest on Twitter data; 
TF-IDF + Random Forest achieved 95.8% recall 
and 96.6% precision, but had limitations in 
capturing complex semantic context. Teppap et 
al. [18] used web scraping to detect gambling 
content on Thai websites, with 89% accuracy, but 
the keyword-based approach was less robust to 
language variations. Widiyanto et al. [19] 
compared LightGBM, XGBoost, CatBoost with 
LSTM and GRU for YouTube comments, with 
LightGBM performing best (F1-score 0.8737), but 
deep learning failed consistently due to 
overfitting. In general, most research focuses on 
accurate models, but not many have integrated 
models into real-time systems or utilized DomainAdaptive Pre-Training (DAPT) techniques for 
online gambling-specific vocabulary. In fact, 
online gambling promotions have distinctive 
vocabulary that is often implicit and uses stylistic 
variations to evade censorship, such as terms like 
"deposit", "spin", "new member bonus", or 
disguised with symbols and numbers. This makes 
general models such as BERT or IndoBERT 
prone to misclassification when faced with text 
outside their initial pre-training distribution [20]. 
This is where Domain -Adaptive Pre-Training 
(DAPT) becomes important. By conducting 
additional pre-training on a corpus of Indonesian 
online gambling text, the model can adapt its 
language representation to domain -specific 
linguistic patterns [21]. Thus, the integration of 
DAPT is expected to provide a significant 
contribution in building a more accurate, adaptive, 
and applicable detection system in real scenarios. 
Based on this gap, this study, titled "An 
Intelligent System for Detecting Online Gambling 
Promotions on Social Media Based on BERT and 
an Adaptive Browser Extension," presents two 
key innovations. First, the development of a 
BERT model with Domain Adaptive Pre-Training 
(DAPT) on an Indonesian -language online 
gambling text corpus improves the accuracy of 
detecting hidden promotions. Second, the model 
is integrated into an adaptive browser extension 
that works in real-time to scan and filter content 
on social media, automatically providing warnings 
or hiding harmful content. 
The scope of this study focuses on 
Indonesian-language content sourced from 
YouTube and X (Twitter). The analytical scope 
includes only text-based components such as 
comments, captions, URLs, hashtags, and 
emojis while visual or multimodal elements 
(images and videos) are acknowledged but 
excluded from analysis. The real-time system 
developed in this study is implemented on 
Chromium-based desktop browsers to 
demonstrate feasibility and operational 
performance. 
Thus, this research is expected to make a 
significant contribution to both the development of 
NLP models and their application as real-world 
intelligent systems, providing proactive protection 
for social media users.

---


<!-- PAGE 3 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 681 
 
II. METHOD 
This study uses a Research and Development 
(R&D) approach in designing and testing an 
intelligent online gambling promotion detection 
system based on IndoBERT integrated with a 
browser extension. The research process begins 
with collecting text data from X using keywords 
relevant to online gambling promotion activities, 
in line with the practice of collecting domain -
specific corpora from social media for model 
adaptation needs [22] undergoes a manual 
annotation process by two independent 
annotators, with reliability measured using the 
Cohen's Kappa coefficient to establish ground 
truth (although the use of Kappa is not 
documented in previous literature, this practice is 
recommended to ensure annotation 
consistency). 
After the annotation process, a text 
preprocessing stage is carried out which includes 
data cleaning, normalization, and tokenization 
using tools appropriate for the Indonesian 
language [23]. The preprocessed data is used in 
modeling, which begins with Domain Adaptive 
Pretraining (DAPT) on the IndoBERT model, a 
monolingual BERT model adapted specifically for 
the Indonesian language [23] to adapt the 
language representation to the characteristics of 
the online gambling domain [22, 24], then 
continued with fine-tuning using labeled data. 
The gradual fine-tuning strategy is reported to 
improve stability and accuracy in low resource 
domain adaptation scenarios [25], thus 
supporting the application of this method to 
produce accurate and robust classification 
models. Performance evaluation was conducted 
using standard classification metrics, namely 
accuracy, precision, recall, and F1-score [23, 26, 
27]. In addition, the performance of IndoBERT 
resulting from DAPT + fine-tuning was compared 
with several baseline models, namely a 
combination of TF-IDF and SVM, BiLSTM, and 
Multilingual BERT (mBERT), as commonly used 
to provide a comprehensive overview of t he 
superiority of the proposed approach [23, 28]. 
The final stage of the research was the 
development of an adaptive browser extension 
integrated with the best model. This extension 
allows for automatic and real-time detection of 
online gambling promotions and was tested in a 
user environment to assess its performance and 
reliability. The entire research flow is depicted in 
Fig 1. 
 
 
 
Figure 1. Research Methodology 
A. Data Collection 
The primary data in this study was collected 
anonymously from social media platform X using 
a scraping technique, solely for research 
purposes. The data collection period covered 
posts from January 2024 to June 2025, to 
adequately capture a variety of tren ds and 
language patterns. 
In designing the data collection criteria, three 
content categories were established. The first 
category encompassed gambling promotional 
content, obtained through 34 explicit and implicit 
keywords commonly used in online gambling 
promotions. The second ca tegory was anti-

---


<!-- PAGE 4 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 682 
 
gambling promotional content, collected through 
36 keywords representing rejection or criticism of 
online gambling. Meanwhile, the third category 
consisted of neutral content taken from general 
conversations unrelated to gambling, which 
served as a strong negative class in the 
classification. 
B. Data Annotation and Validation 
A total of 1,500 posts were selected through 
stratified random sampling from the entire 
corpus, with the aim of ensuring proportional 
representation of each category. Each category 
consisted of 500 posts: gambling promotion, antigambling promotion, and irrelevant posts. All 
sample data was then manually annotated by two 
independent, trained annotators. The annotation 
process classified the text into three main 
categories. The first category is gambling 
promotion, which includes text containing 
invitations, promotional offers, or references to 
online gambling platforms. The second category 
is anti-gambling promotion, which includes text 
containing rejections, criticisms, or warnings 
about the dangers of gambling. The third 
category is irrelevant or neutral, which is general 
conversational text unrelated to the gambling 
context. 
To ensure the consistency and reliability of 
the annotation results, agreement between 
annotators was measured using the Cohen's 
Kappa coefficient. A score of 0.9001 indicates a 
very high level of agreement, or almost perfect 
agreement. After cleaning up to eliminate 
ambiguous and inconsistent data, 1,402 valid 
uploads were obtained and used as ground truth 
for the model training stage.  
To clarify the annotation criteria, Table 1 . 
presents representative raw-text samples with 
final labels agreed upon by both annotators, 
covering one positive (gambling promotion), one 
negative (anti -gambling), and one 
borderline/neutral example. These examples 
illustrate how annotators distinguished 
promotional intent from discouraging or non -
promotional mentions. 
C. Text Pre-processing 
Before being used for model training, text data 
undergoes a preprocessing stage to ensure 
quality and uniformity, ensuring optimal 
performance for the transformer-based model. 
This preprocessing process includes three main 
steps: text cleaning, linguistic normalization, and 
filtering. 
The text cleaning stage removes null and 
duplicate data to avoid bias and redundancy. 
Furthermore, noise in the form of special 
characters, symbols, and uninformative non-text 
elements is removed. Certain entities are then 
normalized; for example, URL addresses are 
replaced with <URL> tokens, while user 
mentions are disguised as <USER> tokens to 
reduce data dimensionality without losing 
context. Hashtags are processed by removing 
the pound symbol (#) while preserving their text; 
for example, #slotgacor beco mes slotgacor. 
Meanwhile, emojis and emoticons are converted 
into text representations using the Python emoji 
library; for example, 
"# is represented as the 
word "fire." 
The next stage is linguistic normalization, 
which includes case folding to convert all text to 
lowercase for uniformity; lexical normalization by 
mapping non-standard words, slang, or 
abbreviations to their formal forms using the 
Colloquial Indonesian Lexicon (e.g., "bgst" is 
normalized to "bangsat" or "loe" to "lu"); and 
repeated character correction to change overspelled words like "grraatiisss" to "gratis." 
 
Table 1. Representative Examples of Annotated Raw Text for Each Label Category 
text category label 
slot gacor terpercaya yang memberikan jackpot besar dan 
permainan gampang menang maxwin dengan tingkat rtp dan 
winrate tinggi? Segera kunjungi Raj*****2 jika ingin merasakan 
sensasi bermain yang berbeda LINK DAFTAR : <URL> 
Gambling Promotion 0 
<USER> <USER> Asli gw jg ngeri tp gw pengen orang2 
sedikitnya perlu tau karena sistem ini gabisa diganggu gugat 
oleh siapapun. Masyarakat harus bisa sadar untuk stop judol 
atas kemauan sendiri. Saling ingatkan sekitar 
Anti Gambling 1 
<USER> org Ga ada yg menyalahkan fenomena ini sdh ada 
sejak adanya Mall yg sekedar buat piknik dan ngadem jg sdh 
lama ada. Yg punya Mall jg paham makanya tarif parkir suka 
diluar aturan seenak jidat mereka. 
Neutral 2

---


<!-- PAGE 5 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 683 
 
The final stage is filtering, which removes 
irrelevant numbers, such as telephone numbers 
or random digits. However, numbers with 
significant meaning in the gambling domain are 
retained, such as bonus percentages like 
"100%," monetary denominations like "10,000" or 
"50,000," and service formats like "24/7." 
All these stages are designed to improve the 
quality of data representation, reduce noise, and 
preserve semantic meaning, enabling the model 
to classify text more accurately. 
D. IndoBERT Domain Adaptive Pre-Training 
This stage uses IndoBERT [18], a pre-trained 
language model (PLM) based on the BERT 
architecture that has been optimized for the 
Indonesian language. This model then 
undergoes Domain Adaptive Pre-Training 
(DAPT) [19] using a corpus of 18,057 unlabeled 
texts obtained specifically from the online 
gambling domain. This corpus has never been 
used in previous pre -training processes, 
ensuring a genuine adaptation to the target 
domain. 
The DAPT process involves retraining the 
model using a Masked Language Modeling 
(MLM) task on this domain specific corpus. The 
goal of this stage is to adapt IndoBERT's 
linguistic representations to be more 
contextualized to the lexical, syntactic, and 
semantic characteristics typical of the online 
gambling domain. This adaptation is expected to 
improve the model's ability to recognize 
disguised language patterns commonly used in 
online gambling promotions, ultimately improving 
its performance on text classification tasks that 
rely heavily on understanding this domain. 
From a theoretical standpoint, DAPT provides 
advantages over standard fine-tuning because 
general-purpose pretrained language models are 
trained on broad and heterogeneous corpora 
whose linguistic distributions differ substantially 
from those of specialized domains. Continued 
pre-training on a domain -specific unlabeled 
corpus allows the model to internalize domainrelevant lexical statistics, semantic regularities, 
euphemistic expressions, and context -
dependent patterns that are underrepresented in 
generic corpora. This process enriches the 
model's underlying semantic representations 
prior to supervised fine -tuning, enabling the 
subsequent fine-tuning stage to operate on 
domain-adapted representations rather than 
general-purpose ones. In contrast, standard finetuning adjusts primarily task-specific parameters 
and does not substantially reshape the model's 
representational space, limiting its effectiveness 
in domain-specific settings with limited labeled 
data. Empirical evidence reported in [21] 
demonstrates that domain-adaptive pre-training 
followed by fine-tuning consistently improves 
downstream performance on specialized tasks, 
thereby providing a strong theoretical justification 
for the approach adopted in this study. 
E. IndoBERT Fine-tuning 
After going through the Domain-Adaptive PreTraining (DAPT) stage, the IndoBERT model, 
adapted to the online gambling domain, was then 
fine-tuned for the classification task using a 
ground truth of 1,402 labeled texts. The fine -
tuning process was performed by adding a linear 
layer above the [CLS] token in the IndoBERT 
encoder, where all model parameters were 
adjusted through a full fine-tuning scheme to 
minimize the loss function for the classification 
task. 
To optimize performance and test robustness, 
experiments were conducted considering two 
main aspects. First, the data was randomly and 
stratified into a 90:10 or 80:20 ratio for training 
and test data, ensuring a proportional label 
distribution. Second, hyperparameter exploration 
was conducted by adjusting the batch size (16 
and 32), the learning rate (2e-5, 3e-5, and 5e-5), 
and the number of epochs between three and five 
training rounds. All combinations were evaluated 
to find the optimal configuration, balancing 
training speed, convergence stability, and 
preventing overfitting. 
The primary goal of this experiment was to 
find the best training configuration so that the 
model could produce accurate, robust 
predictions, and have good generalization 
capabilities. The model with the best 
performance on the validation data was then 
selected for final evaluation using the test data, 
before being integrated into the online gambling 
promotion detection system. 
F. Browser Extension Development and 
Integration. 
The best model selected from the evaluation 
results, IndoBERT, which underwent DomainAdaptive Pre-Training (DAPT) and fine-tuning, 
was then integrated into an adaptive browser 
extension. This extension is designed to operate 
in real time, aiming to automatically detect and 
flag online gambling promotional content as 
users browse social media platforms. 
The model's integration into the extension is 
accomplished through efficient client-server 
architecture. On the server side, the machine 
learning model is deployed as a lightweight and 
scalable web API service utilizing the FastAPI 
framework in Python. This service receives text

---


<!-- PAGE 6 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 684 
 
requests from the extension and returns a 
response in JSON format containing the 
classification predictions and the model's 
confidence score. Meanwhile, on the client side, 
the extension was developed using JavaScript 
for Chromium-based browsers like Googl e 
Chrome and Microsoft Edge. Its function is to 
monitor and access the Document Object Model 
(DOM) of the currently opened web page, extract 
text content from social media posts, and send it 
to the available API endpoint. 
Once the response from the API is received, 
the extension automatically takes action based 
on the predictions. These actions can include 
hiding, blurring, or marking elements of posts 
detected as promoting online gambling. The 
entire process is designed to run with low latency, 
ensuring a responsive user experience without 
interruption. With this architecture, heavy 
computation, such as model inference, is 
performed server-side, while the extension 
handles only lightweight front-end tasks. This 
approach ensures smooth performance and 
efficient resource usage in the user's browser. A 
detailed overview of this architecture is presented 
in Fig 2, which outlines the data flow between the 
browser extension, server-side inference API, 
and the IndoBERT+DAPT model. 
 
 
 
Figure 2. Architecture of the browser extension integrated 
with the IndoBERT + DAPT model for real-time gamblingcontent detection. 
G. Extension Testing 
The final stage of this research involved 
testing the system's overall functionality in a 
simulated environment that mimics real -world 
conditions. The test aimed to assess the 
performance, accuracy, and integration between 
the machine learning model and the browser 
extension. To this end, synthetic content was 
created representing various scenarios, including 
text containing explicit and implicit gambling  
promoting keywords, text criticizing or rejecting 
gambling, and neutral text unrelated to gambling. 
The testing was then applied to major social 
media platforms, namely YouTube and X 
(formerly Twitter), by installing the extension on 
the Google Chrome browser. Each piece of 
synthetic content was uploaded, and the 
extension's response was observed to assess 
the overall system. 
III.RESULT AND DISCUSSION 
A. Dataset Statistic 
The dataset preparation process goes 
through several critical stages, from data 
collection to annotation validation, to produce 
high-quality ground truth. The initial scraping 
process collected 19,974 posts, with an early 
distribution dominated by gambling-promotion 
content (Label 0). From this corpu s, 1,500 
samples were selected using a stratified random 
sampling method (500 samples per category) to 
ensure balanced representation during 
annotation. 
Two independent annotators then labeled 
the data, and disagreements were resolved 
through adjudication, resulting in a final dataset 
of 1,401 samples. The Cohen's Kappa score of 
0.9001 indicates near -perfect agreement, 
fulfilling widely accepted standards for annotation 
reliability. The final dataset distribution is 
relatively balanced, consisting of 30.8% 
"Gambling Promotion," 30.2% "Anti-Promotion," 
and 39.0% "Neutral." 
Although neutral posts were more frequent in 
the scraped corpus, the stratified sampling 
procedure effectively mitigated this imbalance by 
enforcing equal sample sizes during annotation. 
As a result, the final ground -truth dataset 
maintains class proportions within the 30-40% 
range, which is generally considered sufficiently 
balanced for supervised classification tasks. 
Therefore, additional imbalance -handling 
techniques such as oversampling, 
undersampling, or class -weight adjustments 
were not required. Detailed statistics of this 
process are presented in Table 2.

---


<!-- PAGE 7 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 685 
 
 
Table 2. Data Distribution in the Dataset Preparation Stage 
Preparation Step Gambling Promotion 
(Label 0) 
Anti Promotion 
(Label 1) 
Irrelevant / Neutral 
(Label 2) 
Total 
Initial Data Scraping 
Results 7965 5507 6502 19974 
Sample For 
Annotation 500 500 500 1500 
Final Dataset 
(Ground Truth) 431 423 547 1401 
B. Domain-Adaptive Pre-Training (DAPT) 
A key stage in this experiment is Domain -
Adaptive Pre-Training (DAPT), which is 
conducted to adapt the pre-trained IndoBERT 
baseline model to the online gambling domain. 
The goal of this stage is to allow the model to 
learn more specific and context-rich linguistic 
representations from the target domain corpus, 
before being fine-tuned for the classification task. 
The hyperparameter configuration for the 
DAPT process was fixed. We used a learning 
rate of 5e-5, a batch size of 32, and ran the 
training for 3 epochs. This parameter selection 
follows standard practice for domain adaptation, 
designed to enable smooth and stable model 
weight updates, thereby minimizing the risk of 
performance degradation or overfitting to the 
domain data. 
The training results show a very positive 
trend. As shown in Fig 3, the training loss graph 
shows a significant and consistent decrease with 
increasing epochs. This steady downward trend 
indicates that the model has successfully 
internalized the unique patterns, vocabulary, and 
linguistic structures of the online gamblin g 
domain corpus. 
 
 
 
Figure 3. Training Loss vs Validation Loss Graph in the 
IndoBERT DAPT Process 
 
The success of the DAPT process was also 
marked by the absence of any indication of 
overfitting, indicating that the adaptation was 
robust. The resulting DAPT model was then 
saved and used as the base model for all 
subsequent fine-tuning stages. Thus, DAPT 
serves as a foundation that enriches the model's 
representation, thereby increasing the relevance 
and depth of the model's understanding of texts 
in the target domain during the classification 
stage. 
C. Hyperparameter Optimization and FineTuning 
Following the Domain-Adaptive Pre-Training 
(DAPT) phase, the adapted IndoBERT model 
was fine-tuned for the classification task. A 
comprehensive grid search was conducted to 
identify the optimal hyperparameter 
configuration, exploring variations across several 
key parameters. Training epochs were tested at 
3, 4, and 5, batch sizes of 16 and 32 were 
evaluated, and learning rates of 2e-5, 3e-5, and 
5e-5 were compared. Additionally, the data split 
ratio for training and validation varied between 
80:20 and 90:10. The F1-Score on the validation 
set was selected as the primary metric due to its 
robustness in balancing precision and recall, 
which is crucial for classification tasks with 
potential class imbalances. Additional metrics 
including accuracy, precision, recall, and loss 
were also recorded to provide a holistic 
assessment of model performance, ensure 
training stability, and guard against overfitting. 
Through this systematic exploration, the optimal 
configuration was identified: 4 epochs, a batch 
size of 32, a learning rate of 1e-5, and a 90:10 
data split. This configuration achieved a peak F1Score of 98.58%, demonstrating superior 
performance and generalization capability. The 
complete results of the grid search experiment 
are presented in Table 3 and Table 4.

---


<!-- PAGE 8 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 686 
 
Table 3. Hyperparameter Tuning Results with 80:20 Data Split 
Learning Rate Batch Size Accuracy F1-Score Precision Recall Loss 
1e-05 8 98.22% 98.22% 98.27% 98.22% 0.1023 
16 97.86% 97.86% 97.92% 97.86% 0.1074 
32 97.51% 97.51% 97.59% 97.51% 0.0887 
2e-05 8 98.22% 98.22% 98.27% 98.22% 0.1108 
16 97.86% 97.87% 97.95% 97.86% 0.1129 
32 98.22% 98.22% 98.27% 98.22% 0.0959 
3e-05 8 98.58% 98.58% 98.64% 98.58% 0.1219 
16 98.58% 98.58% 98.64% 98.58% 0.0977 
32 98.22% 98.23% 98.32% 98.22% 0.0965 
Table 4. Hyperparameter Tuning Results with 90:10 Data Split 
Learning Rate Batch Size Accuracy F1-Score Precision Recall Loss 
1e-05 bs8 98.58% 98.58% 98.64% 98.58% 0.1111 
16 98.58% 98.58% 98.64% 98.58% 0.1009 
32 98.58% 98.58% 98.64% 98.58% 0.0962 
2e-05 8 98.58% 98.58% 98.64% 98.58% 0.1202 
16 98.58% 98.58% 98.64% 98.58% 0.1084 
32 98.58% 98.58% 98.64% 98.58% 0.0972 
3e-05 8 97.87% 97.88% 98.01% 97.87% 0.1296 
16 98.58% 98.58% 98.64% 98.58% 0.1111 
32 97.87% 97.86% 97.95% 97.87% 0.1234 
Based on the experimental results, the best 
hyperparameter combination was obtained, 
consisting of four epochs, a batch size of 32, and 
a learning rate of 1e-5. The data was also divided 
with a ratio of 90% for training and 10% for 
testing. This configuration proved to produce 
optimal performance with the highest F1-Score 
reaching 98.58% while demonstrating consistent 
stability throughout the training process. 
Therefore, this combination was chosen as the 
final configuration for model testing on the test 
data. Thus, the fine-tuning and hyperparameter 
optimization process successfully produced a 
model that is not only accurate but also robust in 
classifying text in the online gambling domain. 
D. Comparative Analysis and Model 
Performance 
To ensure fair and meaningful comparisons, 
all baseline models, including TF -IDF+SVM, 
BiLSTM, mBERT, and IndoBERT without DAPT, 
were evaluated using the same hyperparameter 
configuration as the proposed model. This 
configuration included four epochs, a batch size 
of 32, and a learning rate set at 1e -5. 
Furthermore, the data was split 90% for training 
and 10% for testing. This consistent configuration 
ensures that any performance differences solely 
reflect differences in model architecture and the 
presence of the DAPT stage, rather than 
variations in hyperparameter settings. 
Based on Table 5, the IndoBERT + DAPT + 
Fine-Tuning model (the proposed model) 
consistently demonstrated the best performance 
across all evaluation metrics. Compared to the 
previously strongest baseline, IndoBERT without 
DAPT, the proposed model delivered significant 
improvements: the F1 -Score increased to 
98.58% (from 97.86%), Accuracy increased to 
98.58% (from 97.86%), and Loss decreased to 
0.096 (from 0.129).

---


<!-- PAGE 9 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 687 
 
Table 5. Performance Comparison of Baseline Models and Proposed IndoBERT-DAPT Model 
Model Accuracy F1-Score Precision Recall Loss 
TF-IDF + SVM 95.79% 95.75% 96.08% 95.79% - 
BiLSTM 92.33% 92.33% 92.25% 92.33% 0.258 
mBERT + Fine -Tuning 97.50% 97.50% 97.54% 97.50% 0.146 
IndoBERT + Fine -Tuning 97.86% 97.86% 97.87% 97.86% 0.129 
IndoBERT + DAPT + FT 98.58% 98.58% 98.64% 98.58% 0.096 
 
In addition to quantitative evaluation, analysis 
was also conducted on the convergence process 
during training to understand the behavior of 
each model. The visualizations in Fig 4 and 5 
show a comparison of the loss curves on the 
training and validation data between the best 
baseline model and the proposed model. 
 
 
 
Figure 4. Training Loss vs Validation Loss Graph in the 
IndoBERT + Fine-tuning 
 
 
 
Figure 5. Training Loss vs Validation Loss Graph in the 
IndoBERT + DAPT + Fine-tuning 
 
The results in the graphs show that IndoBERT 
+ DAPT + Fine-Tuning not only achieved the 
lowest final loss but also exhibited a faster and 
more stable convergence pattern than the other 
models. This indicates that models that go 
through the DAPT stage have a better initial 
understanding of the domain, resulting in a more 
efficient fine-tuning process. In contrast, the 
model without DAPT (IndoBERT FT) 
experienced slower convergence with a higher 
final loss. 
Furthermore, consistent improvements in 
Precision and Recall confirm that the DAPT 
approach not only improves overall detection 
accuracy but also provides a better performance 
balance. The proposed model is more robust in 
recognizing positive patterns while reducing the 
false positive rate. The significant reduction in 
loss also confirms that this model has stronger 
generalization capacity and higher prediction 
confidence compared to the baseline. 
E. Functional Testing of Extensions on 
Social Media Platforms 
Functional testing was conducted to validate 
the browser extension's effectiveness in real -
world scenarios. The extension was tested on 
two social media platforms: YouTube and X, with 
a focus on its ability to accurately detect and hide 
online gambling pro motional content in a 
dynamic, real-time environment. 
 
  
Figure 6. YouTube comments before the extension was 
activated.

---


<!-- PAGE 10 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 688 
 
 
 
 
Figure 7. YouTube comments after the extension was 
activated 
 
 
 
Figure 8. X posts before the extension was activated 
 
The testing used synthetic posts simulating 
different types of content. The first post contained 
gambling promotions, including bonuses, 
gambling site links, or invitations to play. The 
second post contained anti-gambling content that 
promoted or raised awareness about the dangers 
of gambling. The third post was neutral and 
unrelated to gambling. The appearance of the 
extension before activation is shown in Fig 6 and 
8, while the filtering results after activation are 
shown in Fig 7 and 9. This qualitative testing 
aimed to verify whether the extension's basic 
functions, namely detection and concealment, 
were working correctly. 
 
The extension consistently triggered hiding 
only for gambling promotional content and did not 
hide anti-gambling or neutral content. These 
findings confirm that the model has good 
contextual capabilities in distinguishing between 
gambling promotions and content that discusses 
gambling negatively or neutrally. Furthermore, 
the extension can be integrated and run smoothly 
in both YouTube and X environments, 
demonstrating its robust implementation. 
 
 
 
Figure 9. X posts after the extension was activated 
 
In addition to these qualitative observations, 
response time was measured to evaluate the 
real-time feasibility of the browser extension. The 
extension processes visible comments in 
batches rather than individually, allowing multiple 
texts to be classified within a single API request 
to improve efficiency. The batch size was 
determined automatically based on the number 
of visible comments detected in the DOM during 
each scan cycle, reflecting realistic browsing 
conditions.

---


<!-- PAGE 11 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 689 
 
  
Table 6. Response Time Evaluation of the Browser Extension 
Batch Size Min Latency (ms) Max Latency (ms) Average Latency (ms) 
15 texts 794.80 1234.80 958.18 
5 texts 144.70 706.20 295.08 
 
Response time was measured on the client 
side using high-resolution timestamps 
(performance.now()), capturing end -to-end 
latency from the moment the request was sent to 
the inference API until the model returned its 
predictions. During real -world testing using 
comment streams from actual YouTube and X 
pages, the system processed batches of 5 and 
15 texts. Table 6 summarizes the minimum, 
maximum, and average response times for each 
batch size. 
All tests were conducted in a controlled local 
environment in which both the browser extension 
and the inference API ran on the same machine 
(Ryzen 5 652U CPU, 16 GB RAM, SSD). While 
latency may differ in production settings due to 
network variability, the results reflect the intrinsic 
inference time of the IndoBERT+DAPT model 
within the integrated system. The observed 
latency (<1.3 seconds for 15 texts and <0.8 
seconds for 5 texts) falls within a reasonable 
threshold for real -time content moderation. 
Overall, these results demonstrate successful 
system integration and indicate that the 
extension is suitable for larger-scale deployment. 
Overall, this testing demonstrates the 
successful integration of the IndoBERT machine 
learning model enriched with Domain Adaptive 
Pre-Training and Fine-Tuning with the browser 
extension, and the extension is ready for further 
testing on a larger scale. 
IV. CONCLUSION 
This research successfully addresses the 
limitations of previous studies that focused solely 
on model accuracy without considering real-world 
system integration or domain-specific linguistic 
characteristics. The application of Domain -
Adaptive Pre-Training (DAPT) to IndoBERT, 
followed by fine-tuning, resulted in substantial 
performance gains, achieving an F1-Score of 
98.58% and outperforming baselines such as TFIDF+SVM, BiLSTM, mBERT, and IndoBERT 
without DAPT. Through exposure to gamblingrelated unlabeled corpora, DAPT equips the 
model with domain -specific semantic 
understanding, enabling it to recognize implicit 
promotional cues, coded expressions, 
euphemisms, and context-dependent linguistic 
patterns that general-purpose pre-training cannot 
capture. 
The integration of this model into an adaptive 
browser extension enables real-time detection of 
online gambling promotions on social media 
platforms, with the ability to hide harmful content 
without disrupting neutral or anti -gambling 
content. Functional test results demonstrate the 
system's consistent, efficient, and responsive 
performance, providing proactive protection for 
social media users. 
Beyond its technical contributions, the 
proposed system offers long-term implications for 
digital governance and public digital literacy. By 
enabling automated, real-time filtering of illegal 
gambling promotions, the system has the 
potential to support pla tform-level content 
moderation policies, strengthen national digital 
safety initiatives, and reduce societal exposure to 
harmful online content. Over time, this contributes 
to a healthier digital ecosystem and enhances 
users' awareness and resilience toward predatory 
or deceptive online gambling practices. 
However, this research has several limitations. 
The developed system currently only runs on 
Chromium-based desktop browsers and does not 
yet support mobile devices or other browser 
platforms. Furthermore, this research still focuses 
on text-based detection, even though online 
gambling promotional content is often packaged 
in images or a combination of text and images, so 
multimodal aspects are not optimally 
accommodated. 
Further research should focus on expanding 
system support to allow cross  device 
compatibility, including mobile devices, and 
integrating multimodal deep learning techniques 
capable of processing both text and visual 
elements such as images and videos.  
Additionally, exploring distributed or cloud-based 
inference will be essential for large -scale 
deployment, while continual learning approaches 
can help the system adapt to evolving slang, 
coded language, and adversarial promotional 
strategies. These directions are expected to make 
the detection system more comprehensive, 
adaptive, and effective in addressing the dynamic 
nature of online gambling promotional content 
across various social media platforms.

---


<!-- PAGE 12 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 690 
 

## References
 
[1] L. T. D. Amelia and N. R. Balqis, 
"Changes in Communication Patterns in 
the Digital Age," ARRUS J. Soc. Sci. 
Hum., vol. 3, pp. 544-556, Sep. 2023, doi: 
10.35877/soshum1992. 
[2] KALODATA, "Digital 2024: Indonesia - 
Kalodata," Sep. 2024. [Online]. Available: 
https://www.kalodata.com/id/blog/2024/0
4/digital-2024-indonesia/ 
[3] A. House et al., "Social Media and 
Gambling," in Social Media and Mental 
Health. , Cambridge University Press, 
2023, pp. 98 -108. doi: DOI: 
10.1017/9781009024945.014. 
[4] R. B. Perdana, Ardin, I. Budi, A. B. 
Santoso, A. Ramadiah, and P. K. Putra, 
"Detecting Online Gambling Promotions 
on Indonesian Twitter Using Text Mining 
Algorithm," International Journal of 
Advanced Computer Science and 
Applications, vol. 15, no. 8, 2024, doi: 
10.14569/ijacsa.2024.0150893. 
[5] S. R. Paminto, I. K. Ahmad, Z. S. 
Rohman, N. Diana, L. Sari, and A. 
Ghajwan, "Pengaruh Iklan di Media Sosial 
dan Platform Donasi Streamer terhadap 
Peningkatan Aktivitas Judi Online 
Dihubungkan dengan Pasal 27 Ayat 2 
Undang-Undang Nomor 11 Tahun 2008 
tentang Informasi dan Transaksi 
Elektronik," Jurnal Hukum dan Sosial 
Politik, vol. 2, no. 4, pp. 93-101, 2024, 
doi: 10.59581/jhspwidyakarya.v2i4.4277. 
[6] Pemerintah Republik Indonesia, 
"Undang-Undang Nomor 7 Tahun 1974 
tentang Penertiban Perjudian," Sep. 
1974. [Online]. Available: 
https://peraturan.bpk.go.id/Details/47415/
uu-no-7-tahun-1974 
[7] R. Rossi and A. Nairn, "New 
Developments in Gambling Marketing: 
the Rise of Social Media Ads and Its 
Effect on Youth," Curr Addict Rep, vol. 9, 
pp. 385 -391, 2022, doi: 
10.1007/s40429022004570. 
[8] Kementerian Komunikasi dan Informatika 
Republik Indonesia, "Surat Edaran 
Menteri Komunikasi dan Informatika 
Nomor 7 Tahun 2024 tentang 
Pemberantasan Judi Online dan/atau 
Judi Slot di Lingkungan Kementerian 
Komunikasi dan Informatika," Sep. 2024. 
[Online]. Available: 
https://jdih.komdigi.go.id/produk_hukum/
view/id/920/t/surat+edaran+menteri+kom
unikasi+dan+informatika+nomor+7+tahu
n+2024 
[9] P. Angellina and B. Prasetyo, 
"Pertanggungjawaban Pidana Terhadap 
Pelaku yang Mempromosikan Judi 
Online," Ranah Research Journal of 
Multidisciplinary Research and 
Development, vol. 7, pp. 946-952, Sep. 
2024, doi: 10.38035/rrj.v7i2.1395. 
[10] S. H. Bakhtiar and A. N. Adilah, 
"Fenomena Judi Online : Faktor, Dampak, 
Pertanggungjawaban Hukum," 
Innovative, vol. 4, pp. 1016-1026, Sep. 
2024, doi: 
10.31004/innovative.v4i3.10547. 
[11] I. Savolainen, A. Sirola, I. Vuorinen, E. 
Mantere, and A. Oksanen, "Online 
Communities and Gambling Behaviors - 
a Systematic Review," Curr Addict Rep, 
vol. 9, Sep. 2022, doi: 10.1007/s40429022-00430-x. 
[12] A. S. Wardani, "Kominfo Blokir Lebih dari 
810 Ribu Konten Judi Online, Ajak Semua 
Pihak Kerja Bareng," Sep. 2024, 
Liputan6. [Online]. Available: 
https://www.liputan6.com/tekno/read/550
2510/kominfo-blokir-lebih-dari-810-ribukonten-judi-online-ajak-semua-pihakkerja-bareng 
[13] J. Devlin, M.-W. Chang, K. Lee, and K. 
Toutanova, "BERT: Pre-training of Deep 
Bidirectional Transformers for Language 
Understanding," 2019. doi: 
10.48550/arXiv.1810.04805. 
[14] G. F. Situmorang and R. Purba, "Deteksi 
Potensi Depresi dari Unggahan Media 
Sosial X Menggunakan IndoBERT," 
Building of Informatics Technology and 
Science (BITS), vol. 6, pp. 649-661, Sep. 
2024, doi: 10.47065/bits.v6i2.5496. 
[15] A. R. Hanum et al., "Analisis Kinerja 
Algoritma Klasifikasi Teks Bert dalam 
Mendeteksi Berita Hoaks," Jurnal 
Teknologi Informasi dan Ilmu Komputer, 
vol. 11, pp. 537-546, Sep. 2024, doi: 
10.25126/jtiik.938093. 
[16] D. Retnoningrum, D. A. Putri, I. Budi, A. 
B. Santoso, and P. K. Putra, "Stance 
Analysis of Policies Related to Emission 
Test Obligations using Twitter Social 
Media Data," Jurnal Nasional Pendidikan 
Teknik Informatika (JANAPATI), vol. 12, 
pp. 472 -481, Sep. 2024, doi: 
10.23887/janapati.v12i3.69004. 
[17] Samuel and D. P. Kristiadi, "Deteksi Teks 
Promosi Judi Online Menggunakan Ai 
Dengan Kombinasi NLP Dan Deep 
Learning," Jurnal Sistem Informasi dan

---


<!-- PAGE 13 -->

G. F. Situmorang et al. 
An Intelligent System for Detecting Online Gambling Promotion … 
 
JURNAL NASIONAL PENDIDIKAN TEKNIK INFORMATIKA: JANAPATI | 691 
 
Teknologi  (SINTEK), vol. 5, pp. 179-185, 
Sep. 2025, doi: 10.56995/sintek.v5i2.179. 
[18] P. Teppap, P. Tipauksorn, S. Surathong, 
W. Ponglangka, and P. Luekhong, 
"Automating Hidden Gambling Detection 
in Web Sites: A BeautifulSoup 
Implementation," pp. 132 -139. doi: 
10.1109/JCSSE61278.2024.10613687. 
[19] A. Widiyanto, M. Prameswari, and A. 
Latief, "Gambling Comments Detection 
on Youtube: A Comparative Study of 
TreeBased Boosting, LSTM and GRU 
Models," JUTI, vol. 23, pp. 144-160, doi: 
10.12962/j24068535.v23i2.a1305. 
[20] A. R. Perez et al., "Aligning Word 
Embeddings from BERT to 
VocabularyFree Representations," pp. 
108-115. doi: 
10.1109/CSCE60160.2023.00023. 
[21] S. Gururangan et al., "Don't Stop 
Pretraining: Adapt Language Models to 
Domains and Tasks," 2020 , doi: 
10.48550/arXiv.2004.10964. 
[22] J. Liang, A. Martinez, and H. Morita, 
"Language Model Adaptation for 
Downstream Tasks using Text Selection," 
Sep. 2022, pp. 320 -323. doi: 
10.1109/icnlp55136.2022.00058. 
[23] K. S. Nugroho, A. Y. Sukmadewa, H. 
Wuswilahaken DW, F. A. Bachtiar, and N. 
Yudistira, "BERT Fine -Tuning for 
Sentiment Analysis on Indonesian Mobile 
Apps Reviews," Sep. 2021. doi: 
10.1145/3479645.3479679. 
[24] A. Ladkat, A. Miyajiwala, S. Jagadale, R. 
A. Kulkarni, and R. Joshi, "Towards 
Simple and Efficient Task-Adaptive Pretraining for Text Classification," 
Association for Computational 
Linguistics, 2022, pp. 320 -325. doi: 
10.18653/v1/2022.aacl-short.39. 
[25] H. Xu, S. Ebner, M. A. Yarmohammadi, A. 
S. White, B. Van Durme, and K. Murray, 
"Gradual fine-tuning for low -resource 
domain adaptation," ArXiv, vol. 
abs/2103.02205, 2021, doi: 
10.48550/arXiv.2103.02205. 
[26] T. Wibowo, D. Nurjanah, and H. 
Nurrahmi, "Identification of misogyny on 
social media in indonesian using 
bidirectional encoder representations 
from transformers (BERT)," 2023, pp. 
401-406. doi: 
10.1109/ICAIIC57133.2023.10067106. 
[27] F. Baharuddin and M. F. Naufal, "FineTuning IndoBERT for Indonesian Exam 
Question Classification Based on Bloom's 
Taxonomy," Journal of Information 
Systems Engineering and Business 
Intelligence, vol. 9, pp. 253-263, Sep. 
2023, doi: 10.20473/jisebi.9.2.253-263. 
[28] A. Zevana and D. Riana, "Text 
Classification Using IndoBERT Fine -
tuning Modeling with Convolutional 
Neural Network And Bi-LSTM," Jurnal 
Teknik Informatika (Jutif), vol. 4, pp. 
1605-1610, Sep. 2024, doi: 
10.52436/1.jutif.2023.4.6.1650.
