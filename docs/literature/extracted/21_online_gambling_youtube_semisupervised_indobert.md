---
title: "Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification"
slug: "21_online_gambling_youtube_semisupervised_indobert"
authors: "Satriadi Putra Santika, Muhammad Alfhi Saputra, Amalia Zahra, Derwin Suhartono"
year: 2025
venue: "Procedia Computer Science (Elsevier), Vol. 269, pp. 1269–1278 / The 10th International Conference on Computer Science and Computational Intelligence (ICCSCI 2025)"
doi: "10.1016/j.procs.2025.09.068"
category: "Online Gambling (Judol) Detection"
tags: ["online-gambling", "judol", "youtube-comments", "indobert", "semi-supervised-learning", "pseudo-labeling", "svm", "cnn", "text-classification", "procedia-computer-science"]
total_pages: 10
character_count: 24500
word_count: 3820
source_file: "Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification.pdf"
extraction_date: "2026-10-20 15:58:00"
---

# Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification

## Metadata & Bibliographic Overview
- **Authors:** Satriadi Putra Santika, Muhammad Alfhi Saputra, Amalia Zahra, Derwin Suhartono
- **Affiliation:** Computer Science Department, BINUS Graduate Program & School of Computer Science, Bina Nusantara University, Jakarta, Indonesia
- **Publication Year:** 2025
- **Venue / Journal:** Procedia Computer Science 269 (2025) 1269–1278 (Elsevier) / The 10th International Conference on Computer Science and Computational Intelligence (ICCSCI 2025)
- **DOI / Link:** [https://doi.org/10.1016/j.procs.2025.09.068](https://doi.org/10.1016/j.procs.2025.09.068)
- **Category:** Online Gambling (Judol) Detection
- **Original Source File:** `Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification.pdf` (10 pages)
- **Data Availability:** Zenodo Repository, DOI: [10.5281/zenodo.15424844](https://doi.org/10.5281/zenodo.15424844)

## Agent Quick-Scan / Executive Takeaways
> [!IMPORTANT]
> **Core Relevance to This Thesis (*Evaluasi Ketahanan Model Deteksi Promosi Judi Online...*):**
> 1. **Identical Domain & Problem Statement:** Explores Indonesian online gambling (judol) promotion detection specifically on YouTube comments collected organically via YouTube Data API v3 without keyword filtering bias.
> 2. **Baseline Model Alignment:** Directly compares **IndoBERT** against **TF-IDF + SVM**, **CNN**, **LSTM**, **RNN**, and **Random Forest**.
> 3. **Critical Finding on Low-Resource / Short Text:** In the initial supervised setting with limited labeled data (10%), **TF-IDF + SVM slightly outperformed IndoBERT** (SVM F1 = 0.972 vs IndoBERT F1 = 0.961), proving that linear bag-of-words classifiers remain highly competitive on short social media spam.
> 4. **Semi-Supervised Scaling:** By utilizing pseudo-labeling on the remaining 90% unlabeled data, retrained IndoBERT achieved dominant state-of-the-art results: **Accuracy 0.986, Precision 0.991, Recall 0.980, F1-Score 0.985**.
> 5. **Direct Research Gap for Your Thesis:** Section 4 (*Conclusion and Future Works*) explicitly states:
>    > *"the current model has not yet been tested in real-time or integrated environments, and **it does not incorporate mechanisms to extract specific site names or adapt to evolving language patterns used to evade moderation**."*
>    **This sentence is the exact justification for your thesis topic**: evaluating model robustness against intentional text evasion / obfuscation (O1 Character Substitution, O2 Spelling/Noise, O3 Whitespace Manipulation, O4 Unicode Homoglyphs).

### Key Thematic Dimensions
- **Domain:** Online Gambling (Judol) Detection on Indonesian YouTube Comments
- **Methodology Focus:** IndoBERT (`indobenchmark/indobert-base-p2`), Semi-Supervised Learning, Pseudo-Labeling, SVM comparison, CNN baseline
- **Relevance Anchors in Repo:**
  - Stage 8 (YouTube comment dataset collection & annotation guidelines)
  - Stage 9 (Linear SVM vs IndoBERT baseline architectures)
  - Stage 10 & 11 (Motivation for adversarial obfuscation evaluation as an open research gap)

---

# Full Extracted Document Text

<!-- PAGE 1 -->

**ScienceDirect**  
*Procedia Computer Science 269 (2025) 1269–1278*  
Available online at www.sciencedirect.com  
1877-0509 © 2025 The Authors. Published by Elsevier B.V.  
This is an open access article under the CC BY-NC-ND license (https://creativecommons.org/licenses/by-nc-nd/4.0)  
Peer-review under responsibility of the scientific committee of the 10th International Conference on Computer Science and Computational Intelligence (ICCSCI) 2025  
DOI: 10.1016/j.procs.2025.09.068  

### The 10th International Conference on Computer Science and Computational Intelligence 2025

# Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification

**Satriadi Putra Santika**$^{a,*}$, **Muhammad Alfhi Saputra**$^b$, **Amalia Zahra**$^a$, **Derwin Suhartono**$^b$  
$^a$ *Computer Science Department, BINUS Graduate Program - Master of Computer Science, Bina Nusantara University, Jakarta, Indonesia 11480*  
$^b$ *Computer Science Department, School of Computer Science, Bina Nusantara University, Jakarta, Indonesia 11480*  

\* Corresponding author. Tel.: +62-856-9796-3024. E-mail address: satriadi.santika@binus.ac.id

---

## Abstract
The widespread promotion of online gambling through user-generated content on social media platforms has raised significant concerns, especially in regions with high internet penetration such as Indonesia. This research proposes a classification-based approach to detect online gambling promotional content in Indonesian-language YouTube comments using a semi-supervised learning strategy. A total of 10,101 comments were collected, of which 10% were manually labeled as either Promotion or Non-Promotion. Initial training using only the labeled data employed IndoBERT, a pre-trained language model for Bahasa Indonesia, which achieved an accuracy of 0.953, precision of 0.945, recall of 0.977, and F1-score of 0.961. Although the baseline performance was strong, the IndoBERT model was slightly outperformed by the SVM classifier. To address the limitations of labeled data, pseudo-labeling was applied to the remaining unlabeled data, which was then combined with the labeled subset to retrain the IndoBERT model. The evaluation results showed a significant improvement in classification performance after semi-supervised training, achieving an accuracy of 0.986, precision of 0.991, recall of 0.980, and F1-score of 0.985, surpassing all previously tested models. These findings highlight the effectiveness of IndoBERT in understanding informal online language and the advantage of semi-supervised learning in resource-constrained annotation scenarios.

**Keywords:** Classification; IndoBERT; Online Gambling; Semi-Supervised Learning; YouTube

---

## 1. Introduction
Social media has now become an integral part of the daily lives of Indonesians. The rapid development of technology, accompanied by the emergence of various new social media platforms, has increased people's dependence

---

<!-- PAGE 2 -->

on social media. Many individuals in Indonesia spend their free time surfing, interacting or seeking entertainment on various digital platforms. According to a report from We Are Social [1] by early 2025, Indonesia will have 143 million active social media users or about 50.2% of the total population. This percentage shows that social media has become one of the main communication and entertainment tools in Indonesia. Not only that, according to Digital Global Overview [2] in 2024, social media users in Indonesia spend an average of 191 minutes using social media. This figure exceeds the global average of 143 minutes. This indicates the high dependency of Indonesians on social media, which significantly affects communication patterns, information dissemination, and public opinion formation in the modern era.

Among various social media platforms, YouTube is the number one online video platform in Indonesia with 139 million users [3]. YouTube's dominance as the primary source of video entertainment and information is unwavering, making it a very important platform for marketers, content creators, and digital businesses to reach a wide audience. This popularity is also supported by YouTube's characteristics that allow users to not only passively access content, but also actively interact through comments, likes, and sharing features [4]. With a very large number of active users and a high duration of usage time, YouTube has developed into a digital public space where various opinions, information, and promotions circulate freely. However, this open access has been utilized by certain parties to insert illegal content, including online gambling promotions.

Online gambling refers to any form of gambling activity conducted over the internet, using devices such as mobile phones, laptops or tablets [5]. Compared to conventional gambling, online gambling has characteristics such as high accessibility, anomalousness, time flexibility, and online interaction opportunities that make it more difficult to control. In the context of social media, this practice often appears in the form of hidden promotions in the comments section, as is rampant on the YouTube platform.

Director of the Communication and Information System Security Research Center (CISSReC), Pratama Persadha, stated that YouTube's comment section is now the main target for spreading online gambling spam due to the high level of user engagement on the platform [6]. These comments generally contain links or invitations to join certain gambling sites with the lure of huge profits and are often spread using automated bots or fake accounts to reach more users at low cost. In response to this phenomenon, cybersecurity expert Alfons Tanujaya suggested that content creators moderate or filter the comment section [6]. However, this step can be inefficient when the number of comments reaches tens of thousands because it requires large resources and a lot of time. Given these limitations, if the trend of spreading online gambling promotions through YouTube comments is not addressed promptly, the impact may become increasingly widespread and difficult to contain. This condition highlights the urgency of developing an automatic detection system that can accurately and efficiently identify online gambling promotion content.

Detection of harmful content on social media, such as hate speech, hoaxes, and online gambling promotions, is mostly done with Natural Language Processing (NLP) approaches. This technology continues to grow along with the increasing need for automated surveillance systems on social media. Various methods have been applied in previous studies, ranging from conventional machine learning to deep learning-based models. Detection of Indonesian online gambling comments has been explored using various vectorization methods and classification models, with the best result obtained from the combination of TF-IDF and Random Forest, achieving an F1-Score of 96.1% [7]. Similarly, comment detection in Roman Urdu and Urdu has been evaluated using both conventional machine learning and deep learning approaches, where CNN outperformed SVM, Naïve Bayes, and LSTM [8]. Turning to more complex models, IndoBERT was used for fake news classification and achieved 94.66% accuracy [9], demonstrating the power of the Transformer model in understanding the Indonesian context. IndoBERT has also been used for emotion detection in social media comments, achieving an F1-Score of 78% [10]. In another study, IndoBERT was combined as a feature extractor with MBERT as a classifier for multilabel classification of toxic comments in Indonesian, resulting in an F1-Score of 90.32% on the testing data [11].

Another challenge in malicious content detection on social media is the limitation of labeled data, especially when the data is obtained directly through crawling or scraping processes. Therefore, some studies started to apply semi-supervised learning approaches for text classification tasks. A combination of BERT, MixMatchNL, and Focal Loss has been proposed for sentiment classification of unbalanced short texts, achieving 93.67% accuracy on the Amazon Reviews dataset and 93.35% on the Chrome Reviews dataset [12]. Meanwhile, a BERT-based Context-Aware Aspect and Sentiment Classification (CASC) method with semi-automatic labeling using seed words was introduced,

---

<!-- PAGE 3 -->

outperforming the baseline model with a Macro F1 of 77.53% on the Restaurant dataset and 72.23% on the Laptop dataset [13].

Although various studies have shown the effectiveness of NLP in social media comment classification, most of the previous research still has limitations. Some of them have not utilized Transformer-based models such as BERT to specifically detect online gambling promotions. The study [7] has highlighted this issue, but still uses classical approaches such as TF-IDF and RF. In addition, the limited availability of labeled data in social media comments remains a challenge, as the manual labeling process is not only time-consuming but also requires the involvement of domain experts. Moreover, their data collection relies on keyword-based queries on Twitter, which can lead to biased representations where the most frequent words are inherently influenced by the search terms used. In contrast, this study utilizes YouTube comment data collected from trending videos, where online gambling promotions appear organically without keyword filtering, offering a more natural and unbiased depiction of how such content is disseminated in real-world online environments. Therefore, the adoption of a semi-supervised approach becomes a strategic step to enhance scalability while maintaining labeling quality.

Based on the limitations of previous studies, this research proposes an online gambling promotion detection system in Indonesian YouTube comments by utilizing IndoBERT-based classification. To address the scarcity of labeled data, a semi-supervised learning approach is adopted, enabling the model to be trained effectively with minimal annotation. This approach is expected to accurately identify promotional comments related to online gambling while reducing dependency on costly and time-consuming manual labeling processes.

## 2. Method
This research proposes an online gambling promotion detection method on YouTube comments using an IndoBERT-based semi-supervised approach. The methodology flow is depicted in Fig. 1, which begins with the process of data collection and data preprocessing to clean and standardize the YouTube comment text. A descriptive analysis is then performed to explore frequently occurring words, which helps understand linguistic patterns in online gambling promotion. After that, initial supervised training is carried out using a small portion of manually labeled data. The trained model is then used to generate pseudo-labels for the unlabeled data. Both the labeled and pseudo-labeled data are combined and used in the semi-supervised training phase to retrain the classification model with a larger dataset. Finally, the model is evaluated using appropriate classification metrics to measure its performance in detecting promotional comments accurately.

```text
[ Data Collecting ] -> [ Data Preprocessing ] -> [ Descriptive Analysis ] -> [ Initial Supervised Training ] -> [ Semi-Supervised Training ] -> [ Model Evaluation ]
```
*Fig. 1 General Research Stages*

### 2.1. Data Collecting
Data collection in this study was carried out by utilizing the YouTube Data API v3 through the Google Cloud Platform (GCP) service. This research targets the collection of 10,000 Indonesian-language comments from videos that are considered relevant and at high risk of being a place to spread online gambling promotions. The focus of data collection was on 10 trending videos in the gaming category as of May 5, 2025. The selection of this category is based on the KOL.ID report [14] which shows that the gaming category is one of the preferred contents for millennials, with a percentage of 45.7%. On the other hand, data from the Financial Transaction Reports and Analysis Center [15] states that 30 - 50 years old is the largest contributor to online gambling players with a percentage of 40%. The high interest in gaming content among users, especially those in the age range most involved in online gambling activities, makes this category a great potential target for promotion by online gambling players. The combination of content popularity and demographic relevance is the main reason for selecting videos in the gaming category as the source of YouTube comment data in this study.

---

<!-- PAGE 4 -->

After the comment data was collected, 10% of the total dataset was manually labeled into two classes, which are online gambling Promotion and Non-Promotion. The labeling process was carried out by the first author with several indicators. A comment is categorized as Promotion if it contains the name of online gambling site which generally consists of a combination of letters at the beginning and numbers at the end, invitations to play like “main” (play), “gampang” (easy), “coba” (try), or the use of terms that are closely related to online gambling, such as “jepe” (jackpot), “nagih” (addict), or “slot” (refers to online gambling). Meanwhile, comments that have no indication of online gambling promotion are categorized as Non-Promotion. Simple labeling guidelines were established to maintain consistency during annotation and ambiguous cases were manually reviewed. To ensure accuracy, all labeled data will be double-checked by annotators to reduce subjectivity and minimize labeling errors. This annotated subset serves as the initial supervised dataset used to train a baseline classification model.

### 2.2. Data Preprocessing
Data preprocessing is a series of steps used to clean, integrate, transform, and reduce data before it is used in the model training process [16]. This stage is crucial because the use of data that has not been properly prepared can result in erroneous information and suboptimal model performance [17]. Moreover, the quality of the data will be further degraded if there is a lot of meaningless information or noise in it [18]. Therefore, understanding and applying the right preprocessing procedure according to the context of the case study is very important to ensure the quality of the data used.

In this research, comment data from YouTube is processed through a series of text cleaning stages. Fig. 2 illustrates the results of the data preprocessing applied in this study. These stages include unicode character conversion, removal of emojis, URLs, foreign characters, and symbols, as well as the merging of gambling promotion keywords that are separated by spaces. The text is then normalized to lowercase, followed by tokenization and stemming to return words to their base forms. An unslang process is also applied using a simple slang dictionary, which replaces abbreviated forms such as “ad” with “ada” or “adlh” with “adalah.” Finally, stop word removal is performed to eliminate non-informative words. All preprocessing steps are applied consistently to ensure high-quality input for model training. After preprocessing, the dataset is split into training, validation, and test sets using a 7:1.5:1.5 ratio.

```text
[ Raw Text ] -> [ Clean Text ] -> [ Tokenized ] -> [ Stemmed ] -> [ Unslang ] -> [ Processed Text ]
```
*Fig. 2 Data Preprocessing Steps*

### 2.3. Descriptive Analysis
In the context of NLP, descriptive analysis is used to explore word distribution and understand language patterns contained in a text corpus [19]. This stage is important as an initial step in identifying keywords that are often used, especially in comments containing online gambling promotions. One technique that is often done in descriptive analysis of text data is through word cloud visualization. Word cloud is a text visualization used to summarize the content of a document into a visual representation of the most important words [20]. The size of each word in the word cloud is scaled proportionally based on its frequency in the text so that words that appear more frequently will be displayed in a larger size. This research uses word cloud visualization to intuitively display the frequency of word occurrence. The results of the word cloud provide an initial insight into the language strategies used by the perpetrators, such as the use of site names, promotional invitations, and gambling terms.

---

<!-- PAGE 5 -->

### 2.4. Initial Supervised Training
As an initial stage, a supervised training approach is performed by training the model using 10% of the total dataset that has been labeled to build an initial classification model. The model used in this research is IndoBERT, a pre-trained language model based on the Bidirectional Encoder Representations from Transformers (BERT) architecture built on the Transformers model and trained on the Indo4B dataset [21]. The Indo4B dataset includes Indonesian sentences in both formal and informal forms, allowing IndoBERT to better understand the language context [9]. In addition, the syntax-aware attention inherent in the BERT architecture also strengthens its ability to capture complex language structures [22].

Fig. 3 shows the architecture of the classification model used in this study, utilizing IndoBERT as a pre-trained language model and fine tuning the output layer. The processed YouTube comment text is first tokenized using the BERT tokenizer, then fed into IndoBERT which consists of 12 Transformer encoder layers with 12 self-attention heads in each layer. Next, the representation of all comments that have been processed by IndoBERT is forwarded to a fully connected layer with 1 neuron and sigmoid activation. This layer produces a binary prediction to determine whether a comment is an online gambling promotion or not. The model will be trained for 10 epochs with a batch size of 16. The training process is carried out using the Adam optimizer with a learning rate of 10e-5. The loss function used is Binary Cross-Entropy because the classification task is binary.

```text
[ Processed YouTube Comment ] -> [ BERT Tokenizer ] -> [ IndoBERT Pre-Trained Model ] -> [ BERT Sequence Classification Head ] -> [ Output: Promotion / Non-Promotion ]
```
*Fig. 3 Model Architecture*

### 2.5. Semi-Supervised Training
At this stage, the model obtained from the initial training is used to pseudo-label the unlabeled YouTube comment text. Pseudo-labeling is a technique in semi-supervised learning that utilizes model predictions to provide temporary labels on unlabeled data so that the data can be reused in the training process [23]. The pseudo-labeling results are then combined with manually labeled data and retrained using the same model architecture. This strategy is applied to overcome the limited amount of labeled data and improve classification performance by efficiently utilizing information from unlabeled data [12].

### 2.6. Model Evaluation
The classification model was evaluated using accuracy, precision, recall, F1-score, and confusion matrix to measure its ability to distinguish between promotional and non-promotional comments comprehensively. These metrics aim to assess the ratio of correct predictions to total predictions, the precision of identifying positive class, the sensitivity in detecting positive instances, and the overall balance between them [24,25]. The accuracy, precision, recall, and F1-score formulas are presented in equations (1), (2), (3), and (4), respectively [24].

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \tag{1}$$

$$\text{Precision} = \frac{TP}{TP + FP} \tag{2}$$

$$\text{Recall} = \frac{TP}{TP + FN} \tag{3}$$

$$F1\text{-score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \tag{4}$$

---

<!-- PAGE 6 -->

## 3. Results and Discussion

### 3.1. Dataset Summary
As described in the previous section, this research uses data collected from the YouTube platform. The dataset collected was 10,101 comments. From all the data, 10% of the data was randomly selected to be labeled manually. Approximately 1,010 YouTube comments were labeled manually. The entire dataset is then pre-processed to improve data consistency and reduce noise in the dataset. The preprocessing stages carried out are in accordance with those described in the previous section. The remaining dataset after preprocessing is 9,880 data. Examples of datasets and preprocessing results can be seen in Table 1.

**Table 1. Sample Dataset**
| Raw Text (Indonesian) | Raw Text (English) | Processed Text (Indonesian) | Processed Text (English) | Label |
|---|---|---|---|:---:|
| Tadi iseng coba ikutin saran teman gw main di **BAZARTOTO** ternyata beneran di kasih Jepe wkwk, makasih bro | I was just trying to follow my friend's advice to play in **BAZARTOTO** and it turned out to be true wkwk, thanks bro | iseng coba ikutin saran teman main bazartoto nyata beneran kasih jepe wkwk terima kasih saudara laki-laki | idly trying to follow the advice of friends playing real bazartoto really love jepe wkwk thank you brother | 1 |
| Promosi game genshin impact tapi lagunya intro blue archive | Genshin impact game promotion but the song is blue archive intro | iklan genshin impact backsound blue archive | genshin impact advertising blue archive backsound | 0 |

### 3.2. Descriptive Analysis
Descriptive analysis is performed on datasets that have been manually labeled, meaning that 10% of the total dataset is subjected to descriptive analysis. Based on the word cloud for the Promotion class, which can be seen in Fig. 4(a), some of the dominating words are the names of online gambling sites, such as “alexis17”, “weton88”, and “sgi88”. In addition, there are also words that are invitations or describe the benefits of online gambling to attract the attention of YouTube viewers, such as “jepe” (jackpot), “menang” (win), “main” (play), and “auto sultan” (get rich). These words show that online gambling promotional comments tend to display information that attracts readers to try the online gambling service. Conversely, in Fig. 4(b), the word cloud of the Non-Promotion class shows words that are more diverse and not focused on a particular tone or theme. Some of the words that dominate the Non-Promotion class dataset tends to be neutral, such as “bang” (Brother), “konten” (content), “nonton” (watch), and “blazer”, which is the nickname of one of the people on the YouTube channel that is the source of this dataset. From these words, it can be assessed that there is no information that indicates promotion.

*Fig. 4 Word Cloud (a) Promotion Class, dominating words: alexis17, weton88, sgi88, jepe, menang, main, coba; (b) Non-Promotion Class, dominating words: bang, blazer, konten, nonton, nya.*

### 3.3. Initial Supervised Training Result
The manually labeled dataset, comprising 10% of the total preprocessed data, is initially used to train several machine learning and deep learning models. Before training, a review of the label distribution is conducted to evaluate

---

<!-- PAGE 7 -->

the balance of the dataset. Based on the distribution results, it is known that the Promotion class consists of 580 comments, or about 58.7% of the total labeled data. Meanwhile, the Non-Promotion class consists of 408 comments, or about 41.3%. In the research of Buda et al. [26], systematically evaluated the impact of data imbalance in the case of classification and defined the data imbalance ratio with $\rho = 2$. It is implicitly said that the dataset starts to imbalance when it starts to reach a ratio of 1:2. The data distribution ratio in this initial training does not reach 1:2, meaning that it can be said that the dataset still does not fall into the imbalance category. Therefore, the dataset does not need to be applied to data balancing techniques and can be directly trained. Following this, model training was conducted, and the evaluation results of the initial supervised training are presented in Table 2.

**Table 2. Initial Supervised Training Result (10% Labeled Data)**
| Model | Accuracy | Precision | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|
| **TFIDF + SVM** | **0.966** | **0.988** | 0.956 | **0.972** |
| TFIDF + Logistic Regression | 0.946 | 0.966 | 0.945 | 0.956 |
| TFIDF + XGBoost | 0.946 | 0.966 | 0.945 | 0.956 |
| TFIDF + Random Forest | 0.953 | 0.967 | 0.956 | 0.961 |
| RNN | 0.959 | 0.957 | 0.978 | 0.967 |
| LSTM | 0.939 | 0.936 | 0.967 | 0.951 |
| CNN | 0.959 | 0.957 | 0.978 | 0.967 |
| **IndoBERT** | 0.953 | 0.945 | 0.977 | 0.961 |

The training results show that all models get relatively good results on each measurement metric. The best performing model is SVM, which has an accuracy of 0.966, a precision of 0.988, and an F1-score of 0.972. Despite being a relatively simple model, SVM showed competitive performance in this experiment. This can be explained by the characteristics of YouTube comments, which are short, straightforward, and have a less complex language structure. In addition, SVM is known to have stable performance in binary classification, especially in cases with limited data size. These results indicate that in low-resource scenarios, classical models such as SVM can still be a reliable model choice before moving on to more complex models [27].

Meanwhile, the IndoBERT model, which is the primary focus of this research, gets an accuracy value of 0.953, precision 0.945, recall 0.977, and F1-Score 0.961, already getting good results, but still cannot be said to be the best model. Based on the confusion matrix of the IndoBERT model results in Fig. 5, the Confusion matrix shows that the model successfully classified 87 Promotion comments correctly and only misclassified two comments. Meanwhile, in the Non-Promotion class, 55 comments were recognized correctly, and five comments were misclassified as Promotion. In general, these results show that with limited data, the initial model has been able to perform classification with a good level of accuracy and consistency. This result is also a strong foundation to continue to the automatic labeling stage to complete the semi-supervised learning process in the next stage.

*Fig. 5 Confusion Matrix of IndoBERT Model (Initial Supervised Training):*
- True Non-Promotion: 55 correct (TN), 5 misclassified as Promotion (FP)
- True Promotion: 87 correct (TP), 2 misclassified as Non-Promotion (FN)

---

<!-- PAGE 8 -->

### 3.4. Final Model Evaluation
After completing the initial supervised training stage, each trained model was then utilized to pseudo-label the previously unlabeled dataset. In this step, each model independently generated label predictions for the remaining data based on its own classification results. The pseudo-labeling outcome shows that the class distribution remains relatively balanced, consisting of 4,144 comments labeled as Promotion (46.6%) and 4,748 as Non-Promotion (53.4%). Following this, each model was retrained using the newly generated dataset from its own pseudo-labeling output, completing the semi-supervised learning process. The performance of each model after retraining was evaluated using the same metrics applied in the initial stage. The results show improved performance in all models, with IndoBERT achieving the highest accuracy of 0.986, precision 0.991, recall 0.980, and F1-score 0.985. The performance comparison between models is shown in Table 3.

**Table 3. Semi-Supervised Classification Result (After Pseudo-Labeling)**
| Model | Accuracy | Precision | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|
| TFIDF + SVM | 0.965 | 0.979 | 0.951 | 0.965 |
| TFIDF + Logistic Regression | 0.964 | 0.985 | 0.947 | 0.966 |
| TFIDF + XGBoost | 0.967 | 0.969 | 0.997 | 0.983 |
| TFIDF + Random Forest | 0.981 | 0.985 | 0.978 | 0.981 |
| RNN | 0.969 | 0.968 | 0.973 | 0.971 |
| LSTM | 0.968 | 0.964 | 0.975 | 0.970 |
| CNN | 0.966 | 0.973 | 0.967 | 0.970 |
| **IndoBERT** | **0.986** | **0.991** | **0.980** | **0.985** |

Further evaluation is presented in the confusion matrix of the IndoBERT model with pseudo-labeling, as shown in Fig. 6. The matrix illustrates the model's performance on 1,482 test samples. A total of 686 Promotion comments were correctly classified, while 14 Promotion comments were misclassified as Non-Promotion. On the other hand, the model also correctly identified 776 Non-Promotion comments and only 6 instances were misclassified as Promotion. These results indicate that the model performs reliably in distinguishing between promotional and non-promotional content, with a relatively low number of misclassifications across both classes.

*Fig. 6 Confusion Matrix of IndoBERT Model (Semi-Supervised Training):*
- True Non-Promotion: 776 correct (TN), 6 misclassified as Promotion (FP)
- True Promotion: 686 correct (TP), 14 misclassified as Non-Promotion (FN)

The application of the semi-supervised approach through pseudo-labeling has been shown to have a positive impact on the performance of all tested models. Although theoretically there is a risk of accumulative error due to the use of model predictions as new labels, experimental results show that the retraining process actually improves the model capabilities consistently [28]. This is likely due to the significantly increased amount of training data, as well as the similarity in distribution between the labeled data and the resulting pseudo-labeled data. Among all the models,

---

<!-- PAGE 9 -->

IndoBERT showed the most superior performance post-retraining. It successfully outperformed the other models on all evaluation metrics, including accuracy, precision, recall, and F1-score. This dominance suggests that IndoBERT's contextual representation is highly effective in capturing the distinctive linguistic patterns in Indonesian YouTube comments.

## 4. Conclusion and Future Works
This study proposed a classification approach for detecting online gambling promotion in Indonesian YouTube comments using the IndoBERT model with a semi-supervised learning strategy. The experimental results demonstrated that the model trained on 10% manually labeled data already achieved a strong baseline performance. Furthermore, the application of pseudo-labeling and retraining using the remaining unlabeled data improved the classification performance across all evaluation metrics, including accuracy, precision, recall, and F1-score. These findings indicate that the combination of IndoBERT and semi-supervised learning is effective in detecting promotional content related to online gambling, even under conditions of limited labeled data. The model also showed the ability to generalize well on noisy, informal, user-generated text commonly found on social media platforms.

However, the current model has not yet been tested in real-time or integrated environments, and it does not incorporate mechanisms to extract specific site names or adapt to evolving language patterns used to evade moderation. In the future, this model can be further developed as an extension tool to support efforts in identifying and automatically filtering or blocking online gambling promotional comments on public platforms such as YouTube. The addition of Named Entity Recognition (NER) can further enhance this tool by enabling the extraction of specific gambling-related terms or site names. Its integration into moderation systems can assist the public, platform providers, and regulatory bodies in reducing the spread of illegal gambling content.

### Data Availability
Dataset is available from the Zenodo Repository, DOI: [10.5281/zenodo.15424844](https://doi.org/10.5281/zenodo.15424844).

### Author Contribution Statement
**S. P. Santika:** Conceptualization, Methodology, Data curation, Resources, Writing – original draft, Writing – review & editing.  
**M. A. Saputra:** Methodology, Resources, Writing – original draft, Writing – review & editing, Supervision.  
**A. Zahra:** Validation, Supervision.  
**D. Suhartono:** Validation, Supervision.

### AI Usage Declaration
We declare that we used AI tools, specifically ChatGPT by OpenAI, during the preparation of this manuscript for purposes such as grammar checking and paraphrasing suggestions. All AI-assisted outputs were carefully reviewed, edited, and verified by the authors to ensure accuracy, clarity, and academic integrity.

### Acknowledgements
This work is supported by Bina Nusantara University through the International Research Grant Program – Fundamental Scheme (*Penelitian Internasional BINUS – Dasar*) under Contract No: 069B/VRRTT/III/2024.

---

### References
- [1] Riyanto AD. (2025). "Hootsuite (We Are Social): Data Digital Indonesia 2025." We Are Social. https://andi.link/hootsuite-we-are-social-data-digital-indonesia-2025/ (Accessed: 29 April 2025).
- [2] Kemp S. (2024). "Digital 2024: Indonesia." Digital Global. https://datareportal.com/reports/digital-2024-indonesia (Accessed: 29 April 2025).
- [3] Panggabean AD. (2024). "Ini Data Statistik Penggunaan Media Sosial Masyarakat Indonesia Tahun 2024." Databoks. https://www.rri.co.id/iptek/721570/ini-data-statistik-penggunaan-media-sosial-masyarakat-indonesia-tahun-2024 (Accessed: 29 April 2025).

---

<!-- PAGE 10 -->

- [4] Montero A, Mora-Fernandez J. (2020). “Digital culture in YouTube categories and interfaces: User experience and social interactions of the most popular videos and channels.” In *Lecture Notes in Computer Science*, Vol. 12427. https://doi.org/10.1007/978-3-030-60152-2_2.
- [5] Ghelfi M, Scattola P, Giudici G, et al. (2024). “Online Gambling: A Systematic Review of Risk and Protective Factors in the Adult Population.” *Journal of Gambling Studies*, 40: 673–699. https://doi.org/10.1007/s10899-023-10258-3.
- [6] Hardiantoro A, Dzulfaroh AN. (2025). “Kolom Komentar YouTube Jadi Sasaran Spam Judi Online, Ini Penyebab dan Cara Mengatasinya.” *Kompas*. https://www.kompas.com/tren/read/2025/02/17/160000765/kolom-komentar-youtube-jadi-sasaran-spam-judi-online-ini-penyebab-dan-cara?page=all (Accessed: 29 April 2025).
- [7] Perdana RB, Ardin, Budi I, et al. (2024). “Detecting Online Gambling Promotions on Indonesian Twitter Using Text Mining Algorithm.” *International Journal of Advanced Computer Science and Applications*, 15: 942–949. https://doi.org/10.14569/IJACSA.2024.0150893.
- [8] Akhter MP, Jiangbin Z, Naqvi IR, et al. (2022). “Abusive language detection from social media comments using conventional machine learning and deep learning approaches.” *Multimedia Systems*, 28: 1925–1940. https://doi.org/10.1007/s00530-021-00784-8.
- [9] Isa SM, Nico G, Permana M. (2022). “IndoBERT for Indonesian Fake News Detection.” *ICIC Express Letters*, 16(3): 289–297. https://doi.org/10.24507/icicel.16.03.289.
- [10] Masaling NAP, Siswanto RR, Girsang AS. (2024). “Indonesian Tweet Emotion Detection Using IndoBERT.” In *Proceedings of the 2024 International Conference on Information Management and Technology (ICIMTech)*: 478–482. https://doi.org/10.1109/ICIMTech63123.2024.10780847.
- [11] Nabiilah GZ, Alam IN, Purwanto ES, et al. (2024). “Indonesian multilabel classification using IndoBERT embedding and MBERT classification.” *International Journal of Electrical and Computer Engineering*, 14(1): 1071–1078. https://doi.org/10.11591/ijece.v14i1.pp1071-1078.
- [12] Zou H, Wang Z. (2023). “A semi-supervised short text sentiment classification method based on improved BERT model from unlabelled data.” *Journal of Big Data*, 10. https://doi.org/10.1186/s40537-023-00710-x.
- [13] Kumar A, Gupta P, Balan R, et al. (2021). “BERT Based Semi-Supervised Hybrid Approach for Aspect and Sentiment Classification.” *Neural Processing Letters*, 53: 4207–4224. https://doi.org/10.1007/s11063-021-10596-6.
- [14] Fajar. (2025). “KOL.ID Report: Preferensi Konten YouTube Gen Z, Millennial, dan Generasi X di Indonesia.” *KOL.ID*. https://kol.id/blog/kol-id-report-preferensi-konten-youtube-gen-z-milenial-dan-generasi-x-di-indonesia (Accessed: 4 May 2025).
- [15] PPATK. (2024). “GAWAT! Jumlah Fantastis Usia Anak Main Judi Online.” *PPATK*. https://www.ppatk.go.id/news/read/1373/gawat-jumlah-fantastis-usia-anak-main-judi-online.html (Accessed: 4 May 2025).
- [16] Hidayat AA, Cenggoro TW, Pardamean B. (2021). “Convolutional Neural Networks for Scops Owl Sound Classification.” *Procedia Computer Science*, 179: 81–87. https://doi.org/10.1016/j.procs.2020.12.010.
- [17] Isnan M, Elwirehardja GN, Pardamean B. (2023). “Sentiment Analysis for TikTok Review Using VADER Sentiment and SVM Model.” *Procedia Computer Science*, 227: 168–175. https://doi.org/10.1016/j.procs.2023.10.514.
- [18] Bagla K, Kumar A, Gupta S, et al. (2021). “Noisy Text Data: Achilles’ Heel of Popular Transformer-Based NLP Models.” *Arxiv:Preprint*. https://arxiv.org/abs/2110.03353.
- [19] Epperson W, Mathur A, Perer A, et al. (2025). “Texture: Structured Exploration of Text Datasets.” *Arxiv:Preprint*. https://arxiv.org/abs/2504.16898.
- [20] Huber M, Nollenburg M, Villedieu A. (2023). “MySemCloud: Semantic-Aware Word Cloud Editing.” In *IEEE Pacific Visualization Symposium*, April 2023: 147–156. https://doi.org/10.1109/PacificVis56936.2023.00024.
- [21] Wilie B, Vincentio K, Winata GI, et al. (2020). “IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding.” *Arxiv:Preprint*. https://arxiv.org/abs/2009.05387.
- [22] Clark K, Khandelwal U, Levy O, et al. (2019). “What Does BERT Look at? An Analysis of BERT’s Attention.” In *Proceedings of the 2019 Workshop*, 276–286. https://doi.org/10.18653/v1/w19-4828.
- [23] Kage P, Rothenberger JC, Andreadis P, et al. (2024). “A Review of Pseudo-Labeling for Computer Vision.” *Arxiv:Preprint*. https://arxiv.org/abs/2408.07221.
- [24] Rupapara V, Rustam F, Shahzad HF, et al. (2021). “Impact of SMOTE on Imbalanced Text Features for Toxic Comments Classification Using RVVC Model.” *IEEE Access*, 9: 78621–78634. https://doi.org/10.1109/ACCESS.2021.3083638.
- [25] Foody GM. (2023). “Challenges in the Real World Use of Classification Accuracy Metrics: From Recall and Precision to the Matthews Correlation Coefficient.” *PLoS ONE*, 18. https://doi.org/10.1371/journal.pone.0291908.
- [26] Buda M, Maki A, Mazurowski MA. (2018). “A Systematic Study of the Class Imbalance Problem in Convolutional Neural Networks.” *Neural Networks*, 106: 249–259. https://doi.org/10.1016/j.neunet.2018.07.011.
- [27] Zhang Y, Wallace B. (2015). “A Sensitivity Analysis of (and Practitioners’ Guide to) Convolutional Neural Networks for Sentence Classification.” *Arxiv:Preprint*. https://arxiv.org/abs/1510.03820.
- [28] Sohn K, Berthelot D, Li CL, et al. (2020). “FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence.” In *Advances in Neural Information Processing Systems*, December 2020.
