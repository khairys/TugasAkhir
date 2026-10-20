---
title: "MOJI: Character-Level Convolutional Neural Networks for Malicious Obfuscated JavaScript Inspection"
slug: "17_moji_character_level_cnn_obfuscation"
authors: "Minato Ishida, Naoshi Kaneko, Kazuhiko Sumi"
year: 2023
venue: "Applied Soft Computing (Elsevier), Vol. 137, Art. 110138"
doi: "10.1016/j.asoc.2023.110138"
category: "Character-Level CNN & Obfuscation"
tags: ["character-cnn", "obfuscation-resilience", "deep-learning", "n-grams", "feature-extraction"]
total_pages: 12
character_count: 57240
word_count: 3709
source_file: "MOJI Character-level convolutional neural networks for Malicious.pdf"
extraction_date: "2026-10-20 15:11:29"
---

# MOJI: Character-Level Convolutional Neural Networks for Malicious Obfuscated JavaScript Inspection

## Metadata & Bibliographic Overview
- **Authors:** Minato Ishida, Naoshi Kaneko, Kazuhiko Sumi
- **Publication Year:** 2023
- **Venue / Journal:** Applied Soft Computing (Elsevier), Vol. 137, Art. 110138
- **DOI / Link:** 10.1016/j.asoc.2023.110138
- **Category:** Character-Level CNN & Obfuscation
- **Original Source File:** `MOJI Character-level convolutional neural networks for Malicious.pdf` (12 pages, ~3,709 words)

## Agent Quick-Scan / Executive Takeaways
> [!NOTE]
> **Relevance to Tugas Akhir / Research Context:**
> Primary architectural justification for Char-CNN's resilience against obfuscation. Explains why character n-gram kernels preserve structural signals even when word token boundaries and subwords are corrupted.

### Key Thematic Dimensions
- **Domain:** Character-Level CNN & Obfuscation
- **Methodology Focus:** character-cnn, obfuscation-resilience, deep-learning, n-grams, feature-extraction
- **Relevance Anchors in Repo:** Connects to Stage 8 (Data Leakage & Pairing), Stage 9 (Baseline Models), Stage 10 (Adversarial Robustness O1-O4), and Stage 11 (Domain Shift OOD).

---

# Full Extracted Document Text



<!-- PAGE 1 -->

AppliedSoftComputing137(2023)110138
Contents lists available at ScienceDirect
AppliedSoftComputing
journal homepage: www.elsevier.com/locate/asoc
MOJI:Character-levelconvolutionalneuralnetworksforMalicious
ObfuscatedJavaScriptInspection
MinatoIshida,NaoshiKaneko ∗,KazuhikoSumi
Aoyama Gakuin University, 5-10-1 Fuchinobe, Chuo-ku, Sagamihara, Kanagawa 252-5258, Japan
a r t i c l e i n f o
Article history:
Received24October2022
Receivedinrevisedform27January2023
Accepted15February2023
Availableonline21February2023
Keywords:
Malwaredetection
JavaScript
Convolutionalneuralnetworks
Deeplearning
a b s t r a c t
JavaScript malware is one of the major threats to web security. A big challenge in detecting such
malicious JavaScript is obfuscation, which transforms a program code into a harder-to-understand
representationwhilepreservingitsoriginalfunctionality.ManymaliciousJavaScriptdetectionmethods perform code abstraction and prior feature extraction to uncover the functionality hidden by
obfuscation.However,suchpreprocessingstepssignificantlylimitthedetectors'efficiencyinpractical
situations.ThispaperpresentsMaliciousObfuscatedJavaScriptInspector(MOJI),anovelmethodfor
maliciousJavaScriptdetection,whichrequiresnocodeabstractionorpriorfeatureextraction.Instead,
ourdetectordirectlyacceptsasequenceofcharactersinJavaScriptcodeasaninputandoutputsits
maliciousnessscore.Specifically,wedesignacharacter-levelconvolutionalneuralnetworkconsisting
mainlyofseveral1Dconvolutionallayersandfullyconnectedlayers.Weevaluatetheproposedmethod
onadatasetcomposedof24,000JavaScriptcodesandshowthatourmethodoutperformsexisting
malicious JavaScript detectors in terms of both detection performance and running time. We also
provideananalysisoftheeffectofadditionalobfuscationonthesamedataset.Ourresultsindicatethat
MOJIisfarmorerobusttoobfuscationthantheexistingmethodsandcommercialantivirussoftware.
©2023TheAuthor(s).PublishedbyElsevierB.V.ThisisanopenaccessarticleundertheCCBY-NC-ND
license(http://creativecommons.org/licenses/by-nc-nd/4.0/).

## 1. Introduction

1.1. Background
Fordecades,thewebhasexistedasavitalsocialinfrastructure
withmillionsofwebsitesandservices.Nowadays,mostwebsites
providedynamicandinteractivecontent,andusersenjoyeverimprovingexperiences.Oneofthekeyplayersindeliveringsuch
contentisJavaScript,afast,versatile,andpopularprogramming
languagerunningmainlyonclient-sidewebbrowsers.Itspopularity,however,attractsattackerstoabuseitsfunctionalityto
perform cyberattacks, such as drive-by-download, adware injection,andcross-sitescripting.MaliciousJavaScriptperforming
suchattacksisoneofthemajorsecuritythreats[1].Therefore,
detectingJavaScriptmalwarebeforeattacksisafundamentaland
essentialprobleminwebsecurity.
AbigchallengeinmaliciousJavaScriptdetectionisobfuscation, which transforms a program code into a harder-tounderstandrepresentation[2,3].Obfuscatedcodesmaintainthe
originalprogram'sfunctionalitywhilehavingacompletelydifferentphysicalappearance.Forexample,Fig.1showsanobfuscated
∗ Correspondingauthor.
E-mail addresses: ishida.minato@vss.it.aoyama.ac.jp(M.Ishida),
kaneko@it.aoyama.ac.jp(N.Kaneko),sumi@it.aoyama.ac.jp(K.Sumi).
JavaScriptcodeof alert(''Hello world!!'').JavaScriptmalware is often obfuscated to hide its maliciousness and avoid
detection. However, we note that obfuscation itself does not
alwaysindicatemaliciousness.Non-malicious(benign)JavaScript
codesmayalsoemployobfuscationtoreducedatasizeorhide
sensitivecontentfromusers.Therefore,detectorsshouldbeable
todiscriminatebenign/maliciousJavaScriptcodesregardlessof
obfuscation.
Traditionally,JavaScriptmalwarehasbeendetectedbypattern
matching-orrule-basedmethods[4,5].Thesemethodstendto
bevulnerabletounseenorobfuscatedattackssincethepatterns
andrulesareratherrigid.Recently,researchershaveemployed
data-drivenapproaches,especiallymachinelearningtoovercome
theshortcomingsoftraditionalmethods.Machinelearning-based
approachesarebroadlycategorizedintodynamicanalysis[6,7]
andstaticanalysis[8,9].Dynamicanalysismethods[6,7]execute
JavaScriptcodesonvirtualmachinesorsandboxenvironments
and analyze their dynamic behavior. Actual execution makes
thesedetectorsrobusttoobfuscationandletsthemreliablyfind
maliciouscodes.Atthesametime,dynamicanalysisapproaches
requireseparatedenvironmentsforexecutionandarelessefficientthanstaticanalysisapproaches.Incontrast,staticanalysis
methods [8,9] detect JavaScript malware without actual code
execution. They can be used as efficient pre-filters to screen
JavaScript codes to be sent to more time-consuming dynamic
analysis.Ourpresentworkisinlinewiththisresearchdirection.
https://doi.org/10.1016/j.asoc.2023.110138
1568-4946/©2023TheAuthor(s). PublishedbyElsevierB.V.ThisisanopenaccessarticleundertheCCBY-NC-NDlicense(http://creativecommons.org/licenses/bync-nd/4.0/).

---


<!-- PAGE 2 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Fig. 1. ObfuscatedJavaScriptcodeof alert(''Hello world!!'').
List of acronyms
AST AbstractSyntaxTree
AUC AreaUndertheCurve
BCE BinaryCrossEntropy
BiLSTM BidirectionalLongShort-TermMemory
CLCNN Character-Level Convolutional Neural Network
CNN ConvolutionalNeuralNetwork
GCN GraphConvolutionalNetwork
LSTM LongShort-TermMemory
MOJI MaliciousObfuscatedJavaScriptInspector
ReLU RectifiedLinearUnit
RNN RecurrentNeuralNetwork
ROC ReceiverOperatingCharacteristic
SVM SupportVectorMachine
Instaticanalysismethods,researchersoftenconvertJavaScript
codes into new representations to uncover their functionality
hiddenbyobfuscation.AcommonchoiceistouseAbstractSyntax
Trees(ASTs)forcodestructurerepresentation[8-16].However,
thesemethodsinherentlyrequirededicatedpreprocessingsteps
andexternaltoolstobuildASTs(suchasJavaScriptparsers[17]).
Inpracticalsituations,thesepreprocessingstepssignificantlyreducethedetectors'efficiencybecausetheytakeanon-negligible
amountoftime.
1.2. Motivation and contribution
Thisstudyaimstobuildanefficientyetaccurate,staticmaliciousJavaScriptdetector.Ourresearchquestionsareasfollows:
1. How do we build a static detector that can take source
codesdirectlyasinputs,withoutdedicatedpreprocessing
steps?
2. Issuchadetectormoreaccurateandfasterthanthepreviousstaticanalysismethods?
3. Howdoessourcecodeobfuscationaffecttheperformance
ofmaliciousJavaScriptdetectors?
To answer the first question, this paper presents Malicious
Obfuscated JavaScript Inspector (MOJI), an efficient yet accurate malicious JavaScript detector based on deep neural networks.1 Specifically, we design a character-level convolutional
neuralnetwork,whichdirectlyacceptsasequenceofcharacters
inJavaScriptcodeasaninput.Theproposednetworkismainly
composedofseveral1Dconvolutionallayersandfullyconnected
layers. Unlike existing static analysis approaches, our method
requiresnocodeabstractionorpriorfeatureextraction.Instead,
it performs simple character encoding to convert input string
charactersintotheirnumericalrepresentation.Fig.2illustrates
thedifferenceinprocessingflowsbetweenthepreviousmethods
andMOJI.
Toanswerthesecondquestion,weconductexperimentsona
dataset consisting of 12,000 benign and 12,000 malicious
1 Moji(
 )isaJapanesewordmeaning''character''.
2

---


<!-- PAGE 3 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Fig. 2. Comparison of the processing flows between the previous approaches
and MOJI. (a) The previous methods require converting JavaScript codes into
ASTs.Theyalsoneedtoperformfeatureextractionbeforeclassification.(b)MOJI
onlyrequiressimplecharacterencodingbeforeclassification.
JavaScriptcodes.Despiteitssimplicity,weshowthatMOJIoutperforms existing static analysis methods [9,11] and is on par
withcommercialantivirussoftware.
Toanswerthethirdquestion,wealsoinvestigatetheeffect
of obfuscation on the same dataset. The experimental results
indicate that MOJI is far more robust to obfuscation than the
existingmethodsandcommercialantivirussoftware.
Tosummarize,thecontributionsofthispaperarethree-fold:
1. WeproposeMOJI,acharacter-levelconvolutionalneural
networkformaliciousJavaScriptdetection.
2. The proposed method achieves 7%-13% better F1 score
(reaching99.35%)thantheexistingstaticdetectors,while
running97-147timesfaster.
3. Wealsoinvestigatetheeffectofobfuscationonmalware
detection. An experiment on an additionally-obfuscated
datasetshowsthatourmethodmaintainsdetectionperformance,whereastheexistingdetectorsandcommercial
antivirus software drastically reduce their performance,
rangingfrom −9.95to −95.62%inF1score.
Therestofthispaperisorganizedasfollows.Section2providesareviewofrelatedliterature.Section3describestheproposedmethod.Section4discussestheexperimentstoevaluate
theproposeddetector.Lastly,Section5drawstheconclusions.

## 2. Related Work

2.1. Obfuscation
Obfuscation is the process of transforming a code into a
harder-to-understandrepresentationforhumanswhilepreservingtheoriginalprogram'sfunctionality[2,3].Attackersmayemployobfuscationto hidethemaliciousnessof acodetoevade
detection. Note that obfuscation itself is not always a sign of
maliciousness. Benign JavaScript codes may also use obfuscation to reduce data size or hide sensitive content from users.
Fig.1showsanobfuscatedJavaScriptcodeof alert(''Hello
world!!'').Theobfuscatedcodecontainsvariableswithmeaningless names, hexadecimal notation such as0xf2, and symbols used in regular expressions. The original string''Hello
world!!''issplitandencoded,sothatitturnsintothedifferent
appearance.Variousobfuscationmethodsarecombinedtomake
thecodemoredifficulttounderstand.Obfuscationmethodscan
bebroadlycategorizedintofourtypes[3].
• Randomization obfuscation.Randomlyinsertwhite-space/
comments,changevariable/functionnames.e.g., inputData
→ a516ek
• Data obfuscation. Use string splitting/substitution or numericalexpressionstochangethephysicalappearanceof
variables/constants.e.g., i = 10→ i = 5 * 2
• Encoding obfuscation. ConvertacodeintoASCII,Unicode,
hexadecimal, or encrypted representations. e.g.,''str''
→ unescape(''%73%74%72'')
• Logic structure obfuscation. Changethelogicstructureof
acodetomanipulateitsexecutionpath.e.g., if ... else
→ switch ... case
2.2. Machine learning models for text classification
TraditionalmodelsincludenaiveBayesianclassifiers,Support
Vector Machines (SVMs) [18], and random forests [19,20]. Recently,withthesuccessofdeepneuralnetworks,Convolutional
Neural Networks (CNNs), Recurrent Neural Networks (RNNs),
GatedRecurrentUnit(GRU)[21],andLongShort-TermMemory
(LSTM)[22]havebeenpopularchoicesfortextclassification[23].
In most methods utilizing these models, feature extraction is
done by word level. Common examples of word-level feature
extractiontechniquesareBag-of-Words(BoW),TermFrequencyInverse Document Frequency (TF-IDF), n-gram, and word embeddingssuchasWord2Vec[24,25],GlobalVectors(GloVe)[26],
andfastText[27,28].However,thesetechniquesareinherently
vulnerable to obfuscation since they are designed for natural
languagetexts.Unlikenaturaltexts,obfuscatedcodescontaina
lotofrandom,encoded,andsymbolicnotations,whichcannotbe
splitintowords.
Character-LevelConvolutionalNeuralNetworks(CLCNNs)[29,
30]arevariantsofCNNs,designedfortextclassification.They
consist of 1D convolutional layers for feature extraction followed by fully connected layers for classification. They accept
a sequence of encoded characters as an input. Thanks to the
character-levelnature,CLCNNsrequirenowordsplittingorprior
knowledge about a language. Other than text classification,
CLCNNs have been used to detect malicious URLs, file paths,
or registry keys [31,32]. Our present work tackles a different
aspectofcybersecurity,namelydetectingpotentiallyobfuscated
JavaScript malware. JavaScript codes are much more complex
than URLs, file paths, and registry keys, because of the wider
varietyofcharacters(JavaScriptsupportsUnicode),muchlarger
filesizes,andpossibleobfuscation.
2.3. Malicious JavaScript detection
Detecting malicious JavaScript codes is a fundamental and
activeresearchareaincybersecurity.Byobfuscationtechniques,
traditionalapproachessuchassignature-orpatternmatchingbased methods [4] are hindered from detecting maliciousness.
Whilerule-basedmethodscandetectobfuscatedcodes[5],they
sufferfromfalsepositivesbecauseobfuscationisnotalwaysa
sign of maliciousness. Using machine learning is a promising
researchdirectiontoovercometheseshortcomingsoftraditional
methods.IthasbeenthemainstreamofmaliciousJavaScriptdetection nowadays. Machine learning-based approaches are
broadlycategorizedintodynamicandstaticanalysesdepending
onthewayoffeatureextraction.Wefirstbrieflyreviewdynamic
analysisandthenpaymoreattentiontostaticanalysis,sinceour
proposedmethodbelongstothelattercategory.
3

---


<!-- PAGE 4 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
2.3.1. Dynamic analysis
DynamicanalysismethodsemployvirtualmachinesorsandboxenvironmentstoexecuteJavaScriptcodesandanalyzetheir
dynamic behavior. Gorji and Abadi [6] used internal function
debugging to capture sequences of internal function calls, and
detectedmaliciouscodesbyclusteringthesequencesbasedon
normalized Levenshtein distance. Hu et al. [33] constructed a
forced execution engine for JavaScript, which can drive arbitrary JavaScript codes for dynamic analysis. Ndichu et al. [7]
proposedanelaboratedsetofpreprocessingsteps,namelydeobfuscation,unpacking,anddecoding,todynamicallyanalyzeobfuscatedJavaScriptcodes.TheauthorsusedafastTextmodel[27,
28]forfeaturelearningandpassedtheextractedfeaturestoan
SVMclassifier.Rozietal.[34]generatedbytecodesequencesby
executingJavaScript codeon anopen-source JavaScriptengine
and detected malicious codes using a deep pyramid convolutionalneuralnetwork.Dynamicanalysismethodsarerobustto
obfuscationandreliablydetectmaliciousJavaScriptcodesbyexecutingthem.Ontheotherhand,theyrequireseparatedexecution
environmentsandarelessefficientthanstaticanalysismethods.
2.3.2. Static analysis
In contrast with dynamic analysis, static analysis methods
requirenospecialenginesorexecutionenvironmentstodetect
maliciousJavaScriptcodes.Researchersoftenconvertacodeinto
a new representation to uncover its functionality. A common
choiceistouseASTsforcodestructurerepresentation[8-16].
Curtsingeretal.[8]trainedasimpleBayesianclassifierwith
features extracted from ASTs for obfuscation-aware malicious
JavaScript detection. Fass et al. [10] generated an AST using a
JavaScriptparserEsprima[17],andemployedann-grammodel
for feature extraction from the syntactic units of AST. A random forest classifier was trained with the n-gram features to
discriminatebetweenbenignandmalicioussamples.Theauthors
laterextendedtheworkbyincorporatingcontrolanddataflow
information to improve the overall detection rate [9]. Ndichu
et al. [11] leveraged paragraph vectors (Doc2Vec) [35] to embedanASTintoafixed-lengthfeaturevectorandusedanSVM
modelforclassification.Songetal.[12]usedacombinationof
severaldeobfuscationtoolsandgeneratedaprogramdependency
graphbasedonanASTandacontrolflowgraph.Theauthors
selectedseveralAPIfunctionsaskeyfunctions,suchas eval(),
escape(), anddocument.URL(), to generate program slices.
ThegeneratedslicesarepassedtoaWord2Vecmodel[24,25],
followedbyaBidirectionalLSTM(BiLSTM)networkforclassification.Fangetal.[13]alsousedaBiLSTMnetworkasaclassifier.
They utilized a fastText model for feature extraction from an
ASTandincorporatedanattentionmechanisminthenetworkto
weightheimportanceofthefeatures.Rozietal.[14]builtaGraph
ConvolutionalNetwork(GCN)withaself-attentionlayertoanalyzeanASTasagraphstructure.Theattentionscorecanhighlight
thesuspiciouspartsofmalicioussamples.Huangetal.[15]used
aTextCNN[29]asaclassifier.Theyadopteddynamicwordembeddings[36]toconsidercontextualinformationofsyntaxunits
ofAST.Fangetal.[16]constructedaprogramdependencygraph
from an AST and applied graph pruning to remove redundant
information.Then,thegraphwaspassedthroughaGCNtopredict
itsmaliciousness.Whiletheliteraturementionedaboveisbased
onpurestaticanalysis,severalstudiescombinestatic(e.g.,AST)
anddynamic(e.g.,functioncalls)analyses[37].
AllofthesestudiesuseASTs,withtheintenttocaptureabstracted code structure to cope with obfuscation and relevant
evasiontechniques.Therefore,theyrequirededicatedpreprocessing steps and external tools (such as JavaScript parsers [17]),
significantlyreducingtheirefficiencyinpracticalsituations.
Surprisingly,muchfewerstudiespredictmaliciousnessfrom
plainJavaScriptcodes[38,39].PhungandMimura[38]focused
onthedataimbalanceproblemandproposedanoversampling
methodbasedonrandomperturbation.Theauthorstrainedan
SVMclassifierwithparagraphvectorsextractedfromplaincodes
using a Doc2Vec model [35] and reported an improved recall
score.However,theylimitedthemselvestonon-obfuscatedsamples. The Doc2Vec model required separate training from the
classifier,andembeddingawholecodeinaparagraphvectormay
loseword-orcharacter-levelgranularity.
The work of Stokes et al. [39] is of great relevance to our
work,inregardstousingcharacter-levelinputsandemploying
adeepneuralnetworkasaclassifier.Theyinterpretedcharacters
inaJavaScriptfileasasequenceofbytecodesandfedthemto
aproposedConvolutedPartitioningofLongSequences(CPoLS)
model.TheCPoLSmodeliscomposedofrecurrentconvolutions,
stackedLSTMs(orBiLSTMs),andfullyconnectedlayers.Theauthorsdidnotperformaruntimeevaluation;thus,itisunclear
howefficientthemodelwas.However,generallyspeaking,RNNs
areslowerthanfeedforwardneuralnetworks.Ourmethodisbuilt
asaCLCNN,amuchefficientarchitectureconsistingofseveral1D
convolutionsandfullyconnectedlayers.

## 3. Methodology

3.1. Problem formulation
WeformulatemaliciousJavaScriptdetectionasabinaryclassification problem (benign or malicious). Given a sequence of
encoded characters C = {cn}n=1:N in a JavaScript code, the
taskistopredicttheprobabilityofitsmaliciousness ˆp,where
N denotesthenumberofinputcharacters. 2 Thegroundtruths
arerepresentedasbinarylabels p ∈ {0,1},where1indicates
malicioussamples.Weperformthemappingfrom Ctoˆpusinga
deepneuralnetworktrainedtominimizethedifferencesbetween
thegroundtruthlabels pandthepredictedprobabilities ˆp.The
parametersofthenetwork G : RN → R1 areoptimizedbya
gradientmethod.
3.2. Character encoding
Before feeding characters into the network, they should be
transformedintoanumericalrepresentationfromastringrepresentation. We use a vocabulary of charactersV to convert
eachstringcharacter snintoanintegerrepresentinganencoded
character,i.e., cn = V(sn).WechoosetheUnicodecodepoint
tableas V,sincethestandardcharacterencodingofJavaScript
is UTF-16.3 Table 1 shows part of the mapping table (0x200x7f)betweencharactersandtheircorrespondingintegersofthe
Unicodecodepoints.Forexample,characters Aand zaremapped
to 0x41(65)and 0x7a(122),respectively.Wedonotconsider4bytecharacters(surrogatepairs)sincewefoundthatover99.99%
ofcharactersthatappearedinourexperimentalJavaScriptfiles
are2-bytecharacters.Ifwefindthe4-bytecharacters,wesimply
skipthem.Therefore,theencodedcharactersareintherangeof
cn∈{0,1, . . . ,65535}.WeusePython's ord()functionforthe
conversion.
3.3. Malicious JavaScript detection model
OurmaliciousJavaScriptdetectionmodel,MOJI,isacharacterlevelconvolutionalneuralnetwork,asshowninFig.3.Wedesign the network architecture based on eXpose network [31]
withmodificationstobebettersuitedforthetaskofmalicious
JavaScriptdetection.
2 Weset N=20,000.SeeSection4.2.1fortheimplementationdetails.
3 https://262.ecma-international.org/12.0/
4

---


<!-- PAGE 5 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Table 1
PartoftheUnicodecodepointmappingtable(0x20-0x7f).Forexample,acharacter Aismappedto 0x41(65).
0 1 2 3 4 5 6 7 8 9 a b c d e f
0x20 ! '' # $ % & '' ( ) * + , - . /
0x30 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
0x40 @ A B C D E F G H I J K L M N O
0x50 P Q R S T U V W X Y Z [ \ ] ^ _
0x60 ' a b c d e f g h i j k l m n o
0x70 p q r s t u v w x y z { | } ∼ DEL
Fig. 3. NetworkstructureofMOJI.MOJItakesasequenceofencodedcharacters C andestimatesthemaliciousnessscore ˆp.Thenumbersinparenthesesindicate
thelayers'outputsizes,where N representsthenumberofinputcharactersand Distheembeddingdimensionality.DR:Dropout,Conv:Convolution,GSP:Global
SumPooling,LN:LayerNormalization,Concat:Concatenation,andFC:FullyConnected.
First,MOJItakesasequenceofencodedcharacters C ∈ RN
and processes it through an embedding layer to obtain a 64dimensionalembeddingvectorforeachcharacter,resultinginan
embeddingmatrixof64 ×N.Thisembeddinglayerhasthelargest
numberoflearnableparametersinournetwork[40],thatisa
learnableweightmatrix W ∈ RV×D,where V = 65536isthe
vocabularysizeand D= 64istheembeddingdimensionality.
Topreventtheoverfittingofthislayer,weproposeapplyinga
variantofdropout,namelycharacterdropouttotheembedding
matrix. The standard dropout [41] randomly deactivates neuronsinanetworkwithindependentprobabilityduringtraining.
However,neuronsintheembeddingmatrixarenotindependent
sinceitisasetofembeddingvectorsofcharacters.Ourcharacter dropout randomly deactivates the embedding vectors in
theembeddingmatrixtopreservetheconsistencyincharacter
embeddings.Inotherwords,foragivenembeddingmatrixofsize
D× N (where D = 64inournetwork),thestandarddropout
considers D× N neuronsforrandomdeactivation.Incontrast,
characterdropoutconsiders Nembeddingvectors.Fromanother
pointofview,characterdropoutcanbeviewedasakindofdata
augmentation that applies random masks for input characters.
Itisbeneficialtolearningdiscriminativefeaturesfromcomplex,
potentiallyobfuscatedJavaScriptcodes.
Then, the embedding matrix is fed to a group of 1D convolutional layers with varying kernel sizesk ∈ {2,4,6,8} to
extractmulti-scalefeatures.ThisoperationisfollowedbyRectifiedLinearUnit(ReLU)activation[42],globalsumpooling[31],
dropout [41] with a probability of 0.5, and layer normalization[43].Theoutcomesarefour128-dimensionalfeaturevectors,
whicharethenconcatenatedintoasinglefeaturevectorofsize
512.Next,thefeaturevectorpassesthroughafullyconnected
layerwith512units,followedbyReLUactivation,layernormalization,anddropoutwithaprobabilityof0.5.Finally,thelastfully
connectedlayerwithsigmoidactivationoutputsascalarvalue
representingthemaliciousnessscore ˆp∈[0,1].
Comparedtothebaselinenetwork[31],weimprovethefollowing aspects of network architecture. First, we increase the
dimensionality of embedding vectors from 32 to 64 since the
variationofinputcharactersinJavaScriptcodesismuchbroader
thanthetaskthebaselinetackled(detectingmaliciousURLs,file
paths,andregistrykeys).Second,weintroducecharacterdropout
to avoid the overfitting in the embedding layer. Third, in the
convolutionallayers,weuselargerkernelsizes,specifically k∈
{2,4,6,8}insteadof k∈{2,3,4,5}.Weintendtoimprovethe
receptivefieldofthenetworktoseeabroaderareaoftheinput
sequence,becausethenumberofcharactersinJavaScriptcodesis
large,especiallyinobfuscatedcodes.Fourth,wehalvethefeature
dimensionalityoftheintermediatelayerstopreventthenetwork
fromoverfittingthetrainingdata.Finally,wecutthenumberof
fullyconnectedlayersfromfourtotwotoreducethenumber
of parameters in the network. The experimental comparisons
betweenMOJIandthebaseline[31]aregiveninSections4.3-4.5.
3.4. Loss function and optimizer
WeusetheBinaryCrossEntropy(BCE)lossbetweenthemodel
outputsandgroundtruthlabels.TheBCElossisgivenby
Lbce=− 1
m
m∑
i=1
pilog(ˆpi)+(1− pi)log(1−ˆpi), (1)
where misthemini-batchsize, iistheindexofeachsamplein
themini-batch, p∈{0,1}isthegroundtruthbinarylabel,and
ˆp∈[0,1]isthemodeloutputaftersigmoidactivation.Wetrain
themodelbyAdamoptimizer[44]withalearningrateof0.001,
andamini-batchsizeof32.Werunthemodeltrainingfor10
epochs.

## 4. Experiments and Results

In this section, we evaluate the detection performance and
efficiencyofMOJIthroughexperiments.MOJIiscomparedagainst
priorstudiesofmaliciousJavaScriptdetection[9,11],thebaseline
network[31],aswellascommercialantivirussoftware.
WefirstdescribeadatasetusedintheexperimentsinSection4.1,thenexplainourevaluationprotocol,includingimplementationdetailsandperformancemetricsinSection4.2.Next,
wediscusstheresultsfromthreeaspects:detectionperformance,
robustnesstoobfuscation,andrunningtimeinSection4.3,Section 4.4, and Section 4.5, respectively. Finally, we provide an
ablation study in Section 4.6 and feature visualization in Section4.7.
5

---


<!-- PAGE 6 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Table 2
DatasourcesforourmaliciousJavaScriptdetectiondataset.
Name Source #Samples
Benign Alexatop1000websites 15,770
MaliciousA GitHub[45] 30,237
MaliciousB GitHub[46] 1341
4.1. Dataset
Fortheexperiments,wecreatedadatasetof24,000JavaScript
codes,consistingof12,000benignand12,000malicioussamples.
Wedescribethedetailsofourdatasetinthefollowingsections.
4.1.1. Data collection
Usingawebscraper,wecollectedbenignsamplesfromthe
home pages of Alexa top 1000 websites. The scraper obtained
<script>tagsfromthescrapedpagesandgatheredtheirembeddedandlink-referencedJavaScriptcodes.Malicioussamples
wereobtainedfromtwopubliclyavailabledatasetsonGitHub[45,
46]. Most of the samples in the two malicious datasets were
alreadyobfuscated.Tosummarize,weusedthreedatasources
listedinTable2,namely(a)Benign,fromAlexatop1000websites,(b)MaliciousA,fromoneGitHubrepository[45],and(c)
MaliciousB,fromtheotherGitHubrepository[46].Wecompared
samples within and between the data sources and removed
duplicatedsamples.
4.1.2. Data splits
Wesplitthecollectedcodesinto20,000training,2000validation,and2000testsamples.Table3showsthesplitsweusedin
theexperiments.Forthetrainingandvalidationsplits,weused
Benign and Malicious A as data sources. We randomly picked
10,000benignand10,000malicioussamplesforthetrainingsplit
and 1000 benign and 1000 malicious samples for the validationsplit.Thesamplesinthetrainingandvalidationsplitswere
selected without overlap. For the test split, we first randomly
selected1000benignsamplesfromBenign,whichwerenotoverlappedwiththetrainingandvalidationsplits.Wethenrandomly
picked1000malicioussamplesfromMaliciousB.
Here, we used malicious samples from two different data
sources, i.e., Malicious A for the training/validation splits and
MaliciousBforthetestsplit.Thisexperimentalsettingismore
challengingthancross-validationbecausedetectorsshouldgeneralizewellacrossthesamplesfromdifferentdatasources.Since
cross-validationdividesasingledatasetintosplits,thedatadistributionbetweenthesplitstendstobemoresimilarthanour
setting. In real-world situations, however, detectors should be
robusttounseenmalware.Weintendedtoimitatethissituation
inourexperiments.
Toconfirmwhetherthedatadistributionsactuallydifferbetweenourtrainingandtestsplits,wevisualizethedistributions
as bar graphs in Fig. 4. The bar graphs show the number of
malwarefilesthatcontainthreetypesofcharacters(numbers,
alphabets,andsymbols)inspecificproportions.Forexample,a
filecontaining60%numbersand40%alphabetsiscountedinboth
thebluebaratthe60%positiononthehorizontalaxisandthered
baratthe40%position.Thebargraphsshowthatthemalware
samplesinthetestsplithavedifferentcharacteristicsfromthe
trainingsamplesasintended.Specifically,thetestsamplescontainmuchmorealphabetsthanthetrainingsamples.Ontheother
hand,thetrainingsamplescomprisemorenumbersandsymbols
thanthetestsamples.
Table 3
Training,validation,andtestsplitsofourdataset.
Split Datasources #Samples
Training Benign+MaliciousA 20,000
Validation Benign+MaliciousA 2000
Test Benign+MaliciousB 2000
4.1.3. Obfuscation
AsdescribedinSection2.1,maliciouscodesmayemployobfuscationtohidetheirmaliciousness,whilebenignonesmayalso
useobfuscationtoreducedatasizeorhidesensitivecontentfrom
users.Thus,detectionmodelsshouldbeabletoclassifybenign
and malicious samples with or without obfuscation. To do so,
weobfuscatedhalfofthesamplesinthetrainingandvalidation
splitsusinganobfuscationtoolJavaScriptObfuscator. 4Through
thisprocess,10,000samples(5000benign,5000malicious)inthe
trainingsplitand1000samples(500benign,500malicious)in
thevalidationsplitwereobfuscated.Whilemostofthesamples
in Malicious A were already obfuscated, we additionally performedobfuscationonit.Ontheotherhand,wedidnotperform
additionalobfuscationonthetestsplit.
4.2. Evaluation protocol
WecompareMOJIwiththepreviousmachinelearning-based
staticanalysisapproachesformaliciousJavaScriptdetection[9,
11],thebaselinenetwork[31],aswellasseveralcommercialantivirussoftware.Weselecttheabovetwomachinelearning-based
malicious JavaScript detection methods because JStap [9] providespubliclyavailableimplementation,whileforAST-Doc2Vec
[11], all hyperparameters necessary for re-implementation are
availableinthepaper.Forafaircomparison,weusethesame
training,validation,andtestsplitsforallthemachinelearningbasedapproaches(includingMOJIandthebaseline).Wedonot
usethetraining/validationsplitsforantivirusproductssincetheir
detectionalgorithmsareblackboxesandwedonottrainthem.
4.2.1. Implementation details
JStap[9].Weusethepubliclyavailableimplementationprovided
bytheauthors. 5 Thismethodsupportsdifferentlevelsofcode
abstraction,namelytokens,AST,ControlFlowGraph(CFG),ProgramDependencyGraph(PDG),andPDGwithDataFlowGraph
(PDG-DFG). Also, two types of feature extraction, n-gram and
nodevalues,aresupported.WechooseASTforcodeabstraction
andn-gramforfeatureextraction,whichperformsbestinour
experiments.
AST-Doc2Vec[11].ThismethodusesASTsforcodestructurerepresentationandextractstheirparagraphvectorsusingaDoc2Vec
model [35]. We re-implement this method from scratch since
there is no its publicly-available implementation. We use a
JavaScript parser Esprima [17] to obtain ASTs from JavaScript
codes. For the Doc2Vec model, we employ Distributed Bag of
WordsversionofParagraphVector(PV-DBOW)sinceitperforms
betterthanDistributedMemoryversionofParagraphVector(PVDM)inourexperiments.WeuseanSVMclassifierwithalinear
kerneland C=1.0,asdescribedintheoriginalpaper.
Proposed Method. Unlikethepreviousstudies[9,11],MOJIrequiresnocodeabstractionorpriorfeatureextraction.WhileMOJI
canacceptanarbitrarynumberofcharactersasinputs,wefix
thenumberofcharacters N=20,000tomaketrainingtimeand
4 https://github.com/javascript-obfuscator/javascript-obfuscator
5 https://github.com/Aurore54F/JStap
6

---


<!-- PAGE 7 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Fig. 4. Visualizeddatadistributionsofthemalicioussamplesinthetraining(a)andtest(b)splits.Thebargraphsshowthenumberofmalwarefilesthatcontain
three types of characters (numbers, alphabets, and symbols) in specific proportions. The distributions indicate that the training and test samples have different
characteristics.
memoryfootprintreasonable.Weapplyzero-paddingtosamples
shorterthan Ncharacters.Forsampleslongerthan Ncharacters,
weextractthelast Ncharacterstofitthefixedlength. 6
eXpose[31].AsdescribedinSection3.3,weuseeXpose[31]as
thebaselinenetwork.Wefollowtheconfigurationsintheoriginal
paper, i.e., set embedding vectors' dimensionality to 32, apply
nocharacterdropout,usekernelsizesof k∈{ 2,3,4,5}inthe
1Dconvolutionallayers,setthefeaturedimensionalityofthe1D
convolutionallayersandfullyconnectedlayersto256and1024,
respectively,andusefourfullyconnectedlayers.Exceptforthe
networkconfiguration,weusethesamehyperparametersused
forMOJI.
Antivirus Software. Weemployfiveantivirussoftwarethatreceivedthebest''ADVANCED+''awardsintheMalwareProtection
TestbyAV-Comparatives. 7 Inparticular,weuseMicrosoftDefender Antivirus (ver. 1.367.1767.0), Avast Free Antivirus (ver.
22.5.6015),AviraAntivirusPro(ver.15.0.2111.2126),TotalDefense Essential Anti-Virus (ver. 13.0.0.576), and G DATA Total
Security(ver.25.5.12.833).TotalDefenseEssentialAnti-Virusand
G DATA Total Security are trial/free versions of the products
usedintheMalwareProtectionTest,whiletheyhavethesame
functionalitiesasthefullversionsregardingmalwaredetection.
4.2.2. Performance metrics
Forquantitativeevaluation,wereportthefollowingmetrics
commonlyusedinmalwaredetectionstudies[7-16,34,37-39]:
•Accuracy: TP+TN
TP+TN+FP+FN
•Precision: TP
TP+FP
•Recall: TP
TP+FN
•F1score: 2×Precision×Recall
Precision+Recall
TP(TruePositive)isthenumberofmalicioussamplescorrectly
classifiedasmalicious,TN(TrueNegative)isthenumberofbenignsamplescorrectlyclassifiedasbenign,FP(FalsePositive)is
thenumberofbenignsampleswronglyclassifiedasmalicious,
and FN (False Negative) is the number of malicious samples
wronglyclassifiedasbenign.
4.3. Comparison of detection performance
Table 4 shows the quantitative comparison of MOJI against
previousmachinelearning-basedstaticanalysismethods[9,11],
6 Wealsotriedusingthefirst N charactersbutusingthelast N characters
performedbetter.
7 https://www.av-comparatives.org/tests/malware-protection-testseptember-2021/
the baseline network [31], and commercial antivirus software.
Wetrainthemachinelearning-basedmethodsfivetimeseach
withdifferentrandomseedsandshowthemeanandstandard
deviationvaluesinthetable.Regardingaccuracy,recall,andF1
score, MOJI outperforms the previous machine learning-based
methods by a noticeable margin. While JStap [9] achieves the
highestmeanprecision,MOJImarkscomparableperformance.
Amongthefourmetrics,weobservesignificantimprovements
in the recall metric over the previous machine learning-based
methods [9,11,31]. We note that the dataset used in our experimentsischallengingbecauseweusedifferentdatasources
for malicious samples in training/validation (i.e., Malicious A)
and test (i.e., Malicious B) splits (Section 4.1). Therefore, the
samples' characteristics and employed obfuscation techniques
mayvarybetweenthesplits.Thisdifferencerequiresdetection
modelstohavestrongrobustnesstovariouscharacteristicsand
obfuscationtechniques.Thepreviousmethodsfailtohavesuch
robustnessandtendtoclassifyobfuscatedmalicioussamplesas
benignwrongly.Incontrast,MOJIyieldspromisingresultseven
forthechallengingdataset.
ComparedtothebaselineeXposenetwork[31],MOJIachieves
consistentperformanceimprovements.WenotethateXposehas
significantly higher standard deviations than MOJI. The results
indicatethateXposeismoresensitivetotherandomnessofthe
trainingprocessofdeepneuralnetworks(e.g.,weightinitialization).Thus,theproposedarchitecturehasbettercharacteristics
regardingstability.
The lower rows of Table 4 show the performance of the
commercial antivirus software. All the software achieves 100%
precision,i.e.,nofalsepositives.However,theperformanceon
theotherthreemetricsvaries.Whilethedetectionalgorithmsof
commercialantivirussoftwareareblackboxes,theyshouldcombinemultipleapproaches,e.g.,patternmatching,statisticalanalysis,heuristicanalysisinsandboxes,etc.Incontrast,MOJIuses
onlyasingleneuralnetworktoachievecomparableperformance
tothebest-rankedcommercialantivirussoftware.
To evaluate the detection characteristics of the proposed
method further, we plot the Receiver Operating Characteristic
(ROC)curveforeachofthemachinelearning-basedmethods. 8
TheROCcurveillustratesthetrade-offbetweenthetruepositive
rate(recall)andthefalsepositiveratebyvaryingthedetection
threshold, i.e., the closer the curve to the top left corner, the
betterthedetectoris.
TheROCcurvesforthemachinelearning-basedmethodsare
showninFig.5.WealsocalculatethecorrespondingAreaUnder
8 Asexplainedearlier,wetrainedthemachinelearning-basedmethodsfive
timeseach.Foreachmethod,weusethelastmodeltoplottheROCcurve.
7

---


<!-- PAGE 8 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Table 4
Quantitativecomparisonagainstpreviousmethodsandcommercialantivirussoftware.Wetrainthemachinelearning-basedmethods
fivetimeseachwithdifferentrandomseedsandshowthemeanandstandarddeviationvalues.Eachvalueisdisplayedin%.The
symbol*denotesourre-implementation.
Method/Software Accuracy Precision Recall F1Score
JStap 93 .22±0.07 99.88± 0.00 86.54±0.13 92 .73±0.08
AST-Doc2Vec* 89 .00±0.09 99 .62±0.00 78 .30±0.19 87 .68±0.12
eXpose* 93 .07±2.36 99 .36±0.09 86 .70±4.76 92 .54±2.71
MOJI(Ours) 99.35± 0.15 99.64±0.32 99.06± 0.11 99 .35± 0.14
MicrosoftDefender 82.15 100.00 64.30 78.27
Avast 99.50 100.00 99.00 99.50
Avira 98.60 100.00 97.20 98.58
TotalDefense 99.40 100.00 98.80 99.40
GDATA 99.65 100.00 99.30 99.65
Table 5
Comparison on the obfuscated test split. MOJI achieves superior performance on all the metrics. The AST-based methods are
significantlyaffectedbytheadditionalobfuscation.Surprisingly,thecommercialantivirussoftwareisverymuchaffectedandfailsto
findoutmostofthemalicioussamples.Thenumbersafterthearrowsindicatethedifferencesinmeanvaluesbetweentheoriginal
testsplit( ↓:dropped, ↑:improved, ↕:same,comparedtoTable4).
Method/Software Accuracy Precision Recall F1Score
JStap 85 .40±3.77 ↓7.82 99 .58±0.05 ↓0.30 71 .10±7.54 ↓15.44 82 .78±5.22 ↓9.95
AST-Doc2Vec* 77 .30±0.16 ↓11.70 98 .82±0.10 ↓0.80 55 .26±0.32 ↓23.04 70 .88±0.26 ↓16.80
eXpose* 93 .28±2.34 ↑0.21 98 .59±0.55 ↓0.77 87 .84±5.19 ↑1.14 92 .83±2.70 ↑0.29
MOJI(Ours) 99.39± 0.08 ↑0.04 99.82± 0.22 ↑0.18 98.96± 0.24 ↓0.10 99.39± 0.08 ↑0.04
MicrosoftDefender 50.30 ↓31.85 100.00 ↕0.00 0.60 ↓63.70 1.19 ↓77.08
Avast 52.25 ↓47.25 90.91 ↓9.09 5.00 ↓94.00 9.48 ↓90.02
Avira 50.75 ↓47.85 100.00 ↕0.00 1.50 ↓95.70 2.96 ↓95.62
TotalDefense 55.90 ↓43.50 99.17 ↓0.83 11.90 ↓86.90 21.25 ↓78.15
GDATA 55.60 ↓44.05 99.12 ↓0.88 11.30 ↓88.00 20.29 ↓79.36
Fig. 5. ROCcurvesandAUCscoresforthemachinelearning-basedmethods.The
falsepositiverate(horizontalaxis)isdisplayedinthelogscale.MOJIachieves
thehighestAUCscore.
theCurve(AUC)scoresandshowtheminthefigurelegend.MOJI
achievesthebestAUCscoreamongthemachinelearning-based
methods. From the ROC curves, we observe that MOJI shows
exceptionalperformance,whichachieveshightruepositiverates
withextremelylowfalsepositiverates.Incontrast,theprevious
methods,especiallyJStap[9],showcleartrade-offsbetweenthe
truepositiverateandthefalsepositiverate.Theseresultsindicate
thatMOJIhasbetterbalancebetweenthetwometricsthanthe
previousmethods.
4.4. Experiment with additional obfuscation
As described in Section 4.1, most of the malicious samples
inthedatasetareobfuscated.However,attackersmayperform
additionalobfuscationtopreviously-obfuscatedJavaScriptcodes
tocomplicatethemfurther.Totesttherobustnesstosuchadditionalobfuscation,weconductanotherexperimentbyreplacing
thesamplesinthetestsplit.Specifically,weperformadditional
obfuscation on the 1000 benign and 1000 malicious samples
in the test split using JavaScript Obfuscator. We use the same
trainedmodelsusedinSection4.3forthisexperiment,i.e.,we
onlyreplacethetestsamplesanddonotre-trainthemodels.
Table5showstheresultsoftheexperimentwithadditional
obfuscation.Thescoredifferencesbetweentheoriginaltestsplit
aredisplayedafterthearrows( ↓:dropped,↑:improved,↕:same,
comparedtoTable4).Here,therecallscoreshavegreatimportance since they indicate how well the detectors find out the
complicatedmalicioussamples.Theresultsindicatethatwhile
JStap[9]andAST-Doc2Vec[11]significantlysufferfromtheadditionalobfuscation,theperformancesofeXpose[31]andMOJI
arewell-preserved.
Thepreviousmethods[9,11]requirecodeabstraction(i.e.,AST)
andpriorfeatureextraction(i.e.,n-gramorparagraphvectors).
Incontrast,MOJItakesencodedcharactersdirectlywithoutsuch
complexpreprocessingsteps.Althoughtheresearchersperform
codeabstractionintendingtomakedetectionmodelsrobustto
obfuscation, the experimental results indicate that it is rather
morefragiletoadditionalobfuscationthanMOJI.Apossiblereasonforthisfragilityisthattheobfuscatedmalicioussamplesmay
becomestructurallysimilartotheobfuscatedbenignsamplesin
training/validationsplitssinceweusethesameobfuscationtool
JavaScript Obfuscator for both the training/validation and test
splits.Suchstructuralsimilaritiesmayleadtosimilarcodeabstractionresultsanddeterioratetheperformanceoftheprevious
methods.
Surprisingly,weobservecatastrophicdropsintherecallscores
of the commercial antivirus software. In other words, the antivirusproductswronglyclassifymostofthemalicioussamples
asbenign.Ontheotherhand,theimpactontheprecisionscores
isrelativelysmall.Onepossiblereasonisthatthetypesofobfuscationtoolsmightbiasthedecisionoftheantivirusproducts.
8

---


<!-- PAGE 9 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Table 6
Running time (milliseconds) per single JavaScript file. We report the average time of processing 4000 files. The
symbol*denotesourre-implementation.
Method Preprocessing Classification Totaltime
Algorithm Time Algorithm Time
JStap AST,n-gram 771.62 Randomforest 0.37 771.99
AST-Doc2Vec* AST,Tokenization,Doc2Vec 508.90 SVM 0.05 508.95
eXpose* Characterencoding 3.59 CNN 4.10 7.68
MOJI(Ours) Characterencoding 3.56 CNN 1.68 5.24
SinceJavaScriptObfuscatorisapublic,populartoolontheweb,
benignwebsitesmayalsoemployit.Thesimilarityofobfuscation
might mislead the antivirus software to overlook the signs of
maliciousness.
4.5. Running time
EfficiencyisacrucialaspectofpracticalmaliciousJavaScript
detectiontoprovidecomfortablewebbrowsingexperiencesfor
users.WecomparetherunningtimeofMOJIwithJStap[9],ASTDoc2Vec[11],andeXpose[31].Forafaircomparison,wetestall
themethodsonacomputerrunningUbuntu20.04withanIntel
Corei9-10900(2.8GHz),128GBofRAM,andanNVIDIAGeforce
RTX3090(24GB).
AsshowninTable6,MOJIismuchmoreefficientandtakes
only5.24mstoscanasingleJavaScriptcode.Therunningspeed
isabout ×147fasterthanJStap[9]andabout ×97fasterthan
AST-Doc2Vec[11].Also,MOJIisslightlyfasterthanthebaseline
network eXpose [31] because of the improvement in network
architecture.
MOJIhasasignificantlyshorterpreprocessingtimethanJStap
andAST-Doc2Vecsinceitrequiresnocodeabstractionorprior
feature extraction. In particular, the preprocessing for MOJI is
characterencodingdescribedinSection3.2,namelyconversion
toUnicodecodepoint.Thisprocessisasimpletablelookupand
takesonly3.56ms. 9Ontheotherhand,JStap[9]constructAST
andextractn-gramfeaturesduringitspreprocessing.Similarly,
AST-Doc2Vec [11] performs AST construction and tokenization
followedbyparagraphvectorembeddingusingaDoc2Vecmodel.
Although researchers tend to report the classification time of
theirmethodastherunningtime,thepreprocessingtimeisalso
essentialfromapracticalpointofview.
Regardingclassificationtime,theproposedmethodtakesthird
place. JStap [9] and AST-Doc2Vec [11] are faster because they
employ traditional machine learning methods (JStap: random
forest,AST-Doc2Vec:SVM),whileMOJIisbuiltupondeepneural
networks.MOJIisslightlyfasterthaneXpose[31]sinceournetworkhasfewerparametersthaneXpose.Specifically,wehalve
thefeaturedimensionalityoftheintermediatelayersandreduce
thenumberoffullyconnectedlayers(seeSection3.3fordetails).
4.6. Ablation study
Toinvestigatetheeffectivenessoftheproposednetworkarchitecture,weconductanablationexperimentbyalteringtwo
componentsofthenetwork:thekernelsizesofthe1Dconvolutionallayersandtheon-offofthecharacterdropout.Table7
displaystheresultsofthisexperiment,comparingF1scores.As
inthepreviousexperiments,eachsettingistrainedfivetimes
withdifferentrandomseeds.Thebestkernelsizesare(2,4,6,
8), with the highest mean F1 score. The results indicate that
thecharacterdropoutimprovesthemeanscorewhilereducing
thestandarddeviation.Theseobservationsvalidatethatourarchitecturedesigncontributestoperformanceimprovementand
trainingstability.
9 WeusethesamepreprocessingstepforeXpose[31]andMOJI.
4.7. Visualization of hidden feature vectors
To further analyze the proposed method, we visualize the
hiddenfeaturevectorsofthenetwork.Fig.6showst-SNE[47]
visualizationsofthefeaturevectors h∈ R512takenfromtheconcatenationlayerofMOJI.Thegreenishdotsshowbenignsamples,
whereasthereddishdotsrepresentmalicioussamples.Wevisualizethefeaturevectorsfromfourtypesofsamples;greendots:
benignsamplesfromtheoriginaltestsplit,yellow-greendots:
benignsamplesfromtheobfuscatedtestsplit,reddots:malicious
samplesfromtheoriginaltestsplit,anddarkreddots:malicious
samplesfromtheobfuscatedtestsplit.Thedistributionsofthe
dotsindicatethatMOJIlearnsdiscriminativefeaturesbetween
benignandmalicioussamplesrobusttoadditionalobfuscation.
Interestingly,wefindthatthedistributionsoftheoriginalbenign
(greendots)andobfuscatedbenignsamples(yellow-greendots)
arepartiallyoverlapped.Thedistributionssuggestthatsomeof
theoriginalbenignsamplesareobfuscatedbyatoolsimilarto
theoneweused(i.e.,JavaScriptObfuscator).Ontheotherhand,
the distributions of the original malicious (red dots) and the
obfuscatedmalicious(darkreddots)arerelativelymoredistant.
Thisdifferenceimpliesattackersmayuselesser-knowntoolsto
obfuscatetheirmaliciousprograms.

## 5. Discussion & Conclusion

Inthispaper,wehaveproposedMOJI,amaliciousJavaScript
detectorbasedondeepneuralnetworks.Theproposedmodelis
acharacter-levelconvolutionalneuralnetwork,mainlyconsisting
of1Dconvolutionallayersandfullyconnectedlayers.Unlikeexistingstaticanalysismethods,whichrequirecodeabstractionand
priorfeatureextraction,ourapproachsimplifiestheprocessing
flowbydirectlytakingasequenceofcharactersinJavaScriptcode
andestimatingitsmaliciousnessscore.Theexperimentalresults
onadatasetof24,000JavaScriptcodesshowthatMOJIoutperformspreviousstaticanalysismethodsandisonparwiththe
best-rankedantivirussoftware.Specifically,MOJIachieves99.35%
inF1score,whichis7%-13%betterthanthepreviousmethods.
Moreover,itrequiresonly5.24mstoscanafile,whichis97147timesfaster.Also,theexperimentwithadditionalobfuscation
indicatesthatMOJIisfarmorerobusttoobfuscationthanthe
previousmethodsandcommercialantivirussoftware.Webelieve
thatMOJIbalancessimplicity,accuracy,andefficiencywell.
5.1. Limitations
WhileMOJIcanacceptanarbitrarynumberofcharactersas
inputs, its memory footprint increases linearly with the number of characters. Although our experiments show that using
N = 20,000charactersachievespromisingresults,thislimitationmightbecomeanissueifMOJIisdeployedinedgedevices
with low computational resources. A possible way to mitigate
this issue is splitting a long source code into shorter chunks
andmergingthechunk-wisescores,asLiuetal.didforimage
segmentation[48].
Inaddition,asagenerallimitationofanymalwaredetectors,
iftheproposeddetectorfallsintothehandsofcyberattackers,
theymightdevelopnewevasiontechniquesfortheirmalwareto
slipthroughourdetector.
9

---


<!-- PAGE 10 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Table 7
EffectofthekernelsizesandcharacterdropoutinMOJI.Wereportthemeanandstandarddeviation
values over five training. The kernel sizes (2, 4, 6, 8) achieve the best mean score. Furthermore,
thecharacterdropoutimprovesthemeanscorewhilereducingthestandarddeviation.
Model Kernelsize Characterdropout F1Score
MOJI
(2,3,4,5) ✓ 98.66±0.72
(4,5,6,7) ✓ 99.29±0.12
(6,7,8,9) ✓ 99.25±0.10
(8,9,10,11) ✓ 97.32±2.23
(4,6,8,10) ✓ 98.84±0.64
(6,8,10,12) ✓ 98.92±0.30
(8,10,12,14) ✓ 98.30±1.35
(2,4,6,8) 99 .07±0.38
(2,4,6,8) ✓ 99.35± 0.14
Fig. 6. t-SNE visualization of the hidden feature vectors of MOJI. The feature vectorsh∈ R512 are taken from the concatenation layer after the group of 1D
convolutionallayers.
5.2. Future work
Weseeseveralpossibledirectionsforfutureresearch.
First,sinceMOJIisastaticanalysisapproach,itcanbecombinedwithdynamicanalysismethodstoimprovethedetection
performancefurther.
Second, with the rising popularity of explainable AI, it is
worthwhiletoimprovetheexplainabilityofMOJI.Forexample,
MOJIcouldbecombinedwithanattentionmechanismtoweigh
the importance of characters and highlight suspicious parts of
JavaScriptfiles,similartotheworkofRozietal.[14].
Finally,itwouldbeexcitingtodeployantivirusapplications
using MOJI. As the current study is limited to JavaScript malware, adopting MOJI to other programming languages (e.g., C,
C#,Python,andPerl)tobuildmoregeneralmalwaredetectors
isanotherpromisingdirection.
CRediT authorship contribution statement
Minato Ishida: Conceptualization, Methodology, Software,
Validation, Investigation, Writing - review & editing.Naoshi
Kaneko: Writing - original draft, Writing - review & editing,
Supervision. Kazuhiko Sumi: Supervision.
10

---


<!-- PAGE 11 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
Declaration of competing interest
Theauthorsdeclarethattheyhavenoknowncompetingfinancialinterestsorpersonalrelationshipsthatcouldhaveappeared
toinfluencetheworkreportedinthispaper.
Data availability
Datawillbemadeavailableonrequest.
Acknowledgments
Part of this research was operated as a project of Center
forAdvancedInformationtechnologyResearch(CAIR),Aoyama
GakuinUniversity.

## References

[1] ESET,ESETthreatreportT32021,2021,https://www.welivesecurity.com/
wp-content/uploads/2022/02/eset_threat_report_t32021.pdf. (Accessed 13
April2022).
[2] B.Feinstein,D.Peck,Caffeinemonkey:Automatedcollection,detectionand
analysisofmaliciousJavaScript,in:BlackHatUSA,2007.
[3] W.Xu,F.Zhang,S.Zhu,Thepowerofobfuscationtechniquesinmalicious
JavaScript code: A measurement study, in: International Conference on
MaliciousandUnwantedSoftware,MALWARE,2012,pp.9-16,http://dx.
doi.org/10.1109/MALWARE.2012.6461002.
[4] A.Ikinci,T.Holz,F.Freiling,Monkey-Spider:Detectingmaliciouswebsites
with low-interaction honeyclients, Sicherheit, Schutz Und Zuverlässigkei
(2008).
[5] Y.Choi,T.Kim,S.Choi,C.Lee,AutomaticdetectionforJavaScriptobfuscationattacksinwebpagesthroughstringpatternanalysis,in:International
ConferenceonFutureGenerationInformationTechnology,FGIT,2009,pp.
160-172,http://dx.doi.org/10.1007/978-3-642-10509-8_19.
[6] A. Gorji, M. Abadi, Detecting obfuscated JavaScript malware using sequencesofinternalfunctioncalls,in:ACMSoutheastRegionalConference,
ACMSE,2014,pp.1-6,http://dx.doi.org/10.1145/2638404.2737181.
[7] S. Ndichu, S. Kim, S. Ozawa, Deobfuscation, unpacking, and decoding of
obfuscatedmaliciousJavaScriptformachinelearningmodelsdetectionperformanceimprovement,CAAITrans.Intell.Technol.5(3)(2020)184-192,
http://dx.doi.org/10.1049/trit.2020.0026.
[8] C.Curtsinger,B.Livshits,B.Zorn,C.Seifert,ZOZZLE:Fastandpreciseinbrowser JavaScript malware detection, in: USENIX Security Symposium,
2011.
[9] A.Fass,M.Backes,B.Stock,JStap:Astaticpre-filterformaliciousJavaScript
detection,in:AnnualComputerSecurityApplicationsConference,ACSAC,
2019,pp.257-269,http://dx.doi.org/10.1145/3359789.3359813.
[10] A.Fass,R.P.Krawczyk,M.Backes,B.Stock,JaSt:Fullysyntacticdetection
of malicious (obfuscated) JavaScript, in: International Conference on DetectionofIntrusionsandMalware,andVulnerabilityAssessment,DIMVA,
2018,pp.303-325,http://dx.doi.org/10.1007/978-3-319-93411-2_14.
[11] S. Ndichu, S. Kim, S. Ozawa, T. Misu, K. Makishima, A machine learning
approachtodetectionofJavaScript-basedattacksusingASTfeaturesand
paragraphvectors,Appl.SoftComput.84(2019)105721,http://dx.doi.org/
10.1016/j.asoc.2019.105721.
[12] X. Song, C. Chen, B. Cui, J. Fu, Malicious JavaScript detection based on
bidirectional LSTM model, Appl. Sci. 10 (10) (2020) 3440, http://dx.doi.
org/10.3390/app10103440.
[13] Y.Fang,C.Huang,Y.Su,Y.Qiu,DetectingmaliciousJavaScriptcodebased
onsemanticanalysis,Comput.Secur.93(2020)101764,http://dx.doi.org/
10.1016/j.cose.2020.101764.
[14] M.F.Rozi,T.Ban,S.Ozawa,S.Kim,T.Takahashi,D.Inoue,JStrack:Enriching
maliciousJavaScriptdetectionbasedonASTgraphanalysisandattention
mechanism,in:InternationalConferenceonNeuralInformationProcessing,
ICONIP, 2021, pp. 669-680, http://dx.doi.org/10.1007/978-3-030-922702_57.
[15] Y. Huang, T. Li, L. Zhang, B. Li, X. Liu, JSContana: Malicious JavaScript
detection using adaptable context analysis and key feature extraction,
Comput. Secur. 104 (2021) 102218, http://dx.doi.org/10.1016/j.cose.2021.
102218.
[16] Y.Fang,C.Huang,M.Zeng,Z.Zhao,C.Huang,JStrong:MaliciousJavaScript
detection based on code semantic representation and graph neural network,Comput.Secur.118(2022)102715,http://dx.doi.org/10.1016/j.cose.
2022.102715.
[17] A. Hidayat, ECMAScript parsing infrastructure for multipurpose analysis,
2022,https://esprima.org/.(Accessed19March2022).
[18] C.Cortes,V.Vapnik,Support-vectornetworks,Mach.Learn.20(3)(1995)
273-297,http://dx.doi.org/10.1007/BF00994018.
[19] T.K. Ho, Random decision forests, in: International Conference on Document Analysis and Recognition, ICDAR, 1995, pp. 278-282, http://dx.doi.
org/10.1109/ICDAR.1995.598994.
[20] L. Breiman, Random forests, Mach. Learn. 45 (1) (2001) 5-32, http://dx.
doi.org/10.1023/A:1010933404324.
[21] K. Cho, B. Van Merriënboer, C. Gulcehre, D. Bahdanau, F. Bougares, H.
Schwenk,Y.Bengio,LearningphraserepresentationsusingRNNencoderdecoder for statistical machine translation, in: Conference on Empirical
MethodsinNaturalLanguageProcessing,EMNLP,2014,http://dx.doi.org/
10.3115/v1/d14-1179.
[22] S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural Comput.
9(8)(1997)1735-1780,http://dx.doi.org/10.1162/neco.1997.9.8.1735.
[23] K. Kowsari, K. Jafari Meimandi, M. Heidarysafa, S. Mendu, L. Barnes, D.
Brown,Textclassificationalgorithms:Asurvey,Information10(4)(2019)
150,http://dx.doi.org/10.3390/info10040150.
[24] T. Mikolov, K. Chen, G. Corrado, J. Dean, Efficient estimation of word
representationsinvectorspace,in:WorkshopAtInternationalConference
onLearningRepresentations,2013.
[25] T.Mikolov,I.Sutskever,K.Chen,G.S.Corrado,J.Dean,Distributedrepresentationsofwordsandphrasesandtheircompositionality,in:Advances
inNeuralInformationProcessingSystems,NIPS,2013.
[26] J. Pennington, R. Socher, C.D. Manning, GloVe: Global vectors for word
representation,in:ConferenceonEmpiricalMethodsinNaturalLanguage
Processing, EMNLP, 2014, pp. 1532-1543, http://dx.doi.org/10.3115/v1/
D14-1162.
[27] P.Bojanowski,E.Grave,A.Joulin,T.Mikolov,Enrichingwordvectorswith
subword information, Trans. Assoc. Comput. Linguist. 5 (2017) 135-146,
http://dx.doi.org/10.1162/tacl_a_00051.
[28] A.Joulin,E.Grave,P.Bojanowski,T.Mikolov,Bagoftricksforefficienttext
classification,in:ConferenceoftheEuropeanChapteroftheAssociationfor
ComputationalLinguistics,EACL,AssociationforComputationalLinguistics,
2017,pp.427-431,http://dx.doi.org/10.18653/v1/e17-2068.
[29] Y. Kim, Convolutional neural networks for sentence classification, in:
ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,EMNLP,
2014,http://dx.doi.org/10.3115/v1/D14-1181.
[30] X.Zhang,J.Zhao,Y.LeCun,Character-levelconvolutionalnetworksfortext
classification,in:AdvancesinNeuralInformationProcessingSystems,NIPS,
2015.
[31] J.Saxe,K.Berlin,eXpose:Acharacter-levelconvolutionalneuralnetwork
withembeddingsfordetectingmaliciousURLs,filepathsandregistrykeys,
2017,arXivpreprintarXiv:1702.08568.
[32] H.Le,Q.Pham,D.Sahoo,S.C.Hoi,URLNet:LearningaURLrepresentation
with deep learning for malicious URL detection, 2018, arXiv preprint
arXiv:1802.03162.
[33] X.Hu,Y.Cheng,Y.Duan,A.Henderson,H.Yin,JSForce:Aforcedexecution
engineformaliciousJavaScriptdetection,in:InternationalConferenceon
SecurityandPrivacyinCommunicationSystems,SecureComm,2017,pp.
704-720,http://dx.doi.org/10.1007/978-3-319-78813-5_37.
[34] M.F.Rozi,S.Kim,S.Ozawa,DeepneuralnetworksformaliciousJavaScript
detection using bytecode sequences, in: International Joint Conference
on Neural Networks, IJCNN, 2020, pp. 1-8, http://dx.doi.org/10.1109/
IJCNN48605.2020.9207134.
[35] Q. Le, T. Mikolov, Distributed representations of sentences and documents,in:InternationalConferenceonMachineLearning,ICML,2014,pp.
1188-1196.
[36] M.E.Peters,M.Neumann,M.Iyyer,M.Gardner,C.Clark,K.Lee,L.Zettlemoyer, Deep contextualized word representations, in: Conference of the
NorthAmericanChapteroftheAssociationforComputationalLinguistics:
Human Language Technologies, NAACL HLT, 2018, pp. 2227-2237, http:
//dx.doi.org/10.18653/v1/N18-1202.
[37] J. Wang, Y. Xue, Y. Liu,T.H. Tan, JSDC: A hybrid approach forJavaScript
malwaredetectionandclassification,in:ACMSymposiumonInformation,
Computer and Communications Security, ASIA CCS, 2015, pp. 109-120,
http://dx.doi.org/10.1145/2714576.2714620.
[38] N.M. Phung, M. Mimura, Detection of malicious JavaScript on an imbalanceddataset,InternetThings13(2021)100357,http://dx.doi.org/10.1016/
j.iot.2021.100357.
[39] J.W. Stokes, R. Agrawal, G. McDonald, M. Hausknecht, ScriptNet: Neural
staticanalysisformaliciousJavaScriptdetection,in:IEEE/AFCEAMilitary
Communications Conference, MILCOM, 2019, http://dx.doi.org/10.1109/
MILCOM47813.2019.9020870.
[40] Y.Gal,Z.Ghahramani,Atheoreticallygroundedapplicationofdropoutin
recurrentneuralnetworks,in:AdvancesinNeuralInformationProcessing
Systems,NIPS,2016.
11

---


<!-- PAGE 12 -->

M. Ishida, N. Kaneko and K. Sumi Applied Soft Computing 137 (2023) 110138
[41] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, R. Salakhutdinov,
Dropout: A simple way to prevent neural networks from overfitting, J.
Mach.Learn.Res.15(56)(2014)1929-1958.
[42] V. Nair, G. Hinton, Rectified linear units improve restricted Boltzmann
machines,in:InternationalConferenceonMachineLearning,ICML,2010.
[43] J.L. Ba, J.R. Kiros, G. Hinton, Layer normalization, 2016, arXiv preprint
arXiv:1607.06450.
[44] D.P. Kingma, J.L. Ba, Adam: A method for stochastic optimization, in:
InternationalConferenceonLearningRepresentations,ICLR,2015.
[45] H. Petrak, JavaScript malware collection, 2021, https://github.com/
HynekPetrak/javascript-malware-collection.(Accessed17December2021).
[46] S. Paganoni, Malicious JavaScript dataset, 2021, https://github.com/
geeksonsecurity/js-malicious-dataset.(Accessed17December2021).
[47] L.VanderMaaten,G.Hinton,Visualizingdatausingt-SNE,J.Mach.Learn.
Res.9(11)(2008)2579-2605.
[48] Y. Liu, Q. Ren, J. Geng, M. Ding, J. Li, Efficient patch-wise semantic
segmentation for large-scale remote sensing images, Sensors 18 (10)
(2018)3232.
12
