---
title: "Textual Variations in Social Media Text Processing Applications: Challenges, Solutions, and Trends"
slug: "01_textual_variations_social_media"
authors: "Jebran Khan, Kashif Ahmad, Senthil Kumar Jagatheesaperumal, Kyung-Ah Sohn"
year: 2025
venue: "Artificial Intelligence Review (Springer), Vol. 58, Issue 1"
doi: "10.1007/s10462-024-11048-2"
category: "Obfuscation & Text Variations"
tags: ["social-media-text", "textual-variations", "obfuscation", "slang", "leetspeak", "nlp-noise"]
total_pages: 48
character_count: 157838
word_count: 23399
source_file: "Textual variations in social media text processing applications challenges, solutions, and trends.pdf"
extraction_date: "2026-10-20 15:09:51"
---

# Textual Variations in Social Media Text Processing Applications: Challenges, Solutions, and Trends

## Metadata & Bibliographic Overview
- **Authors:** Jebran Khan, Kashif Ahmad, Senthil Kumar Jagatheesaperumal, Kyung-Ah Sohn
- **Publication Year:** 2025
- **Venue / Journal:** Artificial Intelligence Review (Springer), Vol. 58, Issue 1
- **DOI / Link:** 10.1007/s10462-024-11048-2
- **Category:** Obfuscation & Text Variations
- **Original Source File:** `Textual variations in social media text processing applications challenges, solutions, and trends.pdf` (48 pages, ~23,399 words)

## Agent Quick-Scan / Executive Takeaways
> [!NOTE]
> **Relevance to Tugas Akhir / Research Context:**
> Provides a comprehensive survey on informal text variations in social media (substitutions, phonetic spelling, character repetitions, word splitting). Serves as theoretical grounding for the four obfuscation families (O1 Character Substitution, O2 Insertion/Deletion, O3 Whitespace, O4 Unicode Homoglyphs).

### Key Thematic Dimensions
- **Domain:** Obfuscation & Text Variations
- **Methodology Focus:** social-media-text, textual-variations, obfuscation, slang, leetspeak, nlp-noise
- **Relevance Anchors in Repo:** Connects to Stage 8 (Data Leakage & Pairing), Stage 9 (Baseline Models), Stage 10 (Adversarial Robustness O1-O4), and Stage 11 (Domain Shift OOD).

---

# Full Extracted Document Text



<!-- PAGE 1 -->

Accepted: 12 December 2024 / Published online: 13 January 2025
© The Author(s) 2024
 
 Kyung-Ah Sohn
kasohn@ajou.ac.kr
Jebran Khan
jebran@ajou.ac.kr
Kashif Ahmad
kashif.ahmad@mtu.ie
Senthil Kumar Jagatheesaperumal
senthilkumarj@mepcoeng.ac.in
1	 Department	of	 Artificial	Intelligence,	Ajou	University,	Suwon,	South	Korea
2	 Department	of	Computer	Science,	Munster	 Technological	University,	Cork,	Ireland
3	 Department	of	Electronics	&	Communication	Engineering,	Mepco	Schlenk	 Engineering	
College,	Sivakasi,	Tamil	Nadu,	India
4	 Department	of	Software	and	Computer	Engineering,	 Ajou	University,	Suwon,	South	Korea
Textual variations in social media text processing 
applications: challenges, solutions, and trends
Jebran Khan1 · Kashif Ahmad2 · Senthil Kumar Jagatheesaperumal3 ·  
Kyung-Ah Sohn1,4
Artificial Intelligence Review (2025) 58:89
https://doi.org/10.1007/s10462-024-11071-z

## Abstract

Being	an	informal	communication	source,	social	media	text	is	susceptible	to	several	
intentional	and	unintentional	textual	variations.	These	variations	lead	to	various	out-ofvocabulary	(OOV)	words,	making	social	media	text	processing	more	challenging.	This	
work	analyses	and	discusses	such	challenges	by	providing	a	detailed	overview	of	different	
sources	of	intentional	and	unintentional	OOV	words	and	associated	challenges.	We	provide	a	detailed	survey	of	pre-processing	techniques,	including	traditional	and	applicationspecific	methods	proposed	in	the	literature	to	handle	intentional	and	unintentional	textual	
variations,	while	highlighting	their	pros	and	cons.	The	paper	analyses	the	implications	of	
text	normalization	(standardization)	in	different	social	media	text-processing	applications.	
Moreover,	the	paper	provides	an	overview	of	the	recent	challenges	and	trends	in	handling	
social	media	textual	variations,	and	it	is	expected	to	provide	a	baseline	for	future	research.
Keywords Social	media	·	Text	variations	·	Text	normalization	·	OOV	words	·	Text	
processing applications
1 3

---


<!-- PAGE 2 -->

J. Khan et al.
1 Introduction
The	recent	development	in	web	and	information	&	communication	technologies	(ICT)	has	
turned	our	society	into	an	online	social	society	by	changing	how	people	communicate	and	
share	information.	As	a	result,	several	social	media	outlets,	allowing	users	to	communicate	
and	share	their	photos,	music	choices,	news,	and	other	material	of	mutual	interests,	have	
been	introduced	Khan	and	Lee	(2019);	Ahmad	et	al.	(2019).	More	recently,	with	the	growing	interest	and	an	enormous	increase	in	the	number	of	users,	the	impact	of	social	media	
outlets on our society has gone beyond entertaining usage to an integrated part of our daily 
life.1	Being	able	to	attract	and	engage	billions	of	users	and	worldwide	accessibility	makes	
them	a	preferred	forum	for	communication	and	discussions	on	different	domestic	and	global	
events	and	issues.	The	literature	already	reports	several	studies	on	the	role	and	effectiveness	of	social	media	in	different	applications,	such	as	healthcare	Moorhead	et	al.	(2013),	
education	Zachos	et	al.	(2018),	e-commerce	Abed	et	al.	(2015),	public	services	Ahmad	et	
al.	(2022),	the	fashion	industry,	disaster	management	Said	et	al.	(2019),	and	entertainment	
Craig	and	Cunningham	(2019).
In	the	modern	world,	where	knowledge,	stats,	and	information	are	considered	valuable	
assets	in	decision-making	for	social,	economic,	political,	and	cultural	development,	the	role	
of	social	media	outlets	is	more	crucial.	Social	media	text	has	already	been	proven	to	be	one	
of	the	primary	sources	of	information,	fulfilling	the	needs	of	a	diversified	set	of	applications.	
However,	social	media	text	also	comes	with	several	challenges,	making	the	extraction	of	
meaningful	insights	more	challenging.	For	instance,	as	an	informal	source	of	communication,	social	media	text	is	generally	inconsistent,	and	it	contains	a	wide	range	of	variations	
that	result	in	out-of-vocabulary	(OOV)	words.	These	variations	are	generally	caused	by	
intended	and	unintended	spells	&	grammar	mistakes,	typographic	&	cognitive/orthographic	
errors,	phonetic	replacements,	as	well	as	word	shortening	and	enlargements	Khan	and	Lee	
(2020).
The	presence	of	OOV	words	in	social	media,	which	are	introduced	due	to	intended	and	
unintended	variations,	may	result	in	inaccurate	text	processing	and	failure	to	extract	meaningful	insights	in	different	applications	Liu	et	al.	(2011).	Social	media	text	is	cleaned	and	
normalized	by	employing	different	techniques	in	the	pre-processing	step,	depending	on	the	
nature	of	the	underlying	applications	that	deal	with	the	OOV	words.	Text	normalization	
performed	during	pre-processing	aims	to	transform	noisy	and	OOV	words	into	corresponding	standard	lexical	representations.	Text	normalization	is	not	limited	to	spelling	correction	
and	substituting	OOV	words	only	Baldwin	and	Li	(2015).	It	involves	identifying	and	handling	a	wide	range	of	OOV	words	and	error	patterns,	such	as	word	enlargement/shortening/
deletion,	dialectal/informal	word	usage,	and	censor	avoidance	Baldwin	et	al.	(2013).	For	
convenience,	all	these	methods	are	termed	pre-processing	methods	throughout	the	paper.
The	exponential	growth	and	potential	of	social	media	informal	text	in	various	applications	have	attracted	the	research	community's	attention.	Consequently,	several	interesting	
normalization	techniques	have	been	proposed	to	clean	and	effectively	utilize	the	text.	In	this	
paper,	we	provide	a	detailed	survey	of	the	types	and	sources	of	text	variations	and	the	corresponding challenges and potential solutions.
1  h	t	t				p	s	:		/	/		t	i	n	y		u	r	l	.	c					o	m	/		b	d		z	j	r		7			5	c  .   
1 3
89 Page 2 of 48

---


<!-- PAGE 3 -->

Textual variations in social media text processing applications:…
1.1 Scope of the survey
This	paper	revolves	around	the	challenges	associated	with	informal	social	media	text	processing.	More	specifically,	it	focuses	on	the	nature	and	sources	of	intentional	and	unintentional	textual	variations	in	social	media	and	the	challenges	associated	with	the	correction	
and	normalization	of	the	OOV	words	caused	by	these	textual	variations.	The	paper	furthermore	focuses	on	the	implications	of	different	pre-processing	techniques	for	dealing	with	
these	textual	variations	in	various	applications.
2 Related surveys
Pre-processing,	which	primarily	aims	at	cleaning	and	normalizing	text,	is	considered	an	
integral	part	of	text	processing	pipelines.	The	literature	reports	several	effective	solutions	
for	cleaning	and	normalization	of	text.	Despite	being	an	integral	part	of	text	processing	
frameworks,	to	the	best	of	our	knowledge,	the	literature	needs	a	detailed	survey	on	dealing	
with	textual	variations	and	associated	challenges	in	general	and	social	media	text	processing	
in	particular.	However,	the	literature	does	report	several	interesting	comparative	analyses	
of	text	pre-processing	techniques	to	deal	with	textual	variations	in	different	applications.	
For	instance,	Naseem	et	al.	(2021)	conducted	a	comparative	analysis	of	twelve	different	
techniques	in	hate	speech.	They	evaluated	these	techniques	for	retaining	key	features	by	
removing	unnecessary	words/features.	Clark	et	al.	(2010)	conducted	a	similar	study	on	
text	normalization	in	social	media,	considering	two	different	spell	correction	methods.	The	
comparative	analysis	of	such	techniques	has	also	been	carried	out	for	other	applications.	
For	instance,	Maslej-Krešňáková	et	al.	(2020)	analyzed	the	impact	of	different	techniques,	
including	tokenization,	lowercasing,	punctuation,	and	stop	word	removal	for	toxic	comments	detection.	Similarly,	Symeonidis	et	al.	(2018)	conducted	a	comparative	analysis	of	
several	such	techniques,	including	lemmatization,	removing	numbers	and	punctuations,	and	
replacing	contractions,	for	sentiment	analysis	in	Twitter.
In	contrast	to	the	existing	comparative	studies,	in	this	paper,	we	provide	a	detailed	survey	of	the	literature	on	handling	intentional	and	unintentional	textual	variations	in	a	social	
media	text.	This	paper	also	provides	a	detailed	taxonomy	of	textual	variations	and	corresponding	solutions.	We	discuss	the	implications	of	such	techniques	(e.g.,	noise	removal,	
text	standardization,	data	augmentation,	text	normalization)	in	different	social	media	textprocessing	applications.	The	paper	also	overviews	limitations	and	open	issues	and	recommends potential solutions.
2.1 Contributions
The	key	contributions	of	the	paper	are	summarized	as	follows.
 ● This	paper	provides	a	detailed	survey	of	the	literature	on	textual	variation,	associated	
challenges,	and	text	normalization	in	social	media	text	processing.
 ● This	work	provides	a	detailed	taxonomy	of	intentional	and	unintentional	sources	of	
textual	variations	in	a	social	media	text.
 ● We	provide	a	detailed	description	and	taxonomy	of	methods,	including	both	traditional	
1 3
Page 3 of 48 89

---


<!-- PAGE 4 -->

J. Khan et al.
and	recent	trends	in	social	media	text	preparation	to	cope	with	the	textual	variation	
and	resulting	OOV	words.	The	paper	particularly	focuses	on	the	pros	and	cons	of	these	
methods.
 ● Furthermore,	this	work	explored	the	implications	of	text	preparation	techniques	(e.g.,	
noise	removal,	text	standardization,	data	augmentation,	text	normalization)	in	different	
social	media	text-processing	applications.
 ● This	work	is	concluded	by	discussing	the	key	challenges	associated	with	social	media	
text	cleaning	and	normalization	and	recommending	potential	solutions.The	remaining	
paper	is	organized	as	follows.	Section	3	provides	a	detailed	overview	of	the	textual	variations	in	a	social	media	text.	Section	4	presents	a	detailed	taxonomy	of	social	media	text	
preparation	techniques.	Section	5	discusses	the	implications	of	text	normalization	in	
different	social	media	text-processing	applications.	Section	6 highlights some key challenges	associated	with	social	media	text	pre-processing	and	makes	recommendations.	
Finally,	Sect.	7 concludes the paper.
3 Sources of textual variations in social media text
Social	media	outlets	are	informal	sources	of	communication	and	generally	contain	various	variations	and	inconsistencies	in	the	text.	Social	media	platforms	are	widespread	with	
unique	textual	variations	due	to	their	informal	nature	and	diverse	user	base.	This	section	
explores	the	primary	sources	of	these	variations,	highlighting	how	they	arise	and	the	challenges	they	present	for	text-processing	applications.	Table	1	shows	a	few	examples	of	different	text	variations	in	different	languages,	illustrating	common	types	of	textual	deviations	
and	their	occurrences	in	social	media	texts.
Several	sources/causes	of	these	variations	and	inconsistencies	include	the	author's	limited	knowledge	of	the	language	and	vocabulary,	spelling	errors,	limits	on	the	message/post	
length,	and	word	shortening	and	user-defined	abbreviations	Khan	and	Lee	(2020).	These	
variations	result	in	OOV	words	representing	the	terms	and	words	that	are	not	part	of	the	
standard	text.	The	OOV	words	can	be	classified	as	(i)	intentional	OOV	words	and	(ii)	Unintentional	OOV	words.	Figure	1	provides	a	taxonomy	of	sources	of	OOV	words,	which	are	
discussed	in	the	following	subsection	in	more	detail.
3.1 Sources of unintentional OOV words
The	unintentional	OOV	words	could	be	introduced	in	the	text	unintentionally	due	to	several	
reasons,	such	as	the	limited	knowledge	and	vocabulary	of	the	social	media	user,	spelling	and	
typing	mistakes,	or	errors	in	the	keypad	Khan	and	Lee	(2021).	This	section	overviews	the	
common	sources	of	unintentional	OOV	words	in	a	social	media	text.
3.1.1 Typographic errors
Typographic	errors	are	simple	mistakes	that	unintentionally	occur	during	typing	text	Shah	
and	Melo	(2020).	For	instance,	pressing	a	wrong	key	in	two	adjacent	keys	and	missing	
keys	are	among	the	most	common	types	of	unintentional	typographic	errors	(e.g.,	"Hello"	
→	"Helo"	or	"tomorrow"	→	"tommorrow").	These	errors	could	also	occur	due	to	keypad	
1 3
89 Page 4 of 48

---


<!-- PAGE 5 -->

Textual variations in social media text processing applications:…
malfunctioning.	For	instance,	sometimes,	a	key	on	a	keypad	needs	to	be	pressed	harder	than	
others	or	a	key	may	not	work	at	all.	Typographic	errors	can	occur	in	any	language,	regardless	of	its	typological	features.	However,	Languages	with	deep	orthographies,	complex	
orthographic	rules,	extensive	diacritical	marks,	long	words,	logographic	writing	systems,	
and	rich	morphological	systems	are	more	susceptible	to	typographic	errors.	Some	examples	
from	Korean	(사랑해	(I	love	you)	→ 살랑해,	and	안돼	(no)	→ 안되	رٹویپمک
computer)	→German	(Schwimmen	(to	swim)	→ 
Schwimmeb,	and	Deutschland	(Germany)	→	Deutshland)	are	provided,	where	the	difference	between	the	actual	and	the	generated	text	is	due	to	typing	mistake.
3.1.2 Cognitive/orthographic errors
Orthographic/cognitive	errors	are	another	common	source	of	unintentional	OOV	words	
and	generally	occur	by	substituting	an	incorrect	spelling/word	for	the	correct	(intended)	
one	due	to	ignorance	or	unfamiliarity	with	the	underlying	language	Reynolds	et	al.	(2022).	
Generally,	the	resulting	misspelled	word	orthographically	resembles	the	actual	words	(e.g.,	
"Right"	→	"rite").	Cognitive	errors	generally	occur	due	to	phonetic	or	semantic	similarity	
Table 1	Sample	social	media	text	variations	in	different	languages
Language Text	variation	type Original	text Text	variation Example
English Typographic	errors	
Shah	and	Melo	
(2020)
"I	bought	this	for	my	
niece for Christmas."
"I	boght	this	for	my	
niece for Chrestmas."
"boght"	instead	of	
"bought",	"Chrestmas"	instead	of	
"Christmas."
Korean Cognitive	errors	
Berthelier	(2023)
"사랑해요." "사랑해." Formal	"해요"	
replaced	with	informal "해"
Spanish Diacritical	variations	
Bustamante	and	Díaz	
(2006)
"Qué	tal	estás?" "Que	tal	estas?" Omission	of	
diacritics
Urdu Real-word	errors	
Aziz	et	al.	(2023)
"وہر	شوخ	ادس"وہر	شوج	ادس" 	شوخ
happy)	is	replaced	
rash)
French Slang	variations	
Keidar	et	al.	(2022)
"Je suis fatigué." "J'suis	crevé." "Je"	replaced	with	
"J'",	"fatigué"	replaced	with	"crevé"
German Emoji usage Koch et 
al.	(2022)
"Ich	liebe	dich!" "Ich	liebe	dich!;)" Addition of an 
emoji at the end
Arabic Dialectal	variations	
Elnagar	et	al.	(2021)
"ًابحرم"الهأ" Formal greeting 
replaced	with	informal greeting
Italian Word	shortening	
Cognola and Casalicchio	(2023)
"Come	stai?" "Cm	stai?" "Come"	replaced	
with	"Cm"
Portuguese Word	enlargement	
Rodríguez-Rubio	
and	FernándezQuesada	(2020)
"Obrigado!" "Obrigadoooo!" Additional "o" at 
the end
Japanese Kanji	variations	
Mori	(2020)
"お元気ですか？" "お元氣ですか？" Different	kanji	
characters used for 
"genki"
1 3
Page 5 of 48 89

---


<!-- PAGE 6 -->

J. Khan et al.
between	the	misspelled	and	the	actual	word	Bhatti	et	al.	(2012).	Languages	with	opaque	or	
deep	orthographies	are	generally	more	susceptible	to	cognitive/orthographic	errors	due	to	
the	complexity	of	the	mapping	between	sounds	(phonemes)	and	written	symbols	(graphemes)	in	these	languages.	For	example,	in	English,	the	sound	/f/	can	be	represented	by	different	graphemes,	such	as	"f"	(fan),	"ph"	(phone),	or	"gh"	(enough),	which	can	lead	to	errors	
like	writing	"fone"	for	"phone"	or	"enuf"	for	"enough."
Fig. 1	A	taxonomy	of	the	sources	of	textual	variations	in	the	social	media	text
 
1 3
89 Page 6 of 48

---


<!-- PAGE 7 -->

Textual variations in social media text processing applications:…
3.1.3 Diacritical errors
Diacritical	errors	are	caused	by	omitting	or	inserting	special	characters	like	accents,	umlauts,	
cedillas,	tildes,	and	other	diacritical	marks	in	languages.	This	type	of	error	significantly	
impacts	communication	as	it	can	change	the	semantic	and	syntactic	properties	of	words	
and	may	potentially	alter	the	meaning	of	sentences,	leading	to	misunderstandings.	In	many	
languages,	like	Vietnamese,	French,	Spanish,	Urdu,	and	Arabic,	the	diacritics	distinguish	
between	words	with	different	meanings	or	grammatical	functions.	For	instance,	in	Vietnamese,	"ma"	can	mean	ghost(ma),	cheek(má),	mother(má),	but/which/if(mà),	horse(mã),	or	
plating(mạ)	depending	on	the	tone.	Some	other	languages	that	are	susceptible	to	diacritical	
errors	include	French	(école	(school)	→	ecole),	Spanish	(está(is)	→	رزج
slaughter)),	
ag)).	Diacritical	
errors are less common in English as standard English orthography does not rely on diacritical	marks.	However,	diacritics	exist	in	some	loan	words	and	names,	neglecting	which	may	
lead	to	a	change	in	meaning,	e.g.,	Café,	Résumé,	São	Paulo,	Zoë,	Naïve,	and	Nestlé,	etc	are	
some	borrowed	words	from	other	languages.
3.1.4 Real word errors
Real-word	errors	represent	the	cases	when	the	unintended	words	are	valid	dictionary	words	
of	the	underlying	language	but	are	not	valid	from	the	context	or	grammar	point-of-view.	
For	instance,	in	the	sentence	"tree	authors	contributed	to	the	text,"	where	"three"	is	unintentionally	mistyped	as	"tree,"	which	is	a	valid	dictionary	word;	however,	it	is	contextually	
big,	great)	→Egypt)	
→Consciousness)	→Lust)	etc.	Aziz	et	al.	(2023)	can	result	
in	a	lexically	valid	word	with	a	different	meaning.	Real-word	errors	can	be	further	grouped	
into	three	groups.	The	first	one	represents	the	unintended	OVV	words	that	are	semantically	incorrect	(e.g.,	"from"	→	"form").	The	second	category	includes	the	unintended	OOV	
words	that	are	grammatically	incorrect	(e.g.,	"yesterday	I	went	to	a	shop"	→	"yesterday	I	
go	to	a	shop").	The	final	category	represents	the	word	division/boundary	errors	(e.g.,	"a	lot"	
→	"a	lot").	Real	word	errors	are	common	in	Arabic,	Urdu,	and	Vietnamese,	where	many	
words	 are	 very	 close	 in	 their	 spelling	 and	 phonetic	 representation.	 For	 instance,	 in	 Urdu	
a	guide	
valley),	etc.	are	at	a	distance	of	
one	character	substitution	Aziz	et	al.	(2023	مْلِع
pen)	are	at	one	character/diacritic	distance	with	a	completely	different	
meaning	Azmi	et	al.	(2019).
3.1.5 Word boundary errors
The	unintended	OOV	words	could	also	be	introduced	in	a	text	due	to	incorrect	spacing.	
Such	unintentional	errors	are	called	word	boundary	errors.	These	errors	can	be	further	categorized	as	incorrect	splits	(e.g.,	"together"	→	"to	gether")	and	run-ons	(e.g.,	"a	lot"	→ 
"alot").	In	English,	these	errors	are	generally	caused	by	unintentionally	pressing/missing	
the	"space"	key	of	the	keypad,	lack	of	knowledge	of	the	language/vocabulary	(i.e.,	spell1 3
Page 7 of 48 89

---


<!-- PAGE 8 -->

J. Khan et al.
ing),	and	an	error	in	the	keypad.	The	word	boundary	errors	in	Agglutinative	languages	like	
Korean,	where	words	contain	different	morphemes	to	determine	their	meaning,	e.g.,	the	
sentence 아버지가방에들어가신다	with	no	spacing	has	no	meaning,	a	space	between	아
버지가 and 방에	(아버지가 방에 들어가신다)	means	"Father	enters	the	room"	and	space	
between	아버지 and 가방에	(아버지 가방에 들어가신다)	means	"Father	enters	the	bag"	
Lee	et	al.	(2023).	In	morphologically	rich	languages	like	Urdu	and	Arabic,	the	insertion/
deletion	of	word	boundaries	mostly	does	not	change	the	meaning	of	the	words,	e.g.,	in	
which	means	"old	
road",	wherein	there	is	no	space,	zero-width	non-joiner	(ZWNJ),	and	a	space	between	the	
of	the	phrase,	respectively.	This	makes	word	tokenization/
segmentation	challenging	due	to	the	inconsistent	use	of	spaces	Rehman	et	al.	(2011);	Daud	
et	al.	(2017).
3.1.6 Phonological errors
Phonological	errors	occur	when	the	author/transcriptor	does	not	correctly	identify	all	the	
sounds	of	the	words	intended	to	be	written/spelled.	These	errors	can	occur	for	many	reasons,	including	the	speaker's	demography,	speech	disorder,	limited	exposure	to	the	target	
language,	or	mispronunciation	of	the	words.	For	instance,	in	some	regions	where	English	
is	not	their	native	language,	confusing	"f"	and	"p"	is	common.	Each	language	has	some	
phonological	restrictions/limitations	that	speakers	subconsciously	adhere	to.	For	instance,	
in	Arabic,	there	is	no	sound	for	"P,	T";	therefore,	it	is	hard	for	a	native	Arab	to	pronounce	it	
correctly	without	forced	effort.	Similarly,	some	languages	like	Korean	have	a	limited	set	of	
vowels	and	consonants	that	can	be	combined	into	syllabic	blocks,	which	leads	to	producing	many	phonetically	similar	words	even	though	they	may	be	written	differently	and	have	
distinct	meanings,	e.g.,	 대학교	(university)	typed	as	 대학꾜	(due	to	mishearing	of	final	
sounds),	confusing	"ㅂ	(b/p)	and	ㅍ	(p')",	"	ㄱ	(g/k)	and	ㅋ	(k')",	ㄷ	(d/t)	and	ㅌ	(t'),	and	
ㅅ	(s)	and	ㅆ	(ss).	Phonological	errors	can	occur	in	Arabic	due	to	confusion	of	phonetically	
proximal	alphabets,	e.g.,	confusing	"(/s/)	with	(/s/)",	"(/h/)	with		(/h/)",	"	(/a/)	with	(/a/)",	
"(/z/)	with		(/z/)",	"(/k/)	with	(/q/)",	(/t̪ 	/)	with			(/t̪ /)	and	vice	versa	are	frequently	observed	
Brosh	(2015).	Similarly,	these	alphabets	are	also	present	in	Urdu.
Phonological	errors	adversely	impact	the	speaker's	communication	and	the	automatic	
transcription	of	online	social	media	content.	Transcription	is	widely	utilized	on	social	media	
and	content	platforms	like	YouTube	to	generate	automatic	subtitles	from	the	commentary	on	
videos.	Mitigating	phonological	errors	is	also	vital	to	perfecting	online	content's	automatic	
transcription and translation.
3.1.7 Morphological errors
Morphological	errors	occur	in	the	structure	of	the	words	when	the	authors	make	mistakes	
in	the	words'	forms,	language	patterns,	morphological	structures,	and	context.	The	morphological	errors	are	divided	into	inflectional,	derivational,	and	compounding	errors.	Inflection	
is	changing	the	form	of	words	(typically	the	words'	ending)	to	express	their	grammatical	
purpose/attribute,	such	as	tense,	emotions,	gender,	number	or	person,	etc.	For	example,	
writing	"deers,	scissor,	and	costed"	instead	of	"deer,	scissors,	and	cost,"	respectively.	The	
inflectional	errors	are	more	common	in	languages	with	intensive	inflectional	morphology,	
1 3
89 Page 8 of 48

---


<!-- PAGE 9 -->

Textual variations in social media text processing applications:…
such	as	fusional	languages	(e.g.,	Russian,	Greek,	Urdu,	etc.)	and	agglutinative	languages	
(Korean,	Turkish,	Finnish,	etc.).	The	derivational	errors	are	generated	when	incorrect	prefixes	or	suffixes	are	added	to	derive	new	words,	e.g.,	writing	"discomplete,	and	teachless"	
instead	of	"incomplete	and	unreachable,"	respectively.	Languages	with	productive	derivational	morphology,	such	as	English	and	German,	are	more	susceptible	to	derivational	errors.	
Compound	errors	occur	when	the	words	are	incorrectly	combined.	These	errors	may	be	
due	to	the	union	of	the	incorrect	forms	of	words,	or	incorrect	compounding	patterns,	e.g.,	
writing	"word	based"	instead	of	"word-based."	These	errors	occur	due	to	the	authors'	short	
vocabulary	or	overgeneralization/unawareness	of	the	grammatical	rules.	These	errors	may	
affect	the	clarity,	fluency,	and	accuracy	of	communication.	These	errors	are	more	common	
in	languages	that	allow	productive	compounding	as	a	major	word-formation	process	e.g.,	
English,	German,	Finnish,	and	Hungarian.
3.1.8 Language dialect errors
The	difference	between	different	language	dialects	may	lead	to	spelling	mistakes.	For	
instance,	English	language	dialects,	i.e.,	British	English	(BrE)	and	American	English	(AmE),	
contain	many	valid	words	in	one	dialect	but	are	invalid	in	another.	AmE	spellings	are	primarily	based	on	the	sounds	of	the	words	in	spoken	language,	whereas	BrE	keeps	the	spelling	of	the	words	absorbed	from	other	languages,	such	as	French	and	German.	Some	of	the	
most	common	differences	between	the	spelling	of	both	dialects	are	as	follows:	Some	words	
in	BrE	ending	in	"our,	ise,	yse,	ence"	usually	end	in	"or,	ize,	yze,	ense",	respectively	in	AmE.	
For	example	"behaviour,	apologise,	analyse,	and	defence"	in	BrE	are	spelled	as	"behavior,	
apologize,	analyze,	and	defense,	respectively	in	AmE.	Similarly,	in	some	words,	the	British	doubles	the	consonants	while	the	Americans	do	not,	e.g.,	"travelling,	and	cancelled"	in	
British	are	spelled	as	"traveling,	and	canceled"	in	AmE.	Some	words	differ	by	vowel	usage	
in	both	dialects	such	as	the	words	"jewellery,	centre,	leukaemia,	and	manoeure"	in	BrE	are	
spelled	as	"jewelry,	center,	leukemia,	and	maneuver"	in	AmE.
In	communication,	the	spell	variants	from	both	of	these	dialects	are	widely	accepted	and	
interchangeably	used;	however,	when	it	comes	to	machine	processing,	they	may	be	treated	
differently.	For	instance,	when	a	specific	dialect	is	selected	while	working	with	text	editors	like	MS	Word	and	Grammarly,	the	spell	checker	considers	words	from	other	dialects	
invalid.
In	the	Arabic	language,	dialects	can	differ	from	each	other	in	vocabulary,	pronunciation,	
morphology,	orthography,	and	even	grammatical	structures,	as	detailed	in	Habash	et	al.	
(2012);	Zaidan	and	Callison-Burch	(2014);	Alnajjar	and	Hämäläinen	(2024).	In	German,	
different	regional	dialects,	such	as	northern,	southern,	and	central	German,	differ	from	each	
other	in	the	pronunciation	of	different	sounds,	resulting	in	different	variants	of	words.	For	
instance,	in	north	and	central	German,	<g>	becomes	<ch>,	as	in	"Betrug	→	Betruch,"	and	in	
southern	German	<s>	becomes	<sch>,	as	in	"kostet	→	koschtet"	Androutsopoulos	(2000).
3.2 Sources of intentional OOV words
Being	an	informal	source	of	communication,	social	media	text	is	also	subject	to	several	
intentional	variations	that	result	in	the	generation	of	different	types	of	OOV	words.	These	
intentional	variations	in	social	media	texts	could	be	motivated	by	several	factors.	For	
1 3
Page 9 of 48 89

---


<!-- PAGE 10 -->

J. Khan et al.
instance,	social	media	users	generally	use	shorthand	words	to	avoid	space	limitations	as	
most	social	media	platforms	provide	a	limited	space	(in	terms	of	maximum	allowed	characters/words)	for	posts/messages	Khan	and	Lee	(2021).	Similarly,	modified	(i.e.,	OOV)	
words	are	also	used	to	emphasize	particular	objects	and	emotions.	The	literature	also	reports	
textual	variations	for	avoiding	automatic	filters,	such	as	hate	speech	and	slang	detectors,	and	
adversarial	attacks	on	NLP	models	in	different	applications	Alsmadi	et	al.	(2022).
These	intentional	variations	in	social	media	text	extend	far	beyond	mere	spelling	errors	
and	include	OOV	slang,	short	forms,	acronyms,	omissions,	phonetic	and	semantic	spelling,	
and	other	intentional	variations	and	misspellings	Clark	et	al.	(2010).	Some	familiar	sources	
of	intentional	OOV	words	in	a	social	media	text	are	discussed	in	this	section.
3.2.1 Word shortening
Word	 shortening	 is	 very	 common	 in	 social	 media	 communication.	 Generally,	 two	
approaches,	namely	(i)	vowel	removal	(having	→	hvng,	good	→	gd	)	and	(ii)	half-words/
clipping	(doing	→	doin),	are	used	for	this	purpose.	The	literature	reports	the	social	media	
users'	 tendency	 towards	 using	 consonants	 and	 excluding	 vowels	 from	 words	 to	 keep	 the	
post/message	length	short	Khan	and	Lee	(2020).	Inspired	by	the	Arabic	and	Hebrew's	Abjad	
writing	system,	where	only	consonants	are	considered	as	characters	and	vowels	can	be	
inferred	by	readers	Daniels	(2013),	Shaibani	and	Ahmad	Al-Shaibani	and	Ahmad	(2023)	
proposed	a	novel	text	representation	for	the	English	language	where	they	removed/masked	
vowels	from	English	text	before	text	analysis.	Such	textual	variations	are	very	frequent	in	
English	informal	social	media	communication.	The	vowel	removal	is	also	used	in	Roman	
texts,	such	as	Roman	Urdu,	Hindi,	and	Pashto	textual	communication.	In	German	language,	
clipping	is	commonly	used	for	word	shortening,	e.g.,	"eine	→	ne	by	clipping	the	first	portion	
of	the	word,	and	ich	habe	→	ich	hab	by	clipping	the	final	e	from	the	verb"	Androutsopoulos	(2000).	In	the	Korean	language,	clipping	is	used	to	change	formal	words	into	informal	
words	e.g.,	왜 이렇게	(why	so)	→ 왜케,	어떻게	(how)	→ 어케 and 재미있게	(having	fun)	
→ 잼게 etc.
3.2.2 Word enlargement
Word	enlargement	is	another	common	source	of	OOV	words	in	a	social	media	text.	In	social	
media	posts/messages,	word	enlargement	is	generally	used	for	the	expression	of	emotions	
(i.e.,	emotional	intensity)	(e.g.,	"Goooood	Morningggggggg")	or	to	highlight	an	entity/
words	or	for	instruction	instructions	in	a	piece	of	text	(i.e.,	emotional	intensity)	(e.g.,"	You	
'musttttt'	check	that")	Khan	and	Lee	(2020).	The	word	enlargement	text	variation	is	also	
frequently	observed	in	other	languages,	including	German	(e.g.,	"gut!	(good!)	→	guuuut!),	
genau!	(Exactly!)	→	Genaaauuuu!"	Androutsopoulos	(2000ok)	→ 
sarcastic	agreement)").
3.2.3 Alphabetism
Alphabetism,	which	refers	to	the	abbreviations	read	letter	by	letter,	is	another	common	
source	of	intentional	OOV	words.	In	this	context,	we	refer	to	user-generated	abbreviations,	
which	are	very	common	in	social	media.	Generally,	every	language	has	a	list	of	standard	
1 3
89 Page 10 of 48

---


<!-- PAGE 11 -->

Textual variations in social media text processing applications:…
abbreviations;	however,	in	social	media,	users	tend	to	generate	abbreviations	of	commonly	
occurring	phrases/sentences	to	reduce	the	message/post	length.	For	example,	in	English	
"Good	Morning	→	GM,	Oh	my	God	→	omg,	talk	to	you	later	→	ttyl,	etc.",	in	German	"zum	
Beispiel	(for	example)	→	zB,	Ich	liebe	dich	(I	love	you)	→	ILD,	Bis	dann	(see	you)	→	BD,	
keine	Ahnung	(no	idea)	→	ka,	and	kein	Bock	(no	desire)	→	kb"	Bick	(2020),	and	in	Korean	
어디?	(where	are	you?)	→ ㅇㄷ?,	오키	(ok)	→ ㅇㅋ,	감사	(shortened	"thank	you")	→ ㄱ
ㅅ and 죄송/죄송합니다	(sorry)	→ ㅈㅅ.
3.2.4 Dialectal usage and contractions
The	use	of	contractions	in	the	text	is	also	one	of	the	common	sources	of	intentional	OOV	
words	in	social	media.	Generally,	contractions	are	used	to	replace	multiple	standard	words	
in	a	language,	for	example,	using	"aint"	instead	of	"are	not",	and	"dunno"	instead	of	"do	not	
know".	Most	languages	have	a	set	of	contractions,	which	are	used	frequently	with	disregard	
for	the	medium	of	communication.	However,	the	usage	of	such	terms	is	more	frequent	in	
informal	sources	of	text,	such	as	social	media	posts	and	messages.	In	German,	contractions	
are	usually	made	up	of	prepositions	and	definite	articles	e.g.,	an	das	(on/at	the)	→	an,	hinter	
dem	(behind	the)	→	hinterm,	and	bei	dem	(with/in	the)	→ beim.
3.2.5 Phonetic substitution
In	social	media	outlets,	the	use	of	phonetic	words	is	also	common.	In	order	to	keep	the	
length	of	text	short,	social	media	users	generally	tend	to	replace	standard	words	with	their	
phonetically	similar	characters.	For	instance,	the	OOV	words/characters,	such	as	"fone",	
"dis/diz",	"d8",	"ur"	and	"2",	are	commonly	used	to	replace	the	corresponding	standard	
words,	such	as	"phone",	"this",	"that/date",	"your"	and	"two/to/too".	Phonetic	substitution	
is	also	frequent	in	Korean	text	messaging,	e.g.,	replacing	some	characters	at	the	end	of	a	
word	with	similar	sounding	characters	i.e.,	싫다,	좋다,	공부,	아니잖아,	진짜로,	뭐하고 
있어,	and	보고싶어 are spelled as 싫타,	싫타,	공뷰,	아니자나,	진짜루,	뭐하구잇어,	and	
보고시포,	respectively.	Phonetic	substitution-based	text	variations	are	not	common	in	Urdu	
and	Arabic	scripts;	however,	in	digital	communication,	the	romanized	text	is	frequently	
used,	and	phonetic	substitution	becomes	frequent.
3.2.6 Visual substitution
Visual	modifications	to	text	are	frequently	used	on	social	media	platforms	to	avoid	censorship	of	certain	words	that	may	be	hateful,	offensive,	or	against	the	platform's	guidelines,	
e.g.,	"!d10t"	Eger	et	al.	(2019).	In	this	type	of	text	variation,	certain	characters	and	words	
are	substituted	by	other	visually	similar	non-alphabet	characters/symbols	(homoglyphs)	and	
words.	Visual	substitution	is	based	on	the	assumption	that	humans	can	easily	recognize	
similar-looking	symbols	Eger	et	al.	(2019).	For	instance,	social	media	or	online	gaming	
users	frequently	use	LeetSpeak	(1337)	in	their	communication.	LeetSpeak	is	another	set	of	
alphabets,	where	each	valid	English	alphabet	has	a	visually	similar	replacement.2	Álvaro	
et	al.	(Huertas-García	et	al.	2023)	applied	LeetSpeak	to	generate	OOV	words	in	multiple	
languages,	including	English,	French,	German,	Italian,	and	Spanish,	to	simulate	the	robust2    h				t	t		p		s	:		/	/		s	i		m	p	l		e	.					w	i	k	i	p	e	d	i		a	.	o	r	g	/	w		i	k		i	/	L	e	e	t .  
1 3
Page 11 of 48 89

---


<!-- PAGE 12 -->

J. Khan et al.
ness	of	text	classification	models	against	such	textual	variations.	Similarly,	in	some	cases,	
the	users	may	also	replace	the	actual	characters	in	a	language	with	their	similar-looking	
accented	characters	Eger	et	al.	(2020).
3.2.7 Words deletion
Word	deletion/omission	or	skipping	in	a	sentence	is	also	very	common	in	social	media.	
Generally,	social	media	users	tend	to	skip	some	words	without	which	the	message	can	still	
be	conveyed.	For	example,	in	informal	communication,	the	three	words	"Where	are	you?"	
can	be	replaced	by	"Where?".	Humans	can	understand	such	posts/messages;	however,	
machines	can't	understand	such	messages,	thus	making	automatic	text	analysis	more	chalwhere	
are	you?)	→where	
are	you	coming	from?)	→from	where?),	etc.).	In	such	textual	variations,	only	
a	portion	of	the	actual	sentence	is	communicated	to	the	receiver,	who	infers	the	rest	of	the	
words	according	to	the	context.
3.2.8 Code-mixed usage
Code-mixing	is	embedding/using	linguistic	units,	words/phrases/morphemes,	of	one	language	in	the	utterance	of	another	language	Poria	et	al.	(2020).	Code-mixing	is	a	phenomenon	prevalent	in	social	media	communication	that	occurs	in	situations	where	users	speak	
multiple	languages	Wankhade	et	al.	(2022).	Code-mixing	makes	the	syntactic	structure	
analysis	challenging,	as	various	portions	of	text	follow	different	syntactic	rules	depending	
on	the	languages.	For	example,	Uno	no	podia	comer	carne	every	day	(Spanish-English),	He	
is	known	as	shair	ka	bachaa	(Urdu-English),	yeh	ek	code-mixed	sentence	ka	example	hai	
(Hindi-English).
The	frequency	of	these	different	types	of	textual	variations	may	differ	from	the	source	
and	language	of	the	text.	For	instance,	the	text	collected	from	Twitter	may	have	more	intentional	OOV	words	than	the	text	from	LinkedIn	and	online	blogs.	Some	studies	have	provided	statistics	about	how	frequently	a	particular	kind	of	variation	is	observed	in	the	data	to	
decide	the	combination	of	the	normalization	methods	for	enhanced	text	analysis.	Some	of	
the	statistics	are	shown	in	Table	2.
3.3 Types of intentional and unintentional errors
In	this	section,	we	categorize	the	errors	caused	by	textual	variations	in	social	media	text.	
The	unintentional	and	intentional	errors	caused	by	the	above-mentioned	sources	could	be	
divided	into	the	following	categories.
3.3.1 Single and multiple-character errors
The	inclusion	of	OOV	words	in	a	text	could	be	due	to	single	or	multiple-character	errors	in	
the	words.	This	categorization	of	errors	classifies	the	OOV	words	into	single	and	multiplecharacter	errors.	Single-character	errors	represent	the	situations	when	the	OOV	word	is	due	
to	the	insertion/deletion	of	a	single	character/key	(e.g.,	"Right"	→	"right").	In	contrast,	in	
1 3
89 Page 12 of 48

---


<!-- PAGE 13 -->

Textual variations in social media text processing applications:…
Table 2	Statistics	of	Textual	Variations	in	Different	Public	Datasets
Value Fraction	of	textual	variations
Reference 	Naseem	et	
al.	(2021)
	Naseem	et	
al.	(2021)
	Naseem	et	
al.	(2021)
	Glazkova	
(2023)
	Glazkova	
(2023)
	Glazkova	
(2023)
 Contractor and 
Faruquie	
(2010)
 Durrani 
and Hussain 
(2010)
 Brosh 
(2015)
	Rimrott	
and Heift 
(2008)
	Łockiewicz	
and	Barzowska	(2024)
 Lertpiya 
et al. 
(2020)
Dataset 	Davidson et al. 
(2017)
	Waseem	
and	Hovy	
(2016)
	Golbeck	et	
al.	(2017)
	Mandl	et	
al.	(2019)
 Zampieri et al. 
(2019)
 Basile et 
al.	(2019)
 Chen and 
Kan	(2013)
 Durrani 
and Hussain 
(2010)
 Brosh 
(2015)
	Rimrott	
and Heift 
(2008)
	Łockiewicz	
and	Barzowska	(2024)
 Lertpiya 
et al. 
(2020)
Language English English English English English English English Urdu Arabic German Polish Thai
Total	Instances 25,112 15,844 19,968 4522 14,100 13,000 800 5000 457 735 793 247,921
Typographic - - - - - - - - 14 - - 61.38
Cognitive - - - - - - - - 54 27 46.1 -
Word	Boundary - - - - - - - 75.5 - - - -
phonological - - - - - - - - 32 30 43.7 -
Morphological - - - - - - - - - 42 9.2 24
Numbers 45.5 - - 42.44 14.06 48.35 - - - - - -
URLs 15 - - 30.38 17.01 37.83 - - - - - -
Mentions 58.5 - - 72 89.51 41.79 - - - - - -
Emojis 3 0.5 2.94 14.93 10.31 7.12 - - - - - -
Hashtags 11 - - 5.26 15.33 29.08 - - - - - -
Word	Shortening - - - - - - 48 - - - - 0.8
Word	
Enlargement
19.1 11.23 14.4 - - - - - - - - -
Alphabetism 19.9 3.86 6.59 - - - 5 - - - - 15
Dialectal	Usage - - - - - - 4 - - - - -
Phonetic 
Substitution
- - - - - - 33 - - - - -
Words	deletion - - - - - - 1.2 - - - - -
1 3
Page 13 of 48 89

---


<!-- PAGE 14 -->

J. Khan et al.
multiple-character	errors,	the	OOV	words	are	included	due	to	errors	at	multiple	positions/
places	in	a	single	word	(e.g.,	"Right"	→	"rite").	The	literature	has	widely	explored	Single	
and	multiple-character	errors,	especially	in	adversarial	NLP	Kukich	(1992);	Alsmadi	et	al.	
(2022).	Resolving	single-character	errors	is,	in	general,	easy	compared	to	multiple-character	
errors	in	text.	The	intentional	text	errors	in	social	media	text	are	generally	multiple-character	errors	and,	therefore,	challenging	to	handle	with	traditional	spell	checkers.
3.3.2 Long and short word errors
This	categorization	of	errors	is	made	to	show	the	general	cause	of	OOV	words	based	on	the	
length	of	the	words	by	showing	the	relation	between	the	word	length	and	the	chances	of	
OOV	word	generation.	The	literature	shows	a	higher	probability	of	spelling	mistakes/errors	
in	long	words	compared	to	short	words	Khan	and	Lee	(2020);	Bhatti	et	al.	(2014).
3.3.3 First and nth letter errors
The	OOV	words	could	be	included	in	a	text	due	to	mistakes	by	inserting	the	wrong	character/s	
at	different	positions.	Based	on	the	position	of	the	wrong	character/s,	the	OOV	words	can	
be	categorized	into	first	and	nth-letter	errors	Bhatti	et	al.	(2014).	Any	unintended	change	in	
the	first	character	of	a	word	that	results	in	an	OOV	word	is	termed	the	first-letter	error	(e.g.,	
"Hello"	→	"Jello").	On	the	other	hand,	the	mistake/change	in	a	word	at	the	nth	position	that	
results	in	an	OOV	word	is	known	as	an	nth-letter	error.	For	instance,	"Hello"	→	"Heklo"	
represents	an	example	of	an	nth	(i.e.,	n	=	3)	letter	error.	The	first	and	nth	letter	errors	can	
be	 treated/handled	 differently	 depending	 upon	 their	 importance	 in	 the	 target	 application.	
For	instance,	research	suggests	that	words'	first	and	last	letters	are	more	important	than	the	
interior	letters	during	reading	Johnson	and	Eisler	(2012).
Moreover,	errors	in	the	first	character	affect	visual	word	recognition	more	than	errors	in	
the	nth	character	Aschenbrenner	et	al.	(2017).	Eger	et	al.	(2020)	examine	the	robustness	of	
the	RoBERTa	Liu	et	al.	(2019)	model	against	textual	variations,	including	inner-shuffle	and	
full-shuffle.	The	inner	shuffle	randomly	shuffled	all	letters	in	the	word	except	the	first	and	
last,	whereas	there	was	no	first	and	last	letter	constraint	in	the	full	shuffle.	The	simulation	
results	show	that	the	model	was	more	robust	against	the	inner-shuffle	attack	compared	to	the	
full-shuffle,	indicating	the	importance	of	the	first	letter	in	word	identification.
4 The taxonomy of text preparation methods utilized in social media 
text analysis
Figure 2	provides	an	overview	of	preparation	steps,	which	involve	different	strategies	for	
learning	and	normalization	of	text	to	deal	with	the	textual	variations	in	a	general	framework	
of	social	media	text	analysis	for	different	applications.	These	methods	can	be	divided	into	
two	categories.	The	first	category	includes	more	conventional	methods,	such	as	tokenization,	part-of-speech	(POS)	tagging,	removal	of	special	characters,	etc.,	in	the	upper	left	box	
of	the	figure	titled	"Traditional	Pre-processing."	The	second	category	includes	methods	for	
dealing	with	textual	variations	and	the	resultant	OOV	words,	as	highlighted	in	the	upper	
right	side	of	the	figure	titled	"Social	Media	OOV	Words	Handling."
1 3
89 Page 14 of 48

---


<!-- PAGE 15 -->

Textual variations in social media text processing applications:…
As depicted in Fig. 2,	in	social	media	applications,	generally,	the	conventional	methods	
are	employed	to	clean	the	data,	which	are	then	followed	by	the	pre-processing	methods	
aiming	at	dealing	with	textual	variations	and	the	substitution	of	OOV	words	by	the	corresponding	standard	words.	This	survey	is	more	focused	on	the	latter	part;	however,	the	
conventional	methods	are	commonly	used	as	a	first	step	in	social	media	application	and	are	
thus also discussed in the paper.
Figure 3	provides	a	taxonomy	of	pre-processing	techniques	for	social	media	text	processing.	These	methods	are	roughly	divided	into	two	groups,	namely	(i)	traditional	pre-processing	and	(ii)	OOV	word	handling	methods.	In	the	next	subsection,	we	provide	a	detailed	
overview	of	these	methods	and	associated	challenges.
4.1 The traditional text preparation methods
In	this	section,	we	discuss	some	commonly	used	conventional	pre-processing	techniques	for	
text-processing	applications.
4.1.1 Tokenization
Tokenization,	one	of	the	most	common	pre-processing	techniques,	involves	breaking	down	
unstructured	text	(paragraphs	or	sentences)	into	smaller	pieces	known	as	tokens	(words,	
sub-words,	and	characters).	These	tokens	serve	as	the	basis	for	stemming	and	lemmatization	
and	can	help	extract	hidden	patterns	in	the	text.	Tokenization	can	be	carried	out	at	different	
levels	depending	on	the	requirements	of	the	underlying	applications.	Some	of	the	commonly	used	types	of	tokenization	are:
Fig. 2	An	overview	of	the	pre-processing	steps	in	a	generic	social	media	text	processing	application.	The	
traditional	pre-processing	methods	are	generally	used	as	a	first	step	in	cleaning	the	data.	Text	normalization	methods	are	then	employed	to	replace	OOV	words	with	the	corresponding	standard	words
 
1 3
Page 15 of 48 89

---


<!-- PAGE 16 -->

J. Khan et al.
Fig. 3	A	taxonomy	of	the	pre-processing	techniques
 
1 3
89 Page 16 of 48

---


<!-- PAGE 17 -->

Textual variations in social media text processing applications:…
 ● Word	Tokenization:	It	is	the	simplest	form	of	tokenization	where	a	piece	of	text	is	broken	down	into	single/separate	words	using	delimiters,	such	as	","	or	";"	or	",".	One	of	
the	main	limitations	of	word	tokenization	is	its	inefficacy	in	dealing	with	OOV	words,	
which	are	represented	as	unknown	words.	Since	OOV	words	are	very	common	in	social	
media	text,	this	method	is	not	suited	for	social	media	text	processing	applications.
 ● Character	Tokenization:	This	method	allows	breaking	down	a	piece	of	text	into	individual	characters.	The	method	is	introduced	to	overcome	some	of	the	key	limitations	of	
word	tokenization.	For	instance,	the	method	can	retain	OOV	words	during	the	tokenization	process.	Similarly,	the	method	does	not	suffer	from	vocabulary	issues	as	it	only	
needs	the	underlying	language's	characters.	For	example,	the	vocabulary	of	the	method	
for	the	English	text	process	should	contain	all	26	characters	of	the	English	language.	
Character	tokenization	also	has	some	drawbacks.	For	instance,	the	length	of	the	output	
vector	of	the	method	is	very	high,	even	for	a	smaller	paragraph/sentence.
 ● Sub-word	Tokenization:	In	contrast	to	word	and	character	tokenization,	sub-word	tokenization	allows	breaking	down	a	piece	of	text	into	sub-words	using	linguistic	rules.	
This	method	overcomes	the	limitations	of	both	character	and	word	tokenization.	Since	
the	tokens	have	more	than	a	single	character,	the	output	vector	is	smaller	compared	to	
character	tokenization.	On	the	other	hand,	its	ability	to	break	off	affixes	allows	it	to	deal	
with	OOV	words	by	providing	additional	insights	into	how	unknown	words	function.3
4.1.2 PoS tagging
Part-of-speech	(POS)	tagging	labels	each	word	of	an	input	text	with	its	appropriate	parts	
of	speech	(such	as	nouns,	verbs,	etc.)	based	on	its	definition	and	context.	POS	tagging	is	a	
valuable	tool	in	NLP	as	it	allows	algorithms	to	understand	the	grammatical	structure	of	a	
sentence	and	to	disambiguate	words	with	multiple	meanings.	Most	POS	tagging	falls	under	
the	following	categories.
 ● Rule-based	POS	Tagging:	Rule-based	POS	tagging	is	a	knowledge-driven	method	for	
tagging	textual	tokens	based	on	manually	defined	rules	or	linguistic	rules.	The	rulebased	POS	can	be	carried	out	both	manually	and	automatically.	The	former	method	
involves	hand-written	or	user-specified	rules	for	tag	disambiguation.	In	the	linguistic	
rules-based	PoS	tag,	disambiguation	is	carried	out	by	analyzing	the	linguistic	features	
of	the	target	words	in	the	context	of	their	preceding	and	following	words.	For	instance,	
if	the	target	word	follows	an	article,	it	must	be	a	noun.
 ● Stochastic	POS	tagging:	Stochastic	POS	tagging	methods	are	based	on	the	likelihood/
probability	of	a	tag	occurring.	These	methods	are	based	on	diverse	techniques,	such	as	
Maximum	Likelihood	Estimation	(MLE),	n-grams,	or	Hidden	Markov	Models	(HMM).	
The	most	commonly	used	statistical	measures	for	POS	tagging	are	based	on	word	frequency	and	tag	sequence	probability,	which	requires	a	training	corpus.	The	simplest	
method	selects	the	most	frequent	tags	associated	with	a	word	in	the	training	corpus.	
This	method	is	limited	due	to	its	full	dependence	on	the	training	corpus,	e.g.,	the	probability	of	the	words	not	included	in	the	training	corpus	is	zero.POS	tagging	is	typically	performed	using	ML	algorithms,	which	are	generally	trained	on	a	large	annotated	
corpus	of	text.	The	algorithms	learn	to	predict	the	correct	POS	tag	for	each	word	by	
3   h	t	t	p	s	:	/	/	t	i	n	y	u	r	l	.	c	o	m	/	2	w	p	3	8	n	8	4 .  
1 3
Page 17 of 48 89

---


<!-- PAGE 18 -->

J. Khan et al.
considering	the	definition	and	the	context	in	which	the	word	is	used.	Some	commonly	
used	traditional	PoS	tagging	methods	are	based	on	statistical	models,	such	as	HMM,	
Maximum	Entropy	Markov	Models	(MEMMs),	Conditional	Random	Fields	(CRF),	
and	linear	classifiers,	such	as	SVM-based	taggers.	These	models	are	generally	trained	
on	hand-crafted	features.	Most	of	the	earlier	works	on	POS	tagging	for	social	media	
text	in	different	languages	are	based	on	hand-crafted	features	Owoputi	et	al.	(2013);	
Nooralahzadeh	et	al.	(2014).	However,	recently,	the	trend	shifted	towards	Deep	Learning	(DL)	methods	Meftah	and	Semmar	(2018).	OOV	words	also	pose	challenges	for	
POS	tagging	algorithms.	This	is	mainly	due	to	the	lack	of	these	OOV	words	in	the	standard	dictionaries	or	training	corpora	used	by	POS	taggers	Gimpel	et	al.	(2011);	Baig	et	al.	
(2020).	The	performance	of	the	algorithms	is	even	worse	with	rare	and	domain-specific	
OOV	words	Lochter	et	al.	(2020).	Bach	et	al.	Bach	et	al.	(2018)	conducted	an	empirical	study	on	POS	tagging	for	Vietnamese	social	media	text	to	highlight	the	challenges	
to	the	POS	tagger	trained	on	conventional	text.	They	developed	a	new	POS	tagger	for	
Vietnamese	social	media	text.
4.1.3 Chunking (shallow parsing)
Chunking	is	used	to	identify	and	extract	POS	and	phrases	in	the	text.	It	mainly	involves	the	
identification	of	constituent	parts	of	sentences	(i.e.,	nouns,	verbs,	etc.)	and	linking	them	to	
higher-order	units	having	discrete	grammatical	meanings	(i.e.,	noun/verb	groups	or	phrases,	
etc.).	The	basic	goal	of	Chunking	is	to	make	groups	of	"noun	phrases",	which	adds	structure	to	the	sentence	by	following	POS	tagging	combined	with	regular	expressions.	The	
resulting	groups	of	words	are	called	"chunks".	The	chunking	techniques	can	be	classified	
as	(i)	Chunking	up	or	(ii)	Chunking	down.	The	former	aims	at	a	higher	level	(i.e.,	general/

## Abstract
)	of	information,	while	the	latter	aims	at	more	specific	or	detailed	information.	The	
literature	reports	several	interesting	chunking	techniques.	Most	methods	are	based	on	supervised	learning	for	text	chunking	by	training	different	ML	algorithms	Muis	and	Lu	(2016);	
Zhai	et	al.	(2017).	However,	similar	to	POS,	supervised	chunking	methods	face	difficulties	
in	handling	OOV	words	due	to	the	lack	of	training	samples.	Some	methods	also	rely	on	
unsupervised	methods.	For	instance,	Borrelli	et	al.	(2020)	proposed	an	n-gram	frequencybased	method	for	the	chunking	of	Twitter	tweets.	Similarly,	some	unsupervised	methods,	
such	as	Adjacent	Sequence	Clustering	(ASC),	which	is	based	on	the	semantic	similarity	
of	words,	also	suffer	from	the	presence	of	OOV	words.	However,	methods	like	Langchain	
Character	Text	Splitter	(LCTS),	which	are	based	on	the	number	of	characters,	may	not	be	
affected	by	the	presence	of	OOV	words	as	they	do	not	rely	on	any	training	data.
4.1.4 Text standardization
Text	standardization,	which	transforms	text	into	a	single	canonical	form,	is	a	preprocessing	step	aiming	at	enhancing	the	quality	of	the	text.	Text	normalization	generally	involves	
a	series	of	operations	and	tasks	to	prepare	the	text	for	processing.	Some	key	tasks	of	text	
normalization	are	described	as	follows.
 ● Stemming:	Stemming,	which	involves	the	elimination	of	affixes	from	a	word	to	obtain	
a	word	stem/root,	is	critical	in	several	NLP	applications,	such	as	text	recognition	and	
1 3
89 Page 18 of 48

---


<!-- PAGE 19 -->

Textual variations in social media text processing applications:…
retrieval	Moral	et	al.	(2014).	It	reduces	words	to	their	word	stem/base/root	form,	for	
example,	running	→	run,	tables	→	table,	booked	→	book,	etc.	In	the	context	of	social	
media	 text,	 it	 not	 only	 helps	 in	 coping	 with	 sparsity	 issues	 but	 also	 plays	 its	 part	 in	
standardizing	vocabulary.	Stemming	can	be	carried	out	in	different	ways.	Some	of	the	
commonly used approaches are:
 - Truncation-based	Methods:	These	methods	aim	at	removing	affixes	(suffixes	or	
prefixes)	of	a	word.	One	of	the	basic	methods	in	this	category	truncates	the	nth	
and	onward	symbols/characters	in	words	(i.e.	keeps	n	letters	and	removes	the	rest)	
Bhamidipati	and	Pal	(2007).	More	complex	truncation-based	stemming	algorithms	
involve	removing	affixes	by	truncating	the	morphological	and	inflexional	endings	
from	words	Moral	et	al.	(2014).
 - Statistical	Methods:	The	stemmers	in	this	category	are	based	on	statistical	analysis.	
Some	commonly	used	statistical	stemming	methods	include	N-gram	stemmer	Mayfield	and	McNamee	(2003),	HMM-based	stemmer	Melucci	and	Orio	(2003),	and	
Yet	another	suffix	stripper	(YASS)	stemmer	Majumder	et	al.	(2007).
 - Inflectional	and	Derivational	Methods:	These	stemming	methods	rely	on	the	inflectional	and	derivational	morphology	analysis.	In	the	case	of	inflectional	analysis,	the	
stemmers	rely	on	grammatical	information,	such	as	plural,	number,	tense,	agreement,	and	case.	In	derivational	analysis,	the	stemmers	truncate	the	inflected/derived	
words.	Some	of	the	commonly	used	inflectional	and	derivational	stemmers	include	
Krovetz	stemmer	(KSTEM)	Krovetz	(1993),	and	Xerox	Inflectional	and	Derivational	Analyzer	Grefenstette	(1996)
 - Corpus-based	Methods:	These	methods	rely	on	a	corpus	by	looking	for	word	variants	co-occurrence	in	the	corpus	for	stemming.	These	methods	can	be	further	categorized	into	Lexicon	features/analysis-based	and	Corpus	analysis-based	methods	
Singh	and	Gupta	(2019).
 ● Lemmatization:	Lemmatization	is	another	key	task	in	text	normalization.	Despite	having	
several	similarities,	lemmatization	differs	from	stemming	in	several	ways	Balakrishnan	
and	Lloyd-Yemoh	(2014).	For	instance,	stemming	stems/truncates	the	last	few	characters	from	a	word,	which	may	result	in	incorrect	meanings	and	spelling.	However,	lemmatization	always	results	in	meaningful	words	by	considering	the	context	in	which	the	
words	are	used.	To	this	aim,	lexical	knowledge	is	used	to	obtain	the	correct	base	forms	
of	the	underlying	word.	It	also	makes	use	of	POS	tagging	for	transforming	the	word	into	
a	proper	root	form	with	additional	computational	overhead.
 ● Case	Conversion:	Text	documents	in	general	and	social	media	text	in	particular	often	
contain	capital	words.	Machines	treat	these	capitalized	words	differently,	which	may	
result	in	incorrect	analysis.	To	avoid	such	issues,	generally,	in	pre-processing,	the	entire	
text	is	converted	into	lower	or	uppercase,	depending	on	the	requirements	of	the	underlying	application.	However,	this	case	conversion	may	result	in	the	loss	of	critical	information	in	certain	applications.	For	instance,	social	media	users	generally	use	upper-case	
words	to	emphasize	something	or	express	the	intensity	of	their	emotions,	which	could	
be critical in sentiment analysis and emotion recognition applications.
 ● Treatment	for	Numbers:	Text	normalization	also	involves	converting	numbers	into	
words	and	vice	versa,	depending	on	the	requirements	of	the	underlying	applications.	
1 3
Page 19 of 48 89

---


<!-- PAGE 20 -->

J. Khan et al.
Sometimes,	numbers	are	completely	removed	from	the	text.	For	instance,	in	certain	text	
processing	applications,	such	as	sentiment	analysis,	numbers	generally	do	not	provide	
any	meaningful	information	and	thus	can	be	removed	during	pre-processing.	However,	
the	numbers	may	convey	key	information	in	certain	text-processing	applications,	such	
as named entity recognition or chatbots.
4.1.5 Handling of noisy text
This	task	mainly	involves	the	removal	of	unnecessary	information.	Some	of	the	common	
subtasks include:
 ● Remove/replace	URLs:	The	URLs	in	the	informal	text	contribute	little	value	to	the	text	
classification	task	as	they	carry	no	helpful	information.	For	example,	In	the	following	
text,	"https://www.coupang.com/	is	the	most	reliable	and	cheap	online	shopping		p	l	a	t	f	o	
r	m	in	South	Korea."	The	URL	in	this	review	does	not	contain	any	positive	or	negative	
information,	although	occasionally,	it	could	make	a	false	prediction.	Therefore,	it	is	
good	to	remove/replace	the	URLs	before	text	classification	to	avoid	unnecessary	information	and	false	predictions.	The	URL	removal	may	result	in	the	loss	of	some	useful	
information,	as,	in	the	case	of	the	above	example,	the	removal	of	the	URL	will	result	in	
the	loss	of	the	subject,	"Coupang."	It	is	a	better	practice	to	replace	the	URLs	with	their	
representative	tokens.
 ● Convert	Accented	Characters:	The	accented	characters	are	utilized	to	emphasize	certain	
words	in	the	text.	In	some	cases,	the	accented	characters	are	used	to	clarify	the	meaning	
of	the	word,	which	might	be	different	from	that	without	accented	characters.	However,	
accents	are	mostly	induced	by	typing	style	or	mistakes.	For	Example,	"I	would	like	you	
to	have	latté	at	my	café?"	Here,	the	words	"latté"	and	"café"	have	the	same	meaning	
as	"latte"	and	"cafe",	respectively.	But	NLP	models	may	treat	them	as	different	words.	
Thus	the	conversion	of	the	accent	words	into	standard	words	is	a	better	practice.
 ● Remove	Special	Characters	and	Punctuation:	Special	characters	are	non-alphanumeric	
characters	that	have	a	certain	meaning	in	written	communication.	These	special	characters	are	usually	used	as	punctuation,	currency	representation,	mathematical	symbols,	
and	relationship	expression.	In	online	social	media	communication,	most	people	use	
them	to	express	their	thoughts	precisely.	When	simultaneously	read	with	words,	these	
characters	may	result	in	misclassification.	For	example,	the	words	"#bad"	and	"#good"	
are	not	recognized	by	the	machine.	These	special	characters	need	to	be	removed	to	
avoid	discrepancies	in	sentiment	classification.	Similarly,	punctuation	removal	helps	to	
treat	the	text	equally.	For	example,	"hello"	and	"hello!"	are	treated	equally	after	punctuation	removal.	However,	one	needs	to	be	more	careful	while	removing	punctuations	
due	to	the	use	of	contraction	words	and	dialectal	usage	of	words	in	informal	communication.	These	words	may	lose	their	meaning	after	punctuation	removal.
 ● Removing	Stopwords:	Stopwords	are	commonly	used	in	the	text.	In	NLP	tasks	like	
sentiment	analysis	or	text	categorization,	words	like	"we"	and	"are"	often	do	not	add	
much	value.	Therefore,	these	words	are	often	removed	to	save	computational	time	and	
resources	while	processing	big	textual	data.	The	NLTK	library	contains	a	list	of	the	most	
frequent	stopwords	in	the	English	language,	which	are	generally	utilized	to	remove	
stopwords	from	the	text.	However,	based	on	the	target	application	and	data,	a	custom1 3
89 Page 20 of 48

---


<!-- PAGE 21 -->

Textual variations in social media text processing applications:…
ized	list	of	stopwords	can	also	be	developed	to	avoid	information	loss.	For	example,	
"how"	can	be	a	stopword	in	many	applications,	but	it	could	be	useful	for	the	classifier	in	
applications	like	customer	query	classification	and	analysis.	Similarly,	the	word	"not"	
generally	hints	at	negative	opinion	in	sentiment	analysis;	however,	it	is	included	in	the	
list	of	stopwords	of	several	NLP	libraries.
4.2 Out-of-vocabulary words handling
The	traditional	pre-processing	methods	discussed	above	ensure	the	removal	of	undesired	
and	non-informative	contents,	improving	text	analysis	algorithms'	performance.	However,	
it	does	not	guarantee	the	handling	of	OOV	words,	which	are	frequently	used	in	social	media	
texts.	These	intentional	and	unintended	OOV	words	convey	key	information	in	different	
social	media	text	applications.	In	the	literature,	various	pre-processing	techniques	have	been	
reported	to	handle	these	OOV	words	in	a	social	media	text.	These	methods	include	OOV	
word	filtering	Verma	and	Bhattacharyya	(2009),	lexicon	creation	Hu	and	Liu	(2004);	Dinakar	et	al.	(2015),	data-driven	approaches	Kiritchenko	et	al.	(2014),	and	text	normalization	
Sharma	et	al.	(2015).	These	approaches	are	described	as	follows.
4.2.1 Filtering
Filtering	is	the	simplest	method	of	handling	OOV	words.	In	this	approach,	OOV	words	
are	dropped.	As	discussed	earlier,	traditional	pre-processing	has	widely	used	filtering	to	
filter	out	noisy	data.	The	same	approach	is	adopted	for	handling	OOV	words.	For	instance,	
Verma	and	Bhattacharyya	(2009),	and	Habash	and	Metsky	(2008)	adopted	a	filtering	technique	to	deal	with	the	OOV	words	in	English	and	Urdu	text,	respectively.	However,	several	
challenges	are	associated	with	general	data	cleaning	and	filtering.	A	detailed	overview	of	
such	challenges	has	been	provided	by	Chu	et	al.	(2016).	One	of	the	key	limitations	of	filtering	out	OOV	words	is	the	loss	of	useful	information	conveyed	by	these	words,	especially	
the	deliberately	generated	OOV	words.	The	OOV	words	(including	both	intentional	and	
unintentional)	could	be	useful	in	different	social	media	text	processing	applications,	such	
as	sentiment	analysis,	author	profiling,	and	style	change	detection	Zangerle	et	al.	(2021);	
Zamir	et	al.	(2023).
4.2.2 OOV words lexicon
One	of	the	key	limitations	of	filtering	is	the	possibility	of	a	loss	of	key/relevant	information.	In	order	to	cope	with	such	issues,	several	interesting	methods	have	been	proposed	to	
preserve	the	information	contained	in	the	OOV	words.	One	such	method	is	the	creation	of	
a	corpus	of	OOV	words	along	with	their	proper	definition	for	the	target	tasks.	The	methods	
involving	the	creation	of	such	a	corpus	have	been	adopted	in	several	works	to	mitigate	
the	problem	of	information	loss	faced	in	traditional	text	analysis	methods	Puigcerver	et	
al.	(2017).	The	creation	of	the	OOV	words	lexicon	can	be	divided	into	the	following	two	
classes.
 ● Manual	lexicon:	In	this	method,	a	list	of	manually	collected	words	that	are	not	listed	as	
valid	words	in	the	existing	lexicon	is	created.	This	method	has	been	successfully	utilized	
1 3
Page 21 of 48 89

---


<!-- PAGE 22 -->

J. Khan et al.
to	minimize	information	loss	due	to	OOV	words	in	different	text	classification	applications	Sun	et	al.	(2017).	For	instance,	Stone	et	al.	(1966)	manually	created	a	corpus	
containing	3600	words	for	content	analysis	in	behavioral	sciences.	The	authors	reported	
several	techniques	and	procedures	for	identifying	reoccurring	patterns	by	humans	in	
their	communication.	Similarly,	Hu	and	Liu	(2004),	and	Mohammad	et	al.	(2010,	2013)	
developed	manual	corpora	containing	6800	and	14000	manually	annotated	OOV	words	
for	sentiment	and	opinion	analysis	in	English	text.	On	the	other	hand,	Sharma	et	al.	
(2015)	developed	a	large	corpus	of	OOV	words	for	cross-lingual	information	retrieval	
in	Hindi	and	English.	More	recently,	Khan	and	Lee	(2021)	collected	a	list	of	the	most	
frequent	user-generated	abbreviations	from	various	online	data	sources	and	replaced	
them	with	their	full	form	for	text	analysis.	Despite	being	one	of	the	effective	ways	of	
avoiding	loss	of	information	due	to	OOV	words,	the	method	has	several	limitations	
regarding	time	and	resource	inefficiency.
 ● Automatic	lexicon	Several	automatic	methods	for	language	resource	creation	have	been	
reported	in	the	literature	to	avoid	the	cost	associated	with	manual	lexicon	preparation.	
These	automatic	methods	leverage	statistical,	probabilistic,	and	data-driven	approaches	
for	lexicon	creation.	For	instance,	Roark	and	Charniak	(2000)	proposed	a	semi-automatic	method	relying	on	the	frequency	of	noun-phrase	co-occurrence	for	generating	a	
semantic	lexicon	in	English.	Amati	et	al.	(2008),	on	the	other	hand,	automatically	developed	an	opinion-labeled	English	lexicon	where	the	term	frequency	divergence	scores	
the	selection	of	subjective-term	candidates.	Asghar	et	al.	(2019)	developed	an	automatic	
lexicon	for	sentiment	analysis	in	the	Urdu	language.	More	recently,	Li	et	al.	(2020)	proposed	an	effective	method	relying	on	Word2Vec,	a	semantic	relationship	graph,	and	label	propagation	algorithms	for	automatically	constructing	a	depression-domain	lexicon	
in	Chinese.	Similarly,	Tan	(2020)	presented	a	robust	frame-based	approach	for	creating	
an	English	dictionary.	Several	other	studies	also	explored	the	feasibility	of	the	automatic	
creation	of	lexicon,	such	as	methods	presented	in	Viegas	et	al.	(2020);	Esposito	et	al.	
(2020);	Masadeh	and	Sa'ad	Al-Azzam	(2020);	Wang	et	al.	(2020).	These	lexicon-based	
techniques	can	handle	noise	in	social	media	text	by	building	a	lexicon	of	the	noisy	
words;	however,	they	are	strictly	domain-specific	and	application-dependent.
4.2.3 Emoji/emoticons decoding
The	use	of	emojis/emoticons	in	social	media	texts	is	very	common,	and	they	represent	different	things,	including	emotions,	facial	expressions,	postures,	household	items,	and	slang.	
The	emoticons	are	generally	constituted	by	short	sequences	of	ASCII	characters	(i.e.,	symbols,	letters,	or	numbers),	shift	JIS	&	Unicode	art,	and	other	static	and	animated	icons.	
These	emoji/emoticons	convey	useful	information	in	several	text	analysis	applications,	such	
as	sentiment	analysis,	market	trend	detection,	hate	speech,	and	slang	detection	Arafah	and	
Hasyim	(2019);	Wijeratne	et	al.	(2020);	Peacock	and	Khan	(2019);	Ibrohim	et	al.	(2019).	
For	instance,	Brants	et	al.	Brants	et	al.	(2019),	on	the	other	hand,	conducted	a	study	with	
386	participants	to	analyze	the	meaning	of	nine	different	emojis.	The	authors	concluded	
that	the	emojis	represent	different	emotions,	including	anger,	sadness,	joy,	surprise,	and	a	
neutral state.
To	make	better	use	of	these	emojis	in	text	analysis	applications,	each	icon	is	transformed	
into	a	word/phrase	expressing	the	same	information	(i.e.,	expressions,	mood,	item,	etc,).	
1 3
89 Page 22 of 48

---


<!-- PAGE 23 -->

Textual variations in social media text processing applications:…
The	literature	reports	several	inventories	of	emojis	and	their	corresponding	meanings	in	
different	languages.	For	instance,	Wijeratne	et	al.	(2017)	developed	a	large-scale	inventory,	
namely	EmojiNet,	containing	12,904	sense	labels	and	context	words	associated	with	a	total	
of 2389 emojis. Emoji dictionary 4	is	another	inventory	of	emojis	and	the	corresponding	
sense	labels.	The	labels	are	assigned	by	volunteers	based	on	the	message	conveyed	by	each	
emoji in the sentences.
4.2.4 Text normalization
Text	normalization	is	another	technique	employed	to	overcome	the	limitations	of	lexiconbased	OOV	word	handling	methods,	such	as	loss	of	information	and	application	dependencies,	in	social	media	text	analysis.	Normalization,	which	involves	multiple	tasks,	transforms/
translates	noisy	social	media	text	into	its	canonical	(i.e.,	standard).	The	literature	reports	the	
effectiveness	of	text	normalization	in	handling	noisy	text	with	OOV	words	in	a	diversified	set	of	social	media	text	processing	applications,	such	as	sentiment	analysis	Sharma	
et	al.	(2015),	language	detection	Wu	et	al.	(2020),	and	text-speech	synthesis	Silverman	et	
al.	(2013),	etc.	Text	normalization	has	also	been	proven	very	effective	in	defense	against	
adversarial	attacks	Alsmadi	et	al.	(2022).	Some	key	tasks	involved	in	text	normalization	are	
described	below.
4.2.4.1 Spell	checker		 Spell	checking	is	one	of	the	primary	tasks	of	text	normalization.	
In	this	task,	the	OOV	words	are	treated	as	misspelled	words,	and	different	spell	correction	
techniques	are	used	to	correct	deliberate	and	unintentional	spell	errors.	The	literature	reports	
several	works	relying	on	spell	error	correction	methods	for	handling	noisy	text.	For	instance,	
Khan	and	Lee	(2020)	and	Lertpiya	et	al.	(2020)	adopted	the	spell	error	correction	strategy	
for	handling	noisy	text	and	replacing	the	OOV	words	with	the	corresponding	meaningful	
words	in	English	and	Thai	text,	respectively.	Some	key	techniques	used	for	spell	correction	
include	edit	distance	Liang	et	al.	(2008),	similarity	key	Xie	and	Jiang	(2007),	rule-based	
methods	Downs	et	al.	(2020),	N-gram	Priya	et	al.	(2017),	probabilistic	models-based	spell	
checking	Sasu	(2011),	neural	network	Hovermale	(2008),	and	auto-encoders-based	spell	
checking	Lee	et	al.	(2020).	The	edit	distance	technique,	which	is	based	on	the	number	of	
editing	operations	required	for	the	correction,	is	one	of	the	most	widely	explored	spellchecking	methods	in	the	literature	Islam	et	al.	(2019).	On	the	other	hand,	the	similarity	key	
technique	is	based	on	the	assumption	that	the	words	with	similar	spells	have	similar	keys	
and,	hence,	pick	the	words	with	similar	spells	from	a	lexicon.	The	N-gram-based	techniques	
are	generally	used	in	combination	with	other	methods,	such	as	probabilistic	methods	Khan	
and	Lee	(2020).	Most	of	the	recent	methods	rely	on	NNs	for	spell-checking.	For	instance,	
Lee	et	al.	(2020)	employed	auto-encoders	for	context-aware	spell-checking	in	English	text.
Spell	checking	and	correction	are	widely	explored	topics.	However,	the	textual	variations	
in	the	user-generated	text	of	social	media	have	opened	new	avenues	in	the	domain.	The	
challenges	associated	with	social	media	text	are	beyond	the	scope	of	conventional	simple	
spell-checking	and	correction	techniques.	Some	key	challenges	in	spell	checking/correction	
include	OOV	slang,	punctuation	and	omissions	errors,	short	forms	and	acronyms,	misspelling,	and	recognition	of	OOV-named	entities	Clark	et	al.	(2010).	One	of	the	key	limitations	
4   h	t	t	p	s	:	/	/	e	m	o	j	i	d	i	c	t	i	o	n	a	r	y	.	e	m	o	j	i	f	o	u	n	d	a	t	i	o	n	.	c	o	m	/	l	e	a	r	n .  
1 3
Page 23 of 48 89

---


<!-- PAGE 24 -->

J. Khan et al.
of	the	conventional	spell-checking	and	correction	methods	is	their	inability	to	cope	with	the	
intentionally	generated	OOV	words	in	a	social	media	text.
The	literature	already	reports	some	works	aiming	at	dealing	with	intentional	OOV	words	
in	a	social	media	text.	For	instance,	Han	and	Baldwin	(2011)	proposed	a	morpho-phonemic	
similarity-based	approach	for	the	correction	of	OOV	words	in	English	text.	Liu	and	Weng	
(2015),	on	the	other	hand,	explored	the	task	from	the	human	behavior	perspective	of	word	
normalization	through	enhanced	letter	transformation,	visual	priming,	and	string/phonetic	
similarity.
4.2.4.2 Word	shortening	Shortening	words	is	very	common	in	social	media	outlets.	Words	
are	generally	shortened	to	save	some	space	or	avoid	cumbersome	phrases,	which	leads	to	
better	readability	Boot	et	al.	(2019).	However,	such	user-defined	abbreviations	(i.e.,	shortened	words)	make	automatic	processing	of	the	text	more	challenging	Khan	and	Lee	(2020).	
In	social	media,	informal	text/communication,	the	deletion	of	vowels	(e.g.,	using	"msg"	→ 
"message,")	and	repeated	characters	(e.g.,	"tmrw"	→	"tomorrow")	is	very	common	Eisenstein	(2013).	Moreover,	deleting	the	silent	and	some	other	characters	that	have	less	significance	in	pronouncing	a	word,	such	as	"h,"	is	also	a	common	practice	in	social	media.	The	
literature	reports	various	attractive	solutions	for	tackling	this	issue,	ranging	from	rule-based	
to	probabilistic	approaches.	For	instance,	Pennell	and	Liu	(2010)	proposed	a	handcrafted	
rules-based	method	for	the	identification	and	recovery	of	standard	words	from	the	corresponding	shortened	words/abbreviations	in	English.	Hassan	and	Menezes	(2013)	proposed	
a	graph-based	unsupervised	method	by	employing	Random	Walks	on	a	contextual	similarity	
graph	of	n-gram	sequences.	Moreover,	the	authors	highlighted	several	challenges	associated	
with	recovering	standard	words	from	shortened	words	and	demonstrated	how	the	proposed	
method	could	overcome	these	challenges.
4.2.4.3 Removing	repetition	of	alphabets	In	social	media,	the	word	enlargement,	by	repeating	certain	characters	(e.g.,	"coooooool"),	is	a	common	practice	to	stress,	emphasize,	or	
highlight	certain	emotions.	Though	this	enlargement	could	be	critical	in	specific	applications,	such	as	sentiment	analysis,	these	repeated	characters	are	sometimes	removed	to	
recover	valid	words.	For	instance,	Mohammad	et	al.	(2013)	demonstrated	the	importance	
of	the	removal	of	such	repetition	of	alphabets	in	English	words	for	the	improvement	of	
text	classification	techniques.	Several	other	recent	works	also	reported	character	repetitionremoval	as	a	practical	pre-processing	step	for	the	enhancement	of	the	performance	of	text	
analysis	techniques	Kumar	and	Garg	(2019);	Elzayady	et	al.	(2023)	in	English	and	Arabic	language,	respectively.	Some	interesting	solutions	for	recovering	the	standard	forms	of	
enlarged	words	include	considering	that	most	languages	do	not	allow	triple	characters	in	
a	word.	Fernández	et	al.	(2014)	removed	the	characters	that	are	repeated	more	than	three	
times,	e.g.,	"goood"	is	replaced	by	"good";	however,	"good"	will	remain	the	same.	Garg	
and	Chatterjee	(2014)	replaced	characters	repeating	more	than	twice	as	two	characters	in	
multi-lingual	social	media	text.	Based	on	the	assumption	that	the	repetition	of	characters	in	
standard	form	is	rare,	Khan	and	Lee	(2021)	proposed	the	replacement	of	repeated	characters	
by	a	single	instance	to	avoid	the	enlarged	OOV	words	in	English.	One	of	the	critical	limitations	of	the	method	is	the	inability	to	detect	the	repetition	of	characters	in	standard	words.	
1 3
89 Page 24 of 48

---


<!-- PAGE 25 -->

Textual variations in social media text processing applications:…
To	overcome	this	limitation,	the	authors	recommend	using	standard	spell-checkers	after	the	
proposed method.
4.2.4.4 Expansion	of	contractions/dialectal	usage	Contractions	are	shortened	words,	e.g.,	
don't	and	can't.	Contractions	are	widely	used	in	informal	written	and	spoken	communication,	especially	by	online	users,	to	reduce	character	counts.	In	contraction,	one	or	more	
letter(s)	are	replaced	with	an	apostrophe.	In	many	NLP	tasks,	the	contractions	are	expanded	
to	their	original	root	words	form	for	efficient	processing.	In	informal	text,	contractions	can	
be	single-word	contractions	such	as	"I'm"	 →	 "I	 am"	 or	 more	 complex	 expressions	 such	
as	"he'd've"	→	"he	would	have."	Arun	and	Srinagesh	(2020)	explored	the	impact	of	misspelled	words	and	contractions	on	sentiment	analysis	in	multi-lingual	social	media	text.	In	
the	study	conducted	by	Boia	et	al.	(2013),	contractions	in	English	tweets	were	replaced	with	
expanded	variants.	The	contractions	are	expanded	for	accurate	tokenization,	e.g.,	"can't"	is	
tokenized	to	"can"	and	"t"	when	not	expanded.
Dialectal	usage	means	replacing	multiple	words	with	single	or	multiple	OOV	words	
where	each	word	is	formed	by	combining	multiple	words	such	as	"are	not	→ aint" and "cannot →	cant."	The	simple	contraction	expansion	cannot	correct	such	errors	due	to	its	random	
and	unidentifiable	nature.	Khan	and	Lee	(2021)	proposed	a	word-to-sequence	approach	to	
resolve	the	problem	of	dialectal	usage	in	English	text.
4.2.4.5 Expanding	abbreviations	Another	common	practice	in	social	media	communication	is	the	use	of	self-defined	abbreviations.	The	use	of	abbreviations	is	part	of	several	languages,	and	each	has	a	set	of	standard	abbreviations	that	are	part	of	the	dictionary.	However,	
the	use	of	self-defined	abbreviations	in	social	media	text	results	in	OOV	words	that	make	it	
difficult	to	automatically	analyze	the	text	in	different	applications.	These	self-defined	abbreviations	are	generally	used	for	more	frequently	occurring	words,	such	as	"Good	Morning	→ 
GM	and	Good	Night	→	GN",	and	slang.	The	literature	reports	several	interesting	methods,	
including	manual	and	automatic	corrections	of	the	user-defined	abbreviations.	For	instance,	
Kolajo	et	al.	(2020)	employed	a	Lesk	algorithm-based	framework	for	handling	the	abbreviation/acronym	disambiguation	in	Nigerian	social	media	text.	More	recently,	Khan	and	Lee	
(2021)	proposed	a	corpus-based	solution	by	developing	a	dictionary	of	the	most	commonly	
used	user-defined	abbreviations	in	English	text,	such	as	"tbh"	→	"to	be	honest",	"tldr	→ 
"too	long	didn't	read",	and	"dyk"	→	"did	you	know".	The	user-defined	abbreviations	are	
collected	 from	 different	 online	 platforms/data	 sources	 of	 informal	 text.	 The	 user-defined	
abbreviations	are	generally	complicated	and	hard	to	detect.	One	of	the	key	limitations	of	the	
corpus-based	solution	is	its	dependency	on	a	fixed	static	list	of	abbreviations,	whereas	new	
abbreviations	emerge	very	frequently	in	social	media.
4.2.4.6 Slangs	identification	Slangs	represent	an	informal	language	generally	consisting	
of	words	and	phrases	that	target/attack	a	particular	group.	Several	social	media	platforms	
support	the	automatic	detection	and	blockage	of	slang;	however,	social	media	users	use	
different	OOV	words	for	slang	Saputra	and	Marlina	(2019).	For	instance,	in	social	media,	
shorthand	words	are	generally	used	for	slang,	making	their	automatic	detection	more	chal1 3
Page 25 of 48 89

---


<!-- PAGE 26 -->

J. Khan et al.
lenging.	To	cope	with	such	words,	the	literature	reports	several	interesting	solutions	exploring	different	aspects	of	the	task.	For	instance,	Khan	et	al.	(2016)	replaced	the	English	slang	
words	with	their	complete	form	to	perform.	To	this	aim,	a	slang	dictionary	Khan	and	Lee	
(2021)	of	commonly	used	slang	in	social	media	is	developed	from	various	sources.	Napitu	
and	Suhardianto	(2020),	on	the	other	hand,	proposed	a	sociolinguistics	approach	for	analyzing	abbreviations	used	for	slang	on	Instagram	in	English.
4.2.4.7 Phonetic	substitution	Another	common	practice	in	social	media	text	is	using	phonetically	similar	words	instead	of	the	corresponding	standard	words,	e.g.,	"gr8"	→	"great".	
Such	phonetic	substitution	of	words	results	in	different	OOV	words,	making	automatic	text	
analysis	more	challenging.	Several	interesting	solutions	have	been	proposed	in	the	literature	
to	recover	standard	words	from	phonetically	similar	OOV	words.	For	instance,	rule-based	
adaptive	approaches	are	proposed	by	Saloot	et	al.	(2014)	and	Desai	et	al.	(2015)	to	deal	with	
OOV	words	that	result	from	the	substitution	of	phonetically	similar	words.	Similarly,	Doshi	
et	al.	(2020)	proposed	using	a	phonetic	and	string	similarity-based	approach	to	recover	standard	words	from	the	corresponding	phonetically	similar	OOV	words	in	English	text.	The	
literature	also	reports	the	use	of	HMM	and	probabilistic	model-based	approaches	to	recover	
standard	words	from	phonetically	similar	OOV	words	Sikdar	and	Chatterjee	(2020).	Comparatively	better	results	are	reported	for	the	probabilistic	model-based	approaches	compared	
to	HMM-based	solutions	Chatterjee	(2019).	More	recently,	Khan	and	Lee.	(2021)	employed	
the	Metaphone	algorithm	Odell	(1956)	to	generate	normalized	candidates	based	on	the	phonetic	similarity	of	words	in	English	text.
4.3 Pre-processing morphologically complex languages
The	analysis	of	social	media	text	becomes	more	challenging	when	dealing	with	languages	
that	have	a	high	degree	of	morphological	impact.	Languages	such	as	Finnish,	Turkish,	and	
Arabic	demonstrate	such	impact	through	their	widespread	utilization	of	inflection,	derivation,	and	compounding,	resulting	in	a	wide	range	of	word	forms	Al-Jarf	(2021).	The	presence	of	diverse	elements	increases	the	challenges	of	dealing	with	OOV	words,	making	text	
normalization	and	pre-processing	more	challenging.
4.3.1 Morphological complexity
Elaborate	word	creation	is	possible	in	languages	with	complicated	morphology.	Finnish	
nouns,	for	instance,	can	be	suffixed	to	contain	full	phrases	with	rich	inflectional	variation,	
distinguished	by	case,	number,	optional	possessive	suffixes,	and	clitics.	The	inflection	of	
Finnish	nouns	can	be	effectively	captured	by	summing	semantic	vectors	for	lexemes	and	
their	inflectional	features.	The	model	in	Nikolaev	et	al.	(2022)	conceptualizes	Finnish	
inflected	nouns	using	fasttext	embeddings,	and	it	demonstrates	that	incorporating	interactions	between	inflectional	features	improves	accuracy	from	76%	to	89%.	Suffixes	are	added	
during	derivation	in	agglutinating	languages	such	as	Turkish,	which	hold	unique	semantic	
material	relevant	to	computational	tasks.	By	adding	several	affixes	to	a	root	word	to	indicate	grammatical	relationships,	clustering	the	word	embedding	vectors	of	popular	Turkish	
1 3
89 Page 26 of 48

---


<!-- PAGE 27 -->

Textual variations in social media text processing applications:…
derivational	suffixes	could	examine	their	semantic	features.	In	the	work	by	the	authors	in	
Kim	(2024),	they	investigate	the	structure	of	these	suffixes	and	demonstrate	how	many	suffix	categories	may	be	consistently	represented	in	distributional	vector	space.	Many	words	
are	derived	from	triconsonantal	roots	in	the	Arabic	language's	root-based	morphology.	An	
analysis	of	186	Arabic	loanwords	with	derived	verbs	examined	the	patterns,	restrictions,	and	
formation	processes	of	these	verbs	Al-Jarf	(2024).	The	results	showed	that	although	some	
loan	verbs	are	not	changed,	41%	are	Arabized,	and	59%	are	newly	derived	from	borrowed	
nouns.	The	derived	verbs	mostly	follow	quadri-consonantal	paradigms	and	conform	to	nine	
Arabic patterns.
Such	linguistic	morphological	complexity	across	various	languages	makes	a	significant	
impact	with	a	large	amount	of	lexical	variance,	which	impairs	the	efficiency	of	conventional	
pre-processing	methods	and	makes	OOV	word	recognition	more	challenging.
4.3.2 Processing challenges
Tokenization	and	lemmatization	are	extremely	challenging	in	these	languages	due	to	the	
variety	of	inflectional	forms.	Automatic	morphological	processing	can	greatly	improve	
NLP	applications	for	such	low-resource	and	endangered	languages.	The	empirical	work	in	
Wiemerslage	et	al.	(2022)	demonstrates	its	impact,	which	is	increasingly	focused	on	languages	with	limited	resources.	It	is	now	ready	to	take	on	the	challenges	of	comprehending	
morphology	from	raw	text,	even	though	current	models	do	quite	well.
Although	subword-based	techniques	like	byte-pair	encoding	have	gained	popularity,	
classic	NLP	models	concentrated	on	words	as	atomic	tokens	Mielke	et	al.	(2021).	Nevertheless,	no	single	tokenization	technique	is	optimal	for	every	application,	underscoring	the	
significance	of	taking	several	tokenization	strategies	into	account.	The	work	in	Azaz	and	
Alfaifi	(2022)	investigates	the	lexical	preferences	and	assessments	of	knowledgeable	native	
speakers,	highlighting	the	significance	of	regional	variations.	Here,	with	a	case	study	of	
lexical	collocations	in	modern	standard	Arabic,	with	an	emphasis	on	regional	differences,	
the	general	stability	and	regularity	of	standard	Arabic's	lexicon	are	demonstrated	by	an	
acceptability judgment test.
4.3.3 Pre-processing approaches
Advanced	techniques	have	been	developed	by	researchers	to	address	the	challenges	posed	
by	text	variations,	which	are	significantly	influenced	by	the	morphological	complexity	of	
various	languages.	For	the	modern	standard	Arabic	language,	the	rule-based	pre-processing	strategy	in	Alkhairy	et	al.	(2023)	achieves	high	accuracy	and	coverage	in	pronunciation,	root	extraction,	word	generation,	and	discretization,	outperforming	existing	systems.	
It	works	in	both	forward	and	backward	directions	for	applications	like	automatic	speech	
recognition.	It	also	ensures	proper	ordering	of	grammar	and	phonology	rules.	The	work	
in	Aye	and	Soe	(2024)	assesses	transformer	and	RNN	models	and	is	optimized	with	subwording	on	the	Myanmar-English	WAT2019	corpus	in	the	pre-processing	stage.	The	results	
show	that	selecting	a	subword	model	is	crucial	for	translation	performance,	with	an	optimized	Transformer	model	that	uses	32k	Byte	Pair	Encoding	(BPE)	significantly	improving	
bilingual	evaluation	scores.	The	upcoming	section	5	analyzes	the	impact	of	pre-processing	
approaches	in	various	social	media	applications.
1 3
Page 27 of 48 89

---


<!-- PAGE 28 -->

J. Khan et al.
The	effectiveness	of	these	pre-processing	methods	varies	with	the	application	and	target	
languages.	Therefore,	it	is	necessary	to	empirically	test	their	effectiveness	before	adopting	
them.	These	methods	may	be	applied	individually	or	in	combination	to	enhance	the	performance	of	the	target	NLP	application	Naseem	et	al.	(2021).	The	individual	impact	of	some	of	
the	pre-processing	methods,	as	reported	in	the	literature,	is	provided	in	Table	3.
5 Pre-processing in social media applications
In	this	section,	we	discuss	and	analyze	the	implications	of	pre-processing	in	different	applications	of	social	media	text	processing.	We	note	that	a	few	representative	applications	where	
pre-processing	can	improve	or	badly	affect	the	performances	of	NLP	models	are	chosen	to	
demonstrate	that	the	challenges	and	requirements	of	the	applications	must	be	considered	in	
the	selection	of	pre-processing	techniques.
5.1 Sentiment analysis
Sentiment	analysis	is	one	of	the	key	social	media	applications	where	text	pre-processing	is	
considered	an	essential	component	of	the	methodology.	The	literature	reports	the	efficacy	
of	different	text	pre-processing	techniques	in	further	enhancing	the	performance	of	sentiment	analysis	and	opinion-mining	algorithms	Pota	et	al.	(2021);	Duong	and	Nguyen-Thi	
(2021);	Bakar	et	al.	(2019).	Besides	the	traditional	pre-processing	methods,	several	interesting	methods	have	been	proposed	for	handling	textual	variations,	standardization,	reduction	
of	vocabulary	space,	and	minimization	of	randomness	in	social	media	text.	For	instance,	
Balahur 2013	proposed	a	rule-based	method	for	Twitter	text	normalization	to	enhance	the	
performance	of	a	sentiment	classification	model.	Similarly,	Sharma	et	al.	(2015)	proposed	
a	text	normalization	method	for	multilingual	text	data	from	Twitter.	They	investigated	the	
impact	of	text	normalization	on	opinion	mining	from	code-mixed	Hindi-English	tweets.	On	
the	other	hand,	Arora	and	Kansal	(2019)	proposed	a	character-level	embedding	method	with	
deep	CNN	for	Twitter	text	normalization	before	sentiment	analysis.	Table	4	shows	the	effectiveness	of	normalization	on	sentiment	analysis	tasks	reported	by	different	existing	studies.
The	existing	pre-processing	approaches	mitigate/reduce	the	chances	of	information	loss	
and	also	overcome	domain	dependency	problems;	however,	these	approaches	still	have	
several	limitations.	For	instance,	these	approaches	mostly	do	not	consider	the	context	of	
the	intentional	OOV	words	while	substituting	them	with	their	nearest	replacements.	It	is	
also	important	to	keep	in	mind	that	sometimes	the	OOV	words	may	play	a	vital	role	in	
expressing	the	sentiments	and	emotions	of	social	media	users.	For	instance,	as	discussed	
earlier,	enlarged	words,	which	are	generated	by	repeating	certain	characters	in	a	word,	
could	be	useful	in	expressing	sentiments	and	emotions.	However,	these	repeated	characters	
are	sometimes	removed	to	recover	valid	words	during	text	normalization/pre-processing,	
which	may	result	in	the	loss	of	meaningful	information	in	sentiment	analysis.	Similarly,	
sometimes,	emojis/emotions	are	transformed	into	a	word/phrase	expressing	the	same	information	during	text	normalization.	These	emojis/emotions	could	be	completely	removed	in	
other	applications,	however,	in	sentiment	analysis,	they	convey	meaningful	information	and	
must	be	retained.	Moreover,	most	of	the	existing	techniques	normalize	isolated	word	prob1 3
89 Page 28 of 48

---


<!-- PAGE 29 -->

Textual variations in social media text processing applications:…
Table 3	Performance	of	individual	text	Pre-processing	methods
Technique	(Model,	Dataset) Type Glazkova	
(2023)	(BERT,	
heval)
Glazkova	
(2023)	(BERT,	
hsoc)
Glazkova	
(2023)	(BERT,	
hb_off)
Naseem	et	al.	
(2021)	(BiLSTM,	Davidson	et	al.	(2017))
Husain and 
Uzuner	
(2022)	(AraBERT,	L-HSAB)
Baseline 70.14 89.72 96.63 61.3 81.3
Lowercasing 68.0 83.89 96.35 59.9 -
Lemmatization Text	Standardization 70.26 90.34 96.64 65.0 -
Stemming 69.34 90.16 96.66 - -
Treatment	for	Numbers 70.88 90.0 96.68 60.9 80.2
Remove	Special	Character 70.71 90.14 96.53 62.2 -
Remove/	replace	URLs 71.01 89.81 96.68 68.6 -
Removing	Mentions Handling	of	noisy	text 70.96 89.8 96.85 68.6 80.6
Removing	Hashtags 70.69 89.94 96.69 68.6 80.9
Removing	Stopwords 68.92 90.12 96.59 67.4 -
Emoji/Emoticons	Decoding Emoticons Decoding 71.34 90.27 96.75 68.4 82.5
Spell Correction 70.31 89.63 96.62 67.6 -
Removing	repetition 70.9 89.94 96.65 68.8 -
Expansion	of	Contractions 70.40 89.70 96.67 64.4 -
Expanding	Abbreviations Text	Normalization 70.96 89.85 96.69 66.9 -
Slangs	Identification - - - 66.9 82.0
Dialects	Normalization - - - - 82.3
1 3
Page 29 of 48 89

---


<!-- PAGE 30 -->

J. Khan et al.
lems.	However,	in	informal	conversation,	dialectal	usage	and	word	deletion	are	widespread,	
which	can	only	be	handled	by	sentence-level	normalization.
5.2 Text normalization as defense against adversarial attacks
The	literature	also	reports	the	effectiveness	of	pre-processing	in	defense	against	adversarial	
attacks	on	text	and	speech	processing	applications	Alsmadi	et	al.	(2022);	Joshi	et	al.	(2021).	
In	text	processing,	adversarial	attacks	aim	at	fooling	the	target	models	by	making	certain	
changes	in	the	input	samples	at	the	word	or	character	level.	As	discussed	earlier,	social	
media	text	is	not	only	subject	to	textual	variations,	but	the	nature	of	social	media	text	processing	applications	also	makes	the	NLP	model	more	vulnerable	to	such	adversarial	attacks	
Alsmadi	et	al.	(2022).	Different	techniques	are	utilized	in	pre-processing	to	transform	the	
noisy	and	non-standard	text	into	their	standard	lexical	representation.	This	transformation	
can	help	in	avoiding	or	reducing	the	impact	of	adversarial	perturbations	that	may	be	present	in	the	input	text	Alsmadi	et	al.	(2022).	The	literature	reports	several	interesting	defense	
mechanisms	against	adversarial	attacks	relying	on	pre-processing	techniques.	For	instance,	
Moh	et	al.	(2020)	utilized	text	pre-processing-based	defense	techniques.	The	proposed	
methods	are	able	to	guard	against	adversarial	attacks	based	on	white	space,	typos,	benign	
word	insertion,	and	character	boundary	appending	attacks.
Text	normalization	is	the	most	common	pre-processing	method	for	defense	against	
textual	attacks.	Text	normalization	involves	standardization	of	the	input	text	and	includes	
tasks,	such	as	data	cleaning,	tokenization,	OOV	word	correction,	and	textual	variation	handling.	These	techniques	normalize	and	clean	noisy	text	and	bring	the	OOV	words,	which	
are	resulted	by	adversarial	perturbation,	to	their	standard	lexical	counterparts	Khan	and	Lee	
(2020);	Lertpiya	et	al.	(2020).	In	the	literature,	spell-checking,	which	is	one	of	the	key	tasks	
in	text	pre-processing,	has	been	widely	explored	in	defense	against	character-level	adversarial	attacks	Pruthi	et	al.	(2019);	Li	et	al.	(2018).	In	social	media	platforms,	malicious	users	
tend	to	use	new	ways	of	altering	text	for	different	purposes.	Normalization	algorithms	must	
handle	a	wide	range	of	OOV	words	by	sensing	the	error	patterns,	identifying	the	error	types,	
and	activating	the	appropriate	correction	methods	to	cope	with	these	innovative	adversarial	
perturbations.	Thanks	to	the	recent	development	in	text	pre-processing,	the	scope	of	text	
normalization	has	been	widely	explored	to	cope	with	different	OOV	words	resulting	from	
intentional	and	unintentional	textual	variations.	These	methods	aim	at	substituting	OOV	
words	with	their	valid	replacements	Khan	and	Lee	(2021).	Zhou	et	al.	(2019)	provided	a	
novel	framework	to	identify	and	replace	the	adversarial	tokens	with	their	correct	substitutes.	Keller	et	al.	(2021)	proposed	a	BERT-Defense	against	low-level	adversarial	attack.	
The	proposed	model	combines	the	substitutions	of	context-independent	word-level	words	
with	context-dependent	word	substitutions	obtained	from	the	BERT	model	to	normalize	the	
adversarial	text	before	classification.	Khan	et	al.	(2023)	utilized	a	stacked	ensemble-based	
text	normalization	(StackEnsembleNorm)	as	a	defense	against	popular	adversarial	attacks,	
including	DeepWordBug	Gao	et	al.	(2018),	TextBugger	Li	et	al.	(2018),	and	social	mediainspired	character-level	adversarial	attacks	(SocMediTextAttacks)	Khan	et	al.	(2023).	
Table	5	provides	an	insight	into	text	normalization	as	a	defense	against	adversarial	attacks	
in	English	text	classification.
1 3
89 Page 30 of 48

---


<!-- PAGE 31 -->

Textual variations in social media text processing applications:…
5.3 Hate speech detection and cyber bullying
Cyberbullying	and	hate	speech	detection	are	other	key	social	media	text	applications	where	
pre-processing	techniques	are	vital	in	performance	improvement.	To	avoid	cyberbullying	
techniques	and	hate	speech	detectors,	social	media	users	tend	to	use	intelligently	generated	
OOV	words	instead	of	actual	hate	speech.	NLP	models	without	proper	pre-processing	(i.e.,	
text	normalization)	cannot	detect	cyberbullying	and	hate	speech	conveyed	via	the	OOV	
words.	To	cope	with	such	OOV	words	in	these	applications,	text	normalization	techniques	
are	used	to	recover	actual	words	from	the	OOV	words	before	feeding	them	into	a	classifier.	
It	generally	involves	transforming	the	raw	text	data	into	a	format	that	machine	learning	
algorithms	can	efficiently	process	Pericherla	and	Ilavarasan	(2021).
The	literature	reports	several	interesting	cyberbullying	and	hate	speech	detection	frameworks	relying	on	pre-processing	to	enhance	performance	further.	For	instance,	Sanoussi	et	
al.	(2022)	employed	several	traditional	pre-processing	techniques,	including	data	cleaning,	
stop-words	removal,	stemming,	lemmatization,	and	tokenization	before	feature	extraction	
and	feeding	it	into	a	hate-speech	detection	classifier.	On	the	other	hand,	Amanpreet	et	al.	
Singh	and	Kaur	(2019)	compared	various	traditional	pre-processing	and	ML	techniques	
Table 4	Effectiveness	of	pre-processing	on	the	performance	of	sentiment	analysis
Reference Dataset Model Without	Pre-proc With	Pre-Proc Lang 
uageF-Score Accuracy F-Score Accuracy
Duong and 
Nguyen-Thi	
(2021)
Product	Reviews	Duong	
and	Nguyen-Thi	
(2021)
SVM 82.9 - 85.6 - Veitnam-
ese
Balahur	(2013) TweetEm	Mohammad	(2012)
BERT 32.71 49.00 41.48 51.85 English
Pota et al. 
(2021)
SemEval2017	
Rosenthal	et	al.	
(2019)
BERT 67.70 65.1 68.10 67.7 English
Pota et al. 
(2021)
SENTIPOLC	
2016 Barbieri et 
al.	(2016)
BERT 72.23 - 75.06 - Italian
Khan and Lee 
(2021)
GOP	Debate	
Eight	(2019)
LSTM 53.59 64.04 71.31 76.59 English
Khan and Lee 
(2021)
GOP	Debate	
Eight	(2019)
BERT 59.28 68.94 76.34 80.87 English
Sharma et al. 
(2015)
FIRE	2013/2014	
Choudhury et al. 
(2014)
Model - 81.00 - 85.00 Hinglish
Arora and 
Kansal	(2019)
SemEval	2017 CNN 90.00 96.20 92.00 98.81 English
Grancharova	
and Jangefalk 
(2018)
Tel2	Customer	
feedback
Naïve	
Bayes
- 74.6 - 78.4 Swedish
Grancharova	
and Jangefalk 
(2018)
Tel2	Customer	
feedback
SVM - 74.0 - 75.4 Swedish
Toska	(2020) Twitter	Data	
Kalamatianos et 
al.	(2015)
- 80.9 - 95.4 Greek
1 3
Page 31 of 48 89

---


<!-- PAGE 32 -->

J. Khan et al.
Reference Attack Model Dataset Pre-Proc	(Defense) Attack Success-rate
No	
Defense
With	
Defense
Pruthi et 
al.	(2019)
Pruthi BERT MRPC	
Dolan 
and 
Brockett 
(2005)
ScRNN 65.16 7.80
Pruthi et 
al.	(2019)
Pruthi BiLSTM MRPC	
Dolan 
and 
Brockett 
(2005)
ScRNN 55.77 31.05
Li et al. 
(2018)
TextBugger Google	
NLP
IMDB Spellchecker 70.1 22.2
Li et al. 
(2018)
TextBugger Google	
NLP
MR Spellchecker 86.9 38.2
Li et al. 
(2018)
DeepWordBug Google	
NLP
IMDB Spellchecker 43.6 15.9
Li et al. 
(2018)
DeepWordBug Google	
NLP
MR Spellchecker 67.3 26.9
Li et al. 
(2018)
TextBugger MS	Azure IMDB Spellchecker 100 32.2
Li et al. 
(2018)
TextBugger MS	Azure MR Spellchecker 96.8 30.8
Li et al. 
(2018)
DeepWordBug MS	Azure IMDB Spellchecker 56.3 15.9
Li et al. 
(2018)
DeepWordBug MS	Azure MR Spellchecker 71.3 13.8
Zhou et al. 
(2019)
Char/Word	attack BERT SST-2 Spellchecker 31.52 18.47
Zhou et al. 
(2019)
Char/Word	attack BERT IMDB Spellchecker 10.58 7.44
Zhou et al. 
(2019)
Char/Word	attack BERT SST-2 DISP 31.52 13.07
Zhou et al. 
(2019)
Char/Word	attack BERT IMDB DISP 10.58 1.06
Zhou et al. 
(2019)
Char/Word	attack BERT SST-2 DISP+Spellchecker 31.52 7.60
Zhou et al. 
(2019)
Char/Word	attack BERT IMDB DISP+Spellchecker 10.58 4.72
Khan et al. 
(2023)
DeepWordBug BERT MR StackEnsembleNorm 77.17 8.93
Khan et al. 
(2023)
DeepWordBug RoBERTa MR StackEnsembleNorm 80.13 5.31
Khan et al. 
(2023)
DeepWordBug BERT AgNews StackEnsembleNorm 62.34 7.22
Khan et al. 
(2023)
DeepWordBug RoBERTa AgNews StackEnsembleNorm 57.29 3.78
Khan et al. 
(2023)
TextBugger BERT MR StackEnsembleNorm 62.25 10.69
Khan et al. 
(2023)
TextBugger RoBERTa MR StackEnsembleNorm 66.91 8.22
Table 5	Performance	of	text	normalization	as	defense	against	adversarial	attacks
1 3
89 Page 32 of 48

---


<!-- PAGE 33 -->

Textual variations in social media text processing applications:…
for	cyberbullying	detection.	The	effect	of	traditional	pre-processing	and	feature	extraction	
algorithms	on	hate	speech	and	cyberbullying	detection	has	been	reported	in	several	works	
Kshirsagar	et	al.	(2018);	Febriana	and	Budiarto	(2019);	Hettiarachchi	et	al.	(2020);	Gautam	
and	Bansal	(2022);	Aurpa	et	al.	(2022).
Despite	the	proven	performances,	traditional	pre-processing	techniques	have	several	
limitations.	For	instance,	the	traditional	pre-processing	methods	are	insufficient	to	detect	
different	types	of	OOV	words	generated	through	intentional	textual	variations.	Several	
interesting	text	normalization	techniques	have	been	proposed	in	the	literature	to	overcome	
these	limitations,	which	can	detect	and	replace	the	OOV	words	with	their	corresponding	
correct/standard	words.	For	instance,	Naseem	et	al.	(2021)	provide	an	experimental	survey	
to	report	the	effectiveness	of	the	various	text	pre-processing/normalization	methods	on	ML	
and	DL	models.	They	employed	different	combinations	of	these	pre-processing	methods	
on	different	hate	speech	datasets.	Khan	and	Lee	(2021)	proposed	several	context-aware	
pre-processing/text	normalization	methods	for	handling	OOV	words	in	a	social	media	text.	
Abdel	Hamid	et	al.	(2022)	also	utilized	specialized	normalization	methods	for	coping	with	
OOV	words	in	hate	speech	detection.	These	methods	include	elongation	removal	and	dialectal	normalization.	Husain	and	Uzuner	(2022)	investigated	the	effect	of	pre-processing	on	
hate	speech	and	offensive	language	detection	in	Arabic	text.	They	examined	the	effects	of	
different	pre-processing	methods	on	traditional	ML	and	advanced	DL	models.	Mansur	et	
al.	(2024)	presented	a	new	normalization	method	by	integrating	rule-based	pattern	identification	and	Sym-Spell	correction	to	improve	the	performance	of	the	hate	speech	detection	
model	in	social	media	data.	Table	6	shows	the	effectiveness	of	the	pre-processing	on	the	
performance	of	hate	speech	detection	reported	by	some	of	these	works.
5.4 Author attribution and style detection
Stylometry,	which	involves	multiple	sub-tasks	related	to	the	author's	writing	style,	is	another	
interesting	application	of	text	analysis.	In	stylometry,	generally,	different	aspects	of	text	
written	by	a	single	author	or	multiple	authors	are	explored	for	different	tasks,	such	as	authorship	attribution,	verification,	and	authorship	profiling,	etc.,	Neal	et	al.	(2017);	Stamatatos	
(2009).	Interestingly,	in	contrast	to	the	earlier	discussed	applications,	pre-processing	in	styReference Attack Model Dataset Pre-Proc	(Defense) Attack Success-rate
No	
Defense
With	
Defense
Khan et al. 
(2023)
TextBugger BERT AgNews StackEnsembleNorm 52.99 10.94
Khan et al. 
(2023)
TextBugger RoBERTa AgNews StackEnsembleNorm 51.94 7.87
Khan et al. 
(2023)
SocMediTextAttacks
BERT MR StackEnsembleNorm 92.09 37.32
Khan et al. 
(2023)
SocMediTextAttacks
RoBERTa MR StackEnsembleNorm 95.56 23.18
Khan et al. 
(2023)
SocMediTextAttacks
BERT AgNews StackEnsembleNorm 85.42 20.19
Khan et al. 
(2023)
SocMediTextAttacks
RoBERTa AgNews StackEnsembleNorm 84.58 18.79
Table 5 (continued) 
1 3
Page 33 of 48 89

---


<!-- PAGE 34 -->

J. Khan et al.
lometry	can	adversely	impact	the	algorithms'	performances.	In	one	of	the	recent	works	on	
authorship	classification,	Zamir	et	al.	(2023)	reported	an	adverse	impact	of	pre-processing	
on	the	performance	of	NLP	models.	The	authors	employed	several	traditional	pre-processing	techniques	that	mainly	included	removing	special	characters,	such	as	usernames,	URLs,	
emojis,	and	stop	words.	Moreover,	user-defined	shortcuts	and	other	abbreviations	were	
expanded	to	obtain	the	corresponding	actual	words.	The	authors	concluded	that	these	special	characters	can	be	vital	in	differentiating	and	recognizing	an	author's	style.	For	instance,	
one	author	may	use	certain	special	characters	or	may	frequently	use	stop	words	and	abbreviations	compared	to	others.	Similarly,	Zamir	et	al.	(2024)	in	their	extended	work	reported	
Table 6	Effectiveness	of	Pre-processing	on	the	Performance	of	Hate	Speech	Detection
Reference Dataset Model Without	Pre-proc With	Pre-Proc LanguageF-Score Accuracy F-Score Accuracy
Mansur	et	
al.	(2024)
Hate Speech 
Identification	
Waseem	and	
Hovy	(2016)
BiLSTM 46.0 - 88.0 - English
Naseem	et	
al.	(2021)
Hate Speech 
Identification	
Waseem	and	
Hovy	(2016)
CNN 53.5 - 56.3 - English
Naseem	et	
al.	(2021)
Hate Speech 
Identification	
Waseem	and	
Hovy	(2016)
LSTM 52.9 - 57.7 - English
Naseem	et	
al.	(2021)
Hate Speech 
Identification	
Waseem	and	
Hovy	(2016)
BiLSTM 53.1 - 58.6 - English
Khan and 
Lee	(2021)
Cyberbullying Detection 
Elsafoury 
(2020)
LSTM 77.40 77.35 81.83 82.04 English
Khan and 
Lee	(2021)
Cyberbullying Detection 
Elsafoury 
(2020)
BERT 87.80 86.91 92.03 91.36 English
Sosamphan 
et	al.	(2016)
Hate Speech 
Identification	
Waseem	and	
Hovy	(2016)
BiLSTM 46.0 - 81 - English
Husain and 
Uzuner	
(2022)
L-HSAB AraBERT 72.0 81.0 73.0 82.0 Arabic
Husain and 
Uzuner	
(2022)
L-HSAB Arabic-BERT 68.0 79.0 70.0 80.0 Arabic
Husain and 
Uzuner	
(2022)
OSACT AraBERT 77.0 96.0 77.0 97.0 Arabic
Husain and 
Uzuner	
(2022)
OSACT Arabic-BERT 82.0 97.0 83.0 97.0 Arabic
1 3
89 Page 34 of 48

---


<!-- PAGE 35 -->

Textual variations in social media text processing applications:…
the	performance	of	the	state-of-the-art	NLP	models	in	single/multi-authored	document	classification	(S/MADI),	style	change	detection	(SCD),	and	author	recognition	(AuthRec)	tasks	
on	pre-processed	and	raw	data.	The	effects	of	text	pre-processing	on	these	tasks,	as	reported	
by	Zamir	et	al.	(2023,	2024)	are	shown	in	Table	7.
Table	8	presents	a	comprehensive	list	of	text	pre-processing	techniques	used	in	literature	
meant	for	the	social	media	text	data	analysis	in	NLP.	This	table	provides	an	overview	of	
these	techniques	and	can	help	researchers	and	practitioners	choose	the	most	appropriate	preprocessing	strategies	for	their	specific	social	media	NLP	tasks.
6 Challenges, open issues, recommendations, and lessons learned
6.1 Challenges, open issues, and recommendations
This	section	provides	an	overview	of	some	of	the	key	challenges,	open	research	issues,	and	
recommendations	for	pre-processing	social	media	text.
 ● Being	an	informal	source	of	communication,	social	media	text	is	subject	to	several	intentional	and	unintentional	variations.	For	instance,	malicious	netizens	on	social	media	
tend	to	morph	or	replace	objectionable	content,	such	as	toxic	words,	with	different	OOV	
words	(i.e.,	variants	of	the	actual	words)	to	fool	toxic/hate	speech	detection	models	
Alsmadi	et	al.	(2022).	Such	a	random	nature	of	data	generated	by	online	users	is	more	
challenging	to	clean	and	process.	Moreover,	these	malicious	users	explore	novel	and	
intelligent	ways	of	fooling	NLP	models.	The	traditional	NLP	pre-processing	techniques	
are	not	enough	to	deal	with	such	variations	in	the	text	Khan	and	Lee	(2021).
 ● In	a	natural	language,	the	meaning	of	a	word	largely	depends	on	the	context	in	which	
it	is	used.	This	also	holds	in	the	case	of	OOV	words,	and	the	pre-processing	techniques	
may	not	accurately	capture	their	meaning	(i.e.,	replace	it	with	the	correct	word)	without	
considering	the	context.	Moreover,	multi-word	expressions,	such	as	idioms	and	collocations,	also	pose	challenges	to	text	processing	models.	These	expressions	cannot	
be	easily	parsed	through	traditional	pre-processing	techniques	and	require	specialized	
approaches	to	be	handled	effectively.
 ● Another	key	challenge	to	social	media	text	pre-processing	techniques	is	dealing	with	
multi-lingual	text	in	social	media	platforms.	To	effectively	process	social	media	text,	the	
text	pre-processing	techniques	need	to	be	adapted	to	different	languages	and	domains.
 ● Text	pre-processing	can	be	computationally	expensive,	especially	for	large	datasets.	
Table 7	Effects	of	pre-processing	in	author	attribution	and	style	detection
Method/Model Task	1 Task	2 Task	3
Raw	Data Pre-Proc Data Raw	Data Pre-Proc Data Raw	Data Pre-Proc Data
BERT 79.46 79.0 74.23 70.52 52.44 53.09
Albert 79.19 80.0 77.19 72.22 49.40 49.98
Distillbert 75.96 76.0 72.45 68.80 52.13 52.61
Roberta-base 80.0 83.44 76.18 71.43 47.0 48.0
XLM-Roberta 83.0 79.0 76.23 71.25 51.59 52.81
Simple Fusion 82.72 77.0 78.22 73.68 51.64 50.87
PSO-based	Fusion 84.86 79.0 77.53 71.17 54.04 55.35
1 3
Page 35 of 48 89

---


<!-- PAGE 36 -->

J. Khan et al.
Reference Pre-processing	Type Application Overview/Summary
	Baldwin	et	
al.	(2013)
language	identification,	
lexical	normalization,	POS	
tagging
Noise	analysis	of	
social	media	text
Built a corpus from multiple social 
media sources and conducted an empirical	noise	analysis	in	text	from	various	
perspectives	including	language	distribution,	lexical	analysis,	grammaticality,	
corpus	similarity,	and	perplexity.	This	
work	suggests	that	the	mentioned	preprocessing can help reduce noise
 Saloot et al. 
(2014)
Spell	correction,	phonetic	
replacement
Noisy	text	
normalization
Proposed	a	two-phase	text	normalization	method	to	replace	the	OOV	words	
in	the	informal	social	media	text	with	
their appropriate candidates
 Desai and 
Narvekar	
(2015)
Replace	(enlargements,	
numbers,	slangs),	spell	
correction
Social	media	text	
normalization
Present a pre-processing method to 
normalize	social	media	text
	Baldwin	and	
Li	(2015)
Insertion,	replacement,	and	
removal	of	punctuations,	
contractions,	slangs,	typos,	
special tokens
Effect	of	text	
normalization	in	
social media
Built	a	taxonomy	of	text	normalization	
methods and empirically presented the 
effects	of	text	normalization	on	three	
applications
 Khan et al. 
(2016)
POS	tagging,	remove	(stopwords),	stemming,	chunking,	spelling	correction
Sentiment polarity 
detection
Utilized	SentiWordNet	to	develop	a	sentiment	lexicon,	i.e.,	SentiMI	based	on	
the mutual information estimated from 
the terms arranged in synonym groups
 Symeonidis 
et	al.	(2018)
Lemmatization,	stemming,	
lowercasing,	removing	
(Unicode	strings,	punctuation,	numbers,	stopwords),	
expanding	contraction,	
replacing	(URLs,	mentions,	
abbreviations,	slangs,	negation),	POS	tagging
Twitter	sentiment	
analysis
Conducted	a	comparative	analysis	of	
several	pre-processing	techniques	for	
sentiment	analysis	in	Twitter	using	different machine learning methods
	Tessore	et	
al.	(2019)
Tokenization,	remove	
(URLs,	special	characters),	
expanding	contractions,	
spell	correction,	replace	
(abbreviations,	slangs,	
enlargements,	emojis),	
uppercasing
Spanish social 
media	text	
processing
Measures	the	effectiveness	of	cleaning	
and	repairing	tasks	on	social	media	text	
data	to	reduce	noise	and	improve	the	
data's	quality	for	text	analysis	and	emotion	classification	on	the	hashtags	and	
usernames processing
 Kumar and 
Garg	(2019)
Tokenization,	POS	tagging,	
remove	(URLs,	special	
characters,	stopwords,	
mentions,	placeholders),	
replace	expansions,	spell	
correction
Sarcasm detection 
in memes from 
social media
A pipeline for sarcasm detection in 
typo-graphic memes on social media is 
presented.	The	preprocessing	is	reported	
to enhance the performance of the 
proposed method
	MaslejKrešňáková	
et	al.	(2020)
Tokenization,	lowercasing,	remove	(punctuation,	
stopwords)
Toxic	comments	
classification
Evaluate	the	performance	of	DL	models	
including	RNN,	CNN,	BERT,	and	ensembled	methods	in	combination	with	
different	text	representation	and	preprocessing	methods,	on	a	multi-label	
toxic	comments	classification
 Yun et al. 
(2020)
Tokenization,	stemming,	
lowercasing,	remove	
(numbers,	punctuations,	
stopwords),	sorting
Topic	classification	for	advertising	
on social media
Semantic	topic	tagging	to	analyze	
topics	of	conversation	in	social	media	
posts and performed human-coded 
topic	analysis	over	Twitter	feeds	with	
recommendations
Table 8	Summary	of	social	media-specific	text	pre-processing	strategies	in	NLP
1 3
89 Page 36 of 48

---


<!-- PAGE 37 -->

Textual variations in social media text processing applications:…
Reference Pre-processing	Type Application Overview/Summary
 Khan and 
Lee	(2020)
Tokenization,	lemmatization,	lowercasing,	remove	
(URLs,	special	characters,	
stopwords,	punctuations),	
spell correction
Enhancement of 
social media sentiment analysis
Present a pre-processing method to 
enhance social media sentiment analysis 
using ensemble machine learning
 Doshi et al. 
(2020)
Tokenization,	replace	(abbreviations,	enlargements,	
homo-phonic	words),	
expand	contractions
Social	media	text	
normalization
Phonetic and string similarity based 
normalization	methods	using	language	
modeling
	Tao	and	
Zhou	(2020)
Tokenization,	POS	tagging,	
chunking,	lemmatization,	
remove	(stopwords,	URLs,	
numbers,	punctuations)
Aspect learning 
in online product 
reviews
A	deep	learning	approach	with	weakly	
supervised	WordNet-guide	is	developed	
for	aspect	term	extraction	in	online	
reviews,	using	a	set	of	labeled	data	and	
observed	the	semantic	information	from	
WordNet
	Maltseva	et	
al.	(2020)
lowercasing,	remove	
(URLs,	numbers,	punctuations),	padding,	spell	correction,	lemmatization
Social media sentimental analysis
Evaluates	the	sentiment	of	statements	in	
a	social	media	context,	to	assess	users'	
attitudes	towards	freelance	work	by	
classifying	messages	as	"core",	"periphery",	and	"non-relevant"
	Naseem	et	
al.	(2021)
Lemmatization,	remove	
(special	characters,	tags,	
links,	numbers,	stopwords,	
punctuation),	spell	correction,	lowercasing,	expand	
contraction,	replace	(abbreviations,	slangs,	enlargements,	emojis)
hate speech detection	on	Twitter
An	experimental	survey	to	analyze	the	
impact	of	twelve	selected	pre-processing	operations	on	three	Twitter	datasets	
that are labeled for hate speech detection.	Additionally,	this	study	proposed	
a	systematic	method	to	pre-process	text	
without	information	loss
	Hegazi	et	al.	
(2021)
Tokenization,	remove	
(URLs,	special	characters,	
numbers),	spell	correction
Topic	classification,	and	sentiment	
analysis
Four	stage	text	pre-processing,	yielding	
a	useful	and	full-featured	dataset,	of	
Arabic	text	from	social	media,	with	
information	on	topic	classification	and	
sentiment analysis
 Kumar and 
Garg	(2021)
POS	tagging,	lemmatization,	noise	removal
Opinion	mining	
from	tweets
Implements	a	two-step	preprocessing	
for	textual	data	generated	from	Twitter	
API	using	a	NoSQL,	document-based	
database	for	raw	data	accumulation	and	
performs suitable opinion mining
 Chen et al. 
(2021)
POS	tagging,	remove	
(URLs,	special	characters,	
stopwords),	spell	checking,	
expanding	contractions
Early rumor detection	on	Twitter
An early rumor detection model is 
developed	based	on	account	filtering,	
BiGRU	for	context	relationship,	and	RL	
algorithm,	which	improves	accuracy	
and maintains the speed of detection
 Cagnoni et 
al.	(2021)
POS	tagging,	stemming Sentimental 
analysis and 
enhancement
A	feature	weighting	technique	improve	
the	sentence-level	sentiment	analysis	by	
increasing	the	relevance	of	the	features	
in	lexical	patterns
Table 8 (continued) 
1 3
Page 37 of 48 89

---


<!-- PAGE 38 -->

J. Khan et al.
Sometimes,	it	becomes	challenging	to	keep	a	balance	between	precision	and	efficiency	
when	developing	and	applying	pre-processing	techniques.
 ● Social	media	text	has	been	utilized	in	a	diversified	set	of	applications,	and	each	application	has	its	challenges	and	requirements.	For	instance,	certain	pre-processing	techniques	
could	be	useful	in	certain	applications	while	they	may	hurt	other	applications,	as	discussed	earlier.	Thus,	identifying	appropriate	pre-processing	techniques	based	on	the	
target	applications	(performance	improvement/degradation)	and	data	characteristics	(to	
avoid	overhead)	is	necessary.
 ● Natural	languages	are	highly	diverse,	and	different	languages	have	their	unique	characteristics	and	challenges.	These	languages	vary	in	terms	of	syntax,	morphology	(i.e.,	
the	way	words	are	formed),	and	semantics.	Pre-processing	techniques	that	work	well	
for	one	language	may	not	be	effective	for	another	language	Gasparetto	et	al.	(2022).	
For	instance,	stemming,	which	is	a	preprocessing	technique	involving	the	reduction	of	a	
Reference Pre-processing	Type Application Overview/Summary
 Khan and 
Lee	(2021)
Tokenization,	lemmatization,	lowercasing,	remove	
(URLs,	special	characters,	
stopwords,	punctuations),	
spell	correction,	replace	
(enlargements,	abbreviations,	homo-phonic	(sub)
words),	expand	contractions,	insert	(missing	
characters/words)
Enhancement of 
social	media	text	
classification
Present	a	context-aware	pre-processing	
method	to	the	textual	variations	on	
social	media	for	enhanced	text	analysis	
of	data	from	various	data	sources
 Elfaik and 
Nfaoui	
(2022)
Remove	(URLs,	special	
characters,	Unicode	characters),	replace	(enlargements,	abbreviations,	
emojis),	padding
COVID-19	vaccine debate in 
social media
Sentiment	analysis	through	word	
embedding and machine learning 
techniques	on	social	media	data	to	analyze	the	public's	perceptions	towards	
vaccination
 Chen and 
Crooks 
(2022)
Remove	(URLs,	special	
characters,	Unicode	characters),	replace	(enlargements,	abbreviations,	
emojis),	padding
COVID-19	vaccine debate in 
social media
Sentiment	analysis	through	word	
embedding and machine learning 
techniques	on	social	media	data	to	analyze	the	public's	perceptions	towards	
vaccination
	Bai	(2023) Tokenization,	remove	(special	characters,	stopwords),	
lemmatization,	stemming
Psychological 
disorder analysis
A deep learning model for early 
recognition of mental illness using 
BERT	pre-trained	language	model	for	
sentence-level	feature	vector	representation,	results	in	improved	multiple	
classification	accuracy
 Kumar et al. 
(2023)
Tokenization,	remove	(special	characters,	stopwords),	
lemmatization,	stemming
Psychological 
disorder analysis
A deep learning model for early 
recognition of mental illness using 
BERT	pre-trained	language	model	for	
sentence-level	feature	vector	representation,	results	in	improved	multiple	
classification	accuracy
	Elzayady	et	
al.	(2023)
Stemming,	replace	
(enlargements,	emojis),	
remove	(URLs,	stopwords,	
special	characters,	punctuations,	empty	lines),	lemmatization,	stemming
hate speech 
detection in Arabic 
social media
A pipeline for automatic hate speech 
detection	in	Arabic	social	media	text.	
The	system	is	designed	to	integrate	
personality	trait	features	with	textual	
features for hate speech detection
Table 8 (continued) 
1 3
89 Page 38 of 48

---


<!-- PAGE 39 -->

Textual variations in social media text processing applications:…
word	to	its	root,	may	work	well	for	languages	with	simple	morphology,	such	as	English.	
However,	these	techniques	may	not	be	effective	in	languages	with	complex	morphology,	such	as	Turkish,	Arabic,	Hindi,	and	Urdu.	Similarly,	tokenization	may	be	simple	in	
English,	but	the	standard	tokenization	methods	may	not	be	very	effective	in	languages	
like	Chinese	and	Burmese,	which	do	not	use	space	in	the	text.	Developing	languagespecific	pre-processing	techniques	and	tools	is	crucial	to	improving	the	accuracy	of	NLP	
models	across	different	languages.
 ● Pre-processing	issues	with	domain-specific	and	low-resolution	languages	should	be	
thought	over.	Many	languages	lack	pre-trained	models	and	annotated	data,	making	preprocessing	more	challenging.	Customized	NLP	models	are	often	recommended	to	independently	enable	language-specific	text	handling.
 ● Tokenization	could	be	challenging	in	languages	with	complex	morphology,	such	as	
Arabic,	where	a	single	word	may	have	multiple	tokens	and	meanings	Attia	(2007).	For	
is	used	for	contract,	decade,	and	agreement.	Morphological	knowledge	of	the	language	must	be	used	in	tokenization	in	such	languages	
Attia	(2007).
 ● More	recently,	due	to	the	growing	concerns	over	the	misuse	of	technology,	the	literature	emphasizes	fairness	and	the	responsible	use	of	NLP	in	different	smart	cities	and	
societal	applications.	The	nature	of	these	applications	necessitates	assessing	the	ethical	
implications	of	NLP	algorithms	by	focusing	on	key	aspects	such	as	bias,	fairness,	and	
privacy.	For	the	responsible	use	of	NLP,	the	literature	mostly	focuses	on	data	collection	
and	the	processing/classification	algorithms	with	less	attention	to	the	pre-processing	
steps	Biswas	and	Rajan	(2021).	However,	bias	in	NLP	applications	could	be	introduced	
through	pre-processing	Biswas	and	Rajan	(2021).	Pre-processing	plays	a	double-edged	
sword	in	the	fairness	and	responsible	use	of	NLP	applications.	On	one	side,	a	vast	majority	of	the	existing	literature	reports	the	effectiveness	of	pre-processing	techniques	in	
mitigating	potential	bias	and	discrimination	in	different	applications	of	NLP	Calmon	
et	al.	(2017).	However,	several	existing	works	also	report	pre-processing	as	one	of	the	
potential	sources	of	bias	Dixon	et	al.	(2018);	Grgić-Hlača	et	al.	(2018).	Sometimes,	
pre-processing not only encodes bias in the data but may also result in missing the 
detection	of	bias	in	earlier	stages	in	the	frameworks	Biswas	and	Rajan	(2021).	Thus,	
pre-processing	techniques	must	be	carefully	selected	to	avoid	any	potential	biases	in	the	
dataset,	which	may	lead	to	biased	and	unfair	decisions.
6.2 Lessons learned
Some	key	lessons	learned	from	this	study	are	as	follows.
 ● Being	an	informal	source	of	communication	and	a	diversified	list	of	interesting	applications,	social	media	text	is	subject	to	intentional	and	unintentional	textual	variations.	
These	textual	variations	result	in	several	OOV	words,	making	effective	processing	of	
social	media	text	more	challenging.
 ● The	intentional	and	unintentional	textual	variations	in	social	media	text	may	be	easily	
identified	and	replaced	by	humans;	however,	NLP	models	cannot	cope	with	such	OOV	
words.
 ● These	OOV	words	social	media	users	generate	can	be	handled	through	pre-processing	
1 3
Page 39 of 48 89

---


<!-- PAGE 40 -->

J. Khan et al.
techniques.	However,	social	media	users	explore	novel	and	intelligent	text	alteration	
methods	for	different	purposes.	Thus,	the	conventional	pre-processing	methods	are	not	
enough	to	deal	with	it.
 ● There	are	several	factors	that	make	social	media	text	pre-processing	more	challenging	
compared	to	formal	sources	of	text.	Some	of	these	factors	include	the	informal,	noisy,	
and	unstructured	nature	of	social	media	text,	multi-lingual	text,	and	diversity	in	topics/
domains	covered	in	a	social	media	text.	Moreover,	different	social	media	text-processing	applications	have	different	challenges	and	requirements.
 ● To	cope	with	the	associated	challenges,	social	media	text	pre-processing	must	consider	
a	different	aspect	of	social	media	informal,	noisy,	and	unstructured	text.
7 Conclusions
In	this	paper,	we	analyzed	and	discussed	different	challenges	associated	with	social	media	
text	processing	and	how	they	can	be	overcome	through	proper	pre-processing.	Firstly,	we	
provided	a	detailed	overview	of	different	sources	of	intentional	and	unintentional	variations	
and	the	results	in	OOV	words	in	a	social	media	text.	We	also	provided	a	detailed	survey	
of	different	pre-processing	techniques,	including	both	traditional	and	application-specific	
methods	proposed	in	the	literature.	We	also	discussed	the	impact	of	pre-processing	techniques	on	different	social	media	text-processing	applications.	Finally,	we	discussed	the	key	
challenges	and	open	issues	with	current	pre-processing	techniques	and	made	recommendations	for	future	work.	In	the	current	work,	we	briefly	discussed	a	few	social	media	applications	without	going	deeper	into	these	specific	applications.	In	the	future,	we	will	explore	the	
impact	of	these	intentional	and	unintentional	OOV	words	in	specific	applications	in	more	
detail.
Acknowledgements	This	research	was	supported	by	the	MSIT	(Ministry	of	Science	and	ICT),	Korea,	
under	 the	 Artificial	 Intelligence	 Convergence	 Innovation	 Human	 Resources	 Development	 (IITP2024-RS2023-00255968)	grant	and	Grant	RS-2021-II212068	(Artificial	Intelligence	Innovation	Hub),	supervised	by	the	Institute	for	Information	&	Communications	Technology	Planning	&	Evaluation	(IITP),	and	also	
by	the	National	Research	Foundation	of	Korea(NRF)	grant	(No.	NRF2022R1A2C1007434).	The	publication	
fee	has	been	paid	by	the	BK21	FOUR	program	of	the	NRF	of	Korea,	funded	by	the	Ministry	of	Education	
(NRF5199991014091).
Author contributions	All	authors	contributed	equal	to	this	work.
Data availability	No	datasets	were	generated	or	analysed	during	the	current	study.
Declarations
Conflict of interest	The	authors	declare	no	competing	interests.
Open Access 		 This	 article	 is	 licensed	 under	 a	 Creative	 Commons	 Attribution-NonCommercialNoDerivatives	4.0	International	License,	which	permits	any	non-commercial	use,	sharing,	distribution	and	
reproduction	in	any	medium	or	format,	as	long	as	you	give	appropriate	credit	to	the	original	author(s)	and	the	
source,	provide	a	link	to	the	Creative	Commons	licence,	and	indicate	if	you	modified	the	licensed	material.	
You	do	not	have	permission	under	this	licence	to	share	adapted	material	derived	from	this	article	or	parts	of	it.	
The	images	or	other	third	party	material	in	this	article	are	included	in	the	article's	Creative	Commons	licence,	
unless	indicated	otherwise	in	a	credit	line	to	the	material.	If	material	is	not	included	in	the	article's	Creative	
1 3
89 Page 40 of 48

---


<!-- PAGE 41 -->

Textual variations in social media text processing applications:…
Commons	licence	and	your	intended	use	is	not	permitted	by	statutory	regulation	or	exceeds	the	permitted	use,	
you	will	need	to	obtain	permission	directly	from	the	copyright	holder.	To	view	a	copy	of	this	licence,	visit	
http://crea	tivecommons	.org/licens	es/by-nc	-nd/4.0/.

## References

AbdelHamid	M,	Jafar	A,	Rahal	Y	(2022)	Levantine	hate	speech	detection	in	twitter.	Soc	Netw	Anal	Min	
12(1):121
Abed	SS,	Dwivedi	YK,	Williams	MD	(2015)	Social	media	as	a	bridge	to	e-commerce	adoption	in	SMES:	a	
systematic	literature	review.	Mark	Rev	15(1):39-57
Ahmad	K,	Pogorelov	K,	Riegler	M,	Conci	N,	Halvorsen	P	(2019)	Social	media	and	satellites:	disaster	event	
detection,	linking	and	summarization.	Multimedia	Tools	Appl	78:2837-2875
Ahmad	K,	Ayub	M,	Khan	J,	Ahmad	N,	Al-Fuqaha	A	(2022)	Social	media	as	an	instant	source	of	feedback	on	
water	quality.	IEEE	Trans	Technol	Soc	4:325
Al-Jarf	R	(2021)	Derivation	from	foreign	words	and	acronyms	borrowed	in	Arabic.	Lingua.	Lang	Culture	
20(2):52-77
Al-Jarf	R	(2024)	Derivation	of	verbs	from	loanwords	in	Arabic	according	to	Arabic	derivational	paradigms.	
Int	J	Arts	Human	Stud	4(1):68-82
Alkhairy	M,	Jafri	A,	Cooper	A	(2023)	An	integrated,	bidirectional	pronunciation,	morphology,	and	diacritics	
finite-state	system.	Bidirectional	pronunciation,	morphology,	and	diacritics	finite-state	system
Alnajjar,	K,	Hämäläinen	M	(2024)	Normalization	of	Arabic	dialects	into	modern	standard	Arabic	using	bert	
and	gpt-2.	J	Data	Mining	Digit	Human.	https://doi.org/10.46298/jdmdh.13146
Al-Shaibani	M,	Ahmad	I	(2023)	Consonant	is	all	you	need:	a	compact	representation	of	english	text	for	efficient	nlp.	Findings	of	the	association	for	computational	linguistics:	EMNLP	2023:11578-11588
Alsmadi	I,	Ahmad	K,	Nazzal	M,	Alam	F,	Al-Fuqaha	A,	Khreishah	A,	Algosaibi	A	(2022)	Adversarial	NLP	
for	social	network	applications:	attacks,	defenses,	and	research	directions.	IEEE	transactions	on	computational social systems
Amati	G,	Ambrosi	E,	Bianchi	M,	Gaibisso	C,	Gambosi	G	(2008)	Automatic	construction	of	an	opinion-term	
vocabulary	for	ad	hoc	retrieval.	In:	European	conference	on	information	retrieval,	pp	89-100.	Springer
Androutsopoulos	JK	(2000)	Non-standard	spellings	in	media	texts:	the	case	of	German	fanzines.	J	Socioling	
4(4):514-533
Arafah	B,	Hasyim	M	(2019)	The	language	of	emoji	in	social	media.	KnE	Social	Sciences,	pp	494-504
Arora	M,	Kansal	V	(2019)	Character	level	embedding	with	deep	convolutional	neural	network	for	text	normalization	of	unstructured	data	for	twitter	sentiment	analysis.	Soc	Netw	Anal	Min	9(1):12
Arun	K,	Srinagesh	A	(2020)	Multi-lingual	twitter	sentiment	analysis	using	machine	learning.	Int	J	Electric	
Comput	Eng	10(6):5992-6000
Aschenbrenner	AJ,	Balota	DA,	Weigand	AJ,	Scaltritti	M,	Besner	D	(2017)	The	first	letter	position	effect	in	
visual	word	recognition:	the	role	of	spatial	attention.	J	Exp	Psychol	Hum	Percept	Perform	43(4):700
Asghar	MZ,	Sattar	A,	Khan	A,	Ali	A,	Masud	Kundi	F,	Ahmad	S	(2019)	Creating	sentiment	lexicon	for	sentiment	analysis	in	Urdu:	the	case	of	a	resource-poor	language.	Expert	Syst	36(3):12397
Attia	M	(2007)	Arabic	tokenization	system.	In:	Proceedings	of	the	2007	workshop	on	computational	
approaches	to	semitic	languages:	common	issues	and	resources,	pp	65-72
Aurpa	TT,	Sadik	R,	Ahmed	MS	(2022)	Abusive	Bangla	comments	detection	on	facebook	using	transformerbased	deep	learning	models.	Soc	Netw	Anal	Min	12(1):24
Aye	NZM,	Soe	KM	(2024)	Analysis	of	subword	tokenization	for	transformer	model	in	neural	machine	translation	between	Myanmar	and	english	languages.	In:	2024	IEEE	conference	on	computer	applications	
(ICCA),	pp	1-5.	IEEE
Azaz	M,	Alfaifi	E	(2022)	Lexical	variation	in	regional	modern	standard	Arabic.	Lang	Matter	53(1):103-125
Aziz	R,	Anwar	MW,	Jamal	MH,	Bajwa	UI,	Castilla	ÁK,	Rios	CU,	Thompson	EB,	Ashraf	I	(2023)	Real	word	
spelling	error	detection	and	correction	for	Urdu	language.	IEEE	Access
Azmi	AM,	Almutery	MN,	Aboalsamh	HA	(2019)	Real-word	errors	in	Arabic	texts:	a	better	algorithm	for	
detection	and	correction.	IEEE/ACM	Trans	Audio	Speech	Lang	Proc	27(8):1308-1320
Bach	NX,	Linh	ND,	Phuong	TM	(2018)	An	empirical	study	on	pos	tagging	for	Vietnamese	social	media	text.	
Comput	Speech	Lang	50:1-15
Bai	Y	(2023)	Deep	learning-based	pre-diagnosis	and	analysis	of	psychological	disorders.	Int	J	Educ	Human	
6(3):126-130
Baig	A,	Rahman	MU,	Kazi	H,	Baloch	A	(2020)	Developing	a	pos	tagged	corpus	of	Urdu	tweets.	Computers	
9(4):90
1 3
Page 41 of 48 89

---


<!-- PAGE 42 -->

J. Khan et al.
Bakar	MFRA,	Idris	N,	Shuib	L	(2019)	An	enhancement	of	malay	social	media	text	normalization	for	lexiconbased	sentiment	analysis.	In:	2019	international	conference	on	Asian	language	processing	(IALP),	pp	
211-215.	IEEE
Balahur	A	(2013)	Sentiment	analysis	in	social	media	texts.	In:	Proceedings	of	the	4th	workshop	on	computational	approaches	to	subjectivity,	sentiment	and	social	media	analysis,	pp	120-128
Balakrishnan	V,	Lloyd-Yemoh	E	(2014)	Stemming	and	lemmatization:	a	comparison	of	retrieval	performances.	Lecture	Notes	Software	Eng	2(3):174
Baldwin	T,	Li	Y	(2015)	An	in-depth	analysis	of	the	effect	of	text	normalization	in	social	media.	In:	Proceedings	of	the	2015	conference	of	the	North	American	chapter	of	the	association	for	computational	linguistics:	human	language	technologies,	pp	420-429
Baldwin	T,	Cook	P,	Lui	M,	MacKinlay	A,	Wang	L	(2013)	How	noisy	social	media	text,	how	diffrnt	social	
media	sources?	In:	Proceedings	of	the	sixth	international	joint	conference	on	natural	language	processing,	pp	356-364
Barbieri	F,	Basile	V,	Croce	D,	Nissim	M,	Novielli	N,	Patti	V,	et	al.	(2016)	Overview	of	the	evalita	2016	sentiment	polarity	classification	task.	In:	CEUR	workshop	proceedings,	vol.	1749.	CEUR-WS
Basile	V,	Bosco	C,	Fersini	E,	Nozza	D,	Patti	V,	Pardo	FMR,	Rosso	P,	Sanguinetti	M	(2019)	Semeval-2019	
task	5:	multilingual	detection	of	hate	speech	against	immigrants	and	women	in	twitter.	In:	Proceedings	
of	the	13th	international	workshop	on	semantic	evaluation,	pp	54-63
Berthelier	B	(2023)	Division	and	the	digital	language	divide:	a	critical	perspective	on	natural	language	processing	resources	for	the	south	and	north	korean	languages.	Korean	Stud	47(1):243-273
Bhamidipati	NL,	Pal	SK	(2007)	Stemming	via	distribution-based	word	segregation	for	classification	and	
retrieval.	IEEE	Trans	Syst	Man	Cybernet	Part	B	37(2):350-360
Bhatti	Z,	Ismaili	IA,	Shaikh	AA,	Javaid	W	(2014)	Spelling	error	trends	and	patterns	in	Sindhi.	arXiv	preprint	
arXiv:1403.4759
Bhatti,	Z.,	Ismaili,	I.A.,	Shaikh,	A.A.,	Javaid,	W.:	Spelling	error	trends	and	patterns	in	sindhi.	J	Emerging	
Trends	Comput	Inform	Sci.	https://doi.org/10.48550/arXiv.1403.4759
Bick	E	(2020)	An	annotated	social	media	corpus	for	German.	In:	12th	language	resources	and	evaluation	
conference,	pp	6127-6135.	European	language	resources	association	(ELRA)
Biswas	S,	Rajan	H	(2021)	Fair	preprocessing:	towards	understanding	compositional	fairness	of	data	transformers	in	machine	learning	pipeline.	In:	Proceedings	of	the	29th	ACM	joint	meeting	on	european	software	engineering	conference	and	symposium	on	the	foundations	of	software	engineering,	pp	981-993
Boia	M,	Faltings	B,	Musat	C-C,	Pu	P	(2013)	A:	is	worth	a	thousand	words:	how	people	attach	sentiment	to	
emoticons	and	words	in	tweets.	In:	2013	international	conference	on	social	computing,	pp	345-350.	
IEEE
Boot	AB,	Kim	ST,	Dijkstra	E	(2019)	How	character	limit	affects	language	usage	in	tweets.	Palgrave	Commun	5:76
Borrelli	D,	Gongora	Svartzman	G,	Lipizzi	C	(2020)	Unsupervised	acquisition	of	idiomatic	units	of	symbolic	
natural	language:	an	n-gram	frequency-based	approach	for	the	chunking	of	news	articles	and	tweets.	
PLoS	ONE	15(6):0234214
Brants	W,	Sharif	B,	Serebrenik	A	(2019)	Assessing	the	meaning	of	emojis	for	emotional	awareness-a	pilot	
study.	In:	Companion	proceedings	of	the	2019	world	wide	web	conference,	pp	419-423
Brosh	H	(2015)	Arabic	spelling:	errors,	perceptions,	and	strategies.	Foreign	Lang	Ann	48(4):584-603
Bustamante	FR,	Díaz	EL	(2006)	Spelling	error	patterns	in	Spanish	for	word	processing	applications.	In:	
LREC,	pp	93-98
Cagnoni	S,	Ferrari	L,	Fornacciari	P,	Mordonini	M,	Sani	L,	Tomaiuolo	M	(2021)	Improving	sentiment	analysis	using	preprocessing	techniques	and	lexical	patterns.	Int	J	Data	Anal	Tech	Strateg	13(3):171-185
Calmon	F,	Wei	D,	Vinzamuri	B,	Natesan	Ramamurthy	K,	Varshney	KR	(2017)	Optimized	pre-processing	for	
discrimination	prevention.	Adv	Neural	Inform	Proc	Syst	30
Chatterjee	N	(2019)	A	trie	based	model	for	sms	text	normalization.	In:	Intelligent	computing-proceedings	of	
the	computing	conference,	pp	846-859.	Springer
Chen	T,	Kan	M-Y	(2013)	Creating	a	live,	public	short	message	service	corpus:	the	nus	SMS	corpus.	Lang	
Resour	Eval	47:299-335
Chen	Q,	Crooks	A	(2022)	Analyzing	the	vaccination	debate	in	social	media	data	pre-and	post-covid-19	pandemic.	Int	J	Appl	Earth	Obs	Geoinf	110:102783
Chen	X,	Wang	C,	Li	D,	Sun	X	(2021)	A	new	early	rumor	detection	model	based	on	BIGRU	neural	network.	
Discret	Dyn	Nat	Soc	2021:1-11
Choudhury	M,	Chittaranjan	G,	Gupta	P,	Das	A	(2014)	Overview	and	datasets	of	fire	2014	track	on	transliterated	search.	In:	Pre-proceedings	6th	workshop	FIRE-2014
Chu	X,	Ilyas	IF,	Krishnan	S,	Wang	J	(2016)	Data	cleaning:	overview	and	emerging	challenges.	In:	Proceedings	of	the	2016	international	conference	on	management	of	data,	pp	2201-2206
1 3
89 Page 42 of 48

---


<!-- PAGE 43 -->

Textual variations in social media text processing applications:…
Clark	E,	Roberts	T,	Araki	K	(2010)	Towards	a	pre-processing	system	for	casual	english	annotated	with	linguistic	and	cultural	information.	Proceedings	of	the	fifth	IASTED	international	conference	711:044-084
Cognola	F,	Casalicchio	J	(2023)	Microvariation	in	the	distribution	of	resumptive	pronouns	in	the	left	dislocation	construction	in	two	Tyrolean	Dialects	of	Northern	Italy.	Languages	8(2):91
Contractor	D,	Faruquie	TA,	Subramaniam	LV	(2010)	Unsupervised	cleansing	of	noisy	text.	In:	Coling	2010:	
posters,	pp	189-196
Craig	D,	Cunningham	S	(2019)	Social	media	entertainment:	The	new	intersection	of	Hollywood	and	Silicon	
Valley.	NYU	Press,	New	York
Daniels	PT	(2013)	The	Arabic	writing	system.	The	Oxford	handbook	of	Arabic	linguistics,	422-431	(2013)
Daud	A,	Khan	W,	Che	D	(2017)	Urdu	language	processing:	a	survey.	Artif	Intell	Rev	47:279-311
Davidson	T,	Warmsley	D,	Macy	M,	Weber	I	(2017)	Automated	hate	speech	detection	and	the	problem	
of	offensive	language.	Proceedings	of	the	international	AAAI	conference	on	web	and	social	media	
11:512-515
Desai	N,	Narvekar	M	(2015)	Normalization	of	noisy	text	data.	Procedia	Comput	Sci	45:127-132
Dinakar	S,	Andhale	P,	Rege	M	(2015)	Sentiment	analysis	of	social	network	content.	In:	2015	IEEE	international	conference	on	information	reuse	and	integration,	pp	189-192.	IEEE
Dixon	L,	Li	J,	Sorensen	J,	Thain	N,	Vasserman	L	(2018)	Measuring	and	mitigating	unintended	bias	in	text	
classification.	In:	Proceedings	of	the	2018	AAAI/ACM	conference	on	AI,	ethics,	and	society,	pp	67-73
Dolan	B,	Brockett	C	(2005)	Automatically	constructing	a	corpus	of	sentential	paraphrases.	In:	Third	international	workshop	on	paraphrasing	(IWP2005)
Doshi	F,	Gandhi	J,	Gosalia	D,	Bagul	S	(2020)	Normalizing	text	using	language	modelling	based	on	phonetics	
and	string	similarity.	arXiv	preprint	arXiv:2006.14116
Downs	B,	Anuyah	O,	Shukla	A,	Fails	JA,	Pera	S,	Wright	K,	Kennington	C	(2020)	Kidspell:	a	child-oriented,	
rule-based,	phonetic	spellchecker.	In:	Proceedings	of	the	12th	language	resources	and	evaluation	conference,	pp	6937-6946
Duong	H-T,	Nguyen-Thi	T-A	(2021)	A	review:	preprocessing	techniques	and	data	augmentation	for	sentiment	analysis.	Comput	Soc	Networks	8(1):1-16
Durrani	N,	Hussain	S	(2010)	Urdu	word	segmentation.	In:	Human	language	technologies:	the	2010	annual	
conference	of	the	North	American	chapter	of	the	association	for	computational	linguistics,	pp	528-536
Eger	S,	Benz	Y	(2020)	From	hero	to	zéroe:	a	benchmark	of	low-level	adversarial	attacks.	In:	Proceedings	of	
the	1st	conference	of	the	Asia-Pacific	chapter	of	the	association	for	computational	linguistics	and	the	
10th	international	joint	conference	on	natural	language	processing,	pp	786-803
Eger	S,	Şahin	GG,	Rücklé	A,	Lee	J-U,	Schulz	C,	Mesgar	M,	Swarnkar	K,	Simpson	E,	Gurevych	I	(2019)	
Text	processing	 like	 humans	 do:	 visually	 attacking	 and	 shielding	 NLP	 systems.	 arXiv	 preprint	
arXiv:1903.11508
Eight	F	(2019)	First	GOP	debate	twitter	sentiment.		h	t	t	p	s		:	/	/	w	w	w		.	k	a	g	g		l	e	.	c		o	m	/	c	r	o	w	d	fl	 	o	w	e	r	/	fi	 	r	s	t	-	g	o	p	-	d	e	b	a	t	e	-	t	
w	i	t	t	e	r	-	s	e	n	t	i	m	e	n	t	      
Eisenstein	J	(2013)	Phonological	factors	in	social	media	writing.	In:	Proceedings	of	the	workshop	on	language	analysis	in	social	media,	pp	11-19
Elfaik	H,	Nfaoui	EH	(2022)	Sentiment	analysis	in	social	networks	using	convolutional	neural	networks.	In:	
Advanced	intelligent	systems	for	sustainable	development	(AI2SD'2020)	Vol	2,	pp	263-276.	Springer
Elnagar	A,	Yagi	SM,	Nassif	AB,	Shahin	I,	Salloum	SA	(2021)	Systematic	literature	review	of	dialectal	Arabic:	identification	and	detection.	IEEE	Access	9:31010-31042
Elsafoury	F	(2020)	Cyberbullying	datasets.	Mendeley	Data.	https://dat	a.mendeley.	com/dataset	s/wmx9jj	
2htd/2
Elzayady	H,	Mohamed	MS,	Badran	KM,	Salama	GI	(2023)	A	hybrid	approach	based	on	personality	traits	for	
hate	speech	detection	in	Arabic	social	media.	Int	J	Electric	Comput	Eng	13(2):1979
Esposito	M,	Damiano	E,	Minutolo	A,	De	Pietro	G,	Fujita	H	(2020)	Hybrid	query	expansion	using	lexical	
resources	and	word	embeddings	for	sentence	retrieval	in	question	answering.	Inf	Sci	514:88-105
Febriana	T,	Budiarto	A	(2019)	Twitter	dataset	for	hate	speech	and	cyberbullying	detection	in	Indonesian	
language.	In:	2019	international	conference	on	information	management	and	technology	(ICIMTech),	
vol	1,	pp	379-382.	IEEE
Fernández	J,	Gómez	JM,	Martínez-Barco	P	(2014)	A	supervised	approach	for	sentiment	analysis	using	skipgrams.	In:	Proceedings	of	the	workshop	on	natural	language	processing	in	the	5th	information	systems	
research	working	days	(JISIC),	pp	30-36
Gao	J,	Lanchantin	J,	Soffa	ML,	Qi	Y	(2018)	Black-box	generation	of	adversarial	text	sequences	to	evade	deep	
learning	classifiers.	In:	2018	IEEE	security	and	privacy	workshops	(SPW),	pp	50-56.	IEEE
Garg	Y,	Chatterjee	N	(2014)	Sentiment	analysis	of	twitter	feeds.	In:	Big	data	analytics:	third	international	
conference,	BDA	2014,	New	Delhi,	India,	December	20-23,	2014.	Proceedings	3,	pp	33-52.	Springer
Gasparetto	A,	Zangari	A,	Marcuzzo	M,	Albarelli	A	(2022)	A	survey	on	text	classification:	practical	perspectives	on	the	Italian	language.	PLoS	ONE	17(7):0270904
1 3
Page 43 of 48 89

---


<!-- PAGE 44 -->

J. Khan et al.
Gautam	AK,	Bansal	A	(2022)	Effect	of	features	extraction	techniques	on	cyberstalking	detection	using	
machine	learning	framework.	J	Adv	Inform	Technol	13(5)
Gimpel	K,	Schneider	N,	O'connor	B,	Das	D,	Mills	DP,	Eisenstein	J,	Heilman	M,	Yogatama	D,	Flanigan	J,	
Smith	NA	(2011)	Part-of-speech	tagging	for	twitter:	annotation,	features,	and	experiments.	In:	Proceedings of the 49th annual meeting of the association for computational linguistics: human language 
technologies,	pp	42-47
Glazkova	A	(2023)	A	comparison	of	text	preprocessing	techniques	for	hate	and	offensive	speech	detection	in	
twitter.	Soc	Netw	Anal	Min	13(1):155
Golbeck	J,	Ashktorab	Z,	Banjo	RO,	Berlinger	A,	Bhagwan	S,	Buntain	C,	Cheakalos	P,	Geller	AA,	Gnanasekaran	RK,	Gunasekaran	RR,	et al.	(2017)	A	large	labeled	corpus	for	online	harassment	research.	In:	
Proceedings	of	the	2017	ACM	on	web	science	conference,	pp	229-233
Grancharova	M,	Jangefalk	M	(2018)	Comparative	study	of	the	combined	performance	of	learning	algorithms	
and	preprocessing	techniques	for	text	classification
Grefenstette	DAHG	(1996)	A	detailed	analysis	of	English	stemming	algorithms.	Rank	Xerox	Res	Centre	
6:1-16
Grgić-Hlača	N,	Zafar	MB,	Gummadi	KP,	Weller	A	(2018)	Beyond	distributive	fairness	in	algorithmic	decision	making:	feature	selection	for	procedurally	fair	learning.	In:	Proceedings	of	the	AAAI	conference	
on	artificial	intelligence,	vol	32
Habash	N,	Metsky	H	(2008)	Automatic	learning	of	morphological	variations	for	handling	out-of-vocabulary	
terms	in	Urdu-English	mt.	In:	Proceedings	of	the	8th	conference	of	the	association	for	machine	translation	in	the	Americas:	research	papers,	pp	107-116
Habash	N,	Diab	MT,	Rambow	O	(2012)	Conventional	orthography	for	dialectal	Arabic.	In:	LREC,	pp	
711-718
Han	B,	Baldwin	T	(2011)	Lexical	normalisation	of	short	text	messages:	Makn	sens	a#	twitter.	In:	Proceedings	
of the 49th annual meeting of the association for computational linguistics: human language technolo -
gies,	pp	368-378
Hassan	H,	Menezes	A	(2013)	Social	text	normalization	using	contextual	graph	random	walks.	In:	Proceedings	of	the	51st	annual	meeting	of	the	association	for	computational	linguistics	(Volume	1:	Long	
Papers),	pp	1577-1586
Hegazi	MO,	Al-Dossari	Y,	Al-Yahy	A,	Al-Sumari	A,	Hilal	A	(2021)	Preprocessing	Arabic	text	on	social	
media.	Heliyon	7(2):06191
Hettiarachchi	N,	Weerasinghe	R,	Pushpanda	R	(2020)	Detecting	hate	speech	in	social	media	articles	in	
Romanized	Sinhala.	In:	2020	20th	international	conference	on	advances	in	ICT	for	emerging	regions	
(ICTer),	pp	250-255.	IEEE
Hovermale	D	(2008)	Scale:	spelling	correction	adapted	for	learners	of	english.	In:	Pre-CALICO	workshop	
on	"automatic	analysis	of	learner	language:	bridging	foreign	language	teaching	needs	and	NLP	possibilities. Citeseer
Hu	M,	Liu	B	(2004)	Mining	and	summarizing	customer	reviews.	In:	Proceedings	of	the	tenth	ACM	SIGKDD	
international	conference	on	knowledge	discovery	and	data	mining,	pp	168-177
Huertas-García	Á,	Martín	A,	Huertas-Tato	J,	Camacho	D	(2023)	Countering	malicious	content	moderation	
evasion	in	online	social	networks:	simulation	and	detection	of	word	camouflage.	Appl	Soft	Comput	
145:110552
Husain	F,	Uzuner	O	(2022)	Investigating	the	effect	of	preprocessing	Arabic	text	on	offensive	language	and	
hate	speech	detection.	Trans	Asian	Low-Res	Lang	Inform	Proc	21(4):1-20
Ibrohim	MO,	Setiadi	MA,	Budi	I	(2019)	Identification	of	hate	speech	and	abusive	language	on	Indonesian	
twitter	using	the	word2vec,	part	of	speech	and	emoji	features.	In:	Proceedings	of	the	international	conference	on	advanced	information	science	and	system,	pp	1-5
Islam	MIK,	Meem	RI,	Kasem	FBA,	Rakshit	A,	Habib	MT	(2019)	Bangla	spell	checking	and	correction	using	
edit	distance.	In:	2019	1st	international	conference	on	advances	in	science,	engineering	and	robotics	
technology	(ICASERT),	pp	1-4.	IEEE
Johnson	RL,	Eisler	ME	(2012)	The	importance	of	the	first	and	last	letter	in	words	during	sentence	reading.	
Acta	Physiol	(Oxf)	141(3):336-351
Joshi	S,	Villalba	J,	Żelasko	P,	Moro-Velázquez	L,	Dehak	N	(2021)	Study	of	pre-processing	defenses	against	
adversarial	attacks	on	state-of-the-art	speaker	recognition	systems.	IEEE	Trans	Inf	Forensics	Secur	
16:4811-4826
Kalamatianos	G,	Mallis	D,	Symeonidis	S,	Arampatzis	A	(2015)	Sentiment	analysis	of	Greek	tweets	and	
hashtags	using	a	sentiment	lexicon.	In:	Proceedings	of	the	19th	panhellenic	conference	on	informatics,	
pp	63-68
Karoo	K,	Chitte	MV	(2023)	Ethical	considerations	in	sentiment	analysis:	navigating	the	complex	landscape.	
Int	Res	of	Modern	in	Eng	Techn	Sci	5(11):2991-3006		h	t	t	p	s		:	/	/	w	w	w		.	i	r	j	m		e	t	s	.		c	o	m	/	u		p	l	o	a	d	e		d	fi	 	l	e		s	/	p	a		p	e	r	/	/	i	s	
s	u	e	_	1	1	_	n	o	v	e	m	b	e	r	_	2	0	2	3	/	4	6	8	1	1	/	fi	 	n	a	l	/	fi	 	n	_	i	r	j	m	e	t	s	1	7	0	1	2	5	4	8	0	1	.	p	d	f	      
1 3
89 Page 44 of 48

---


<!-- PAGE 45 -->

Textual variations in social media text processing applications:…
Keidar	D,	Opedal	A,	Jin	Z,	Sachan	M	(2022)	Slangvolution:	a	causal	analysis	of	semantic	change	and	frequency	dynamics	in	slang.	arXiv	preprint	arXiv:2203.04651
Keller	Y,	Mackensen	J,	Eger	S	(2021)	Bert-defense:	a	probabilistic	model	based	on	BERT	to	combat	cognitively	inspired	orthographic	adversarial	attacks.	arXiv	preprint	arXiv:2106.01452
Khan	J,	Lee	S	(2019)	Implicit	user	trust	modeling	based	on	user	attributes	and	behavior	in	online	social	networks.	IEEE	Access	7:142826-142842
Khan	J,	Lee	S	(2020)	Enhancement	of	sentiment	analysis	by	utilizing	noisy	social	media	texts.	J	Korean	Inst	
Commun	Sci	45(6):1027-1037
Khan	J,	Lee	S	(2021)	Enhancement	of	text	analysis	using	context-aware	normalization	of	social	media	informal	text.	Appl	Sci	11(17):8172
Khan	FH,	Qamar	U,	Bashir	S	(2016)	Sentimi:	introducing	point-wise	mutual	information	with	sentiwordnet	
to	improve	sentiment	polarity	detection.	Appl	Soft	Comput	39:140-153
Khan	J,	Ahmad	K,	Sohn	K-A	(2023)	An	efficient	character-level	adversarial	attack	inspired	by	textual	variations	in	online	social	media	platforms.	Comput	Syst	Sci	Eng	47(3):2869
Kim	Y-H	(2024)	On	morphological	requirements	for	auxiliary	verb	periphrasis	in	Turkish.	Glossa:	J	General	
Linguist 9(1)
Kiritchenko	S,	Zhu	X,	Mohammad	SM	(2014)	Sentiment	analysis	of	short	informal	texts.	J	Artif	Intell	Res	
50:723-762
Koch	TK,	Romero	P,	Stachl	C	(2022)	Age	and	gender	in	language,	emoji,	and	emoticon	usage	in	instant	messages.	Comput	Hum	Behav	126:106990
Kolajo	T,	Daramola	O,	Adebiyi	A,	Seth	A	(2020)	A	framework	for	pre-processing	of	social	media	feeds	based	
on	integrated	local	knowledge	base.	Inform	Proc	Manage	57(6):102348
Krovetz	R	(1993)	Viewing	morphology	as	an	inference	process.	In:	Proceedings	of	the	16th	annual	international	ACM	SIGIR	conference	on	research	and	development	in	information	retrieval,	pp	191-202
Kshirsagar	R,	Cukuvac	T,	McKeown	K,	McGregor	S	(2018)	Predictive	embeddings	for	hate	speech	detection	
on	twitter.	arXiv	preprint	arXiv:1809.10644
Kukich	K	(1992)	Techniques	for	automatically	correcting	words	in	text.	ACM	Comput	Surv	(CSUR)	
24(4):377-439
Kumar	A,	Garg	G	(2019)	Sarc-m:	sarcasm	detection	in	typo-graphic	memes.	In:	International	conference	on	
advances	in	engineering	science	management	&	technology	(ICAESMT)-2019,	Uttaranchal	University,	
Dehradun,	India
Kumar	P,	Garg	K	(2021)	Preprocessing	steps	for	opinion	mining	on	tweets.	In:	Evolving	technologies	for	
computing,	communication	and	smart	world:	proceedings	of	ETCCS	2020,	pp	333-344.	Springer
Kumar	A,	Chandrayan	A,	Dubey	SK	(2023)	Exploring	the	emotion	recognition	in	speech	using	machine	
learning.	In:	Computational	intelligence:	select	proceedings	of	InCITe	2022,	pp	737-749.	Springer
Lee	J-H,	Kim	M,	Kwon	H-C	(2020)	Deep	learning-based	context-sensitive	spelling	typing	error	correction.	
IEEE	Access	8:152565-152578
Lee	H,	Ha	M,	Lee	J,	Aini	RQ,	Rusmana	AN,	Sya'bandari	Y,	Lee	J-K,	Shin	S,	Lee	G-G,	Choo	J,	et	al.	(2023)	
Spelling	errors	in	Korean	students'	constructed	responses	and	the	efficacy	of	automatic	spelling	correction	on	automated	computer	scoring.	Technol	Knowl	Learn,	pp	1-21
Lertpiya	A,	Chalothorn	T,	Chuangsuwanich	E	(2020)	Thai	spelling	correction	and	word	normalization	on	
social	text	using	a	two-stage	pipeline	with	neural	contextual	attention.	IEEE	Access	8:133403-133419
Li	J,	Ji	S,	Du	T,	Li	B,	Wang	T	(2018)	Textbugger:	generating	adversarial	text	against	real-world	applications.	
arXiv	preprint	arXiv:1812.05271
Li	G,	Li	B,	Huang	L,	Hou	S	(2020)	Automatic	construction	of	a	depression-domain	lexicon	based	on	microblogs:	text	mining	study.	JMIR	Med	Inform	8(6):17650
Liang	BWWHL,	Kourie	DG	(2008)	Classification	for	selected	spell	checkers	and	correctors.	University	of	
South	Africa,	School	of	computing
Liu	F,	Weng	F	(2015)	Broad-coverage	normalization	system	for	social	media	language.	Google	Patents.	US	
Patent	9,164,983
Liu	X,	Zhang	S,	Wei	F,	Zhou	M	(2011)	Recognizing	named	entities	in	tweets.	In:	Proceedings	of	the	49th	
annual	meeting	of	the	association	for	computational	linguistics:	human	language	technologies,	pp	
359-367
Liu	Y,	Ott	M,	Goyal	N,	Du	J,	Joshi	M,	Chen	D,	Levy	O,	Lewis	M,	Zettlemoyer	L,	Stoyanov	V	(2019)	
Roberta:	a	robustly	optimized	bert	pretraining	approach.	arXiv	preprint	arXiv:1907.11692
Lochter	JV,	Silva	RM,	Almeida	TA	(2020)	Deep	learning	models	for	representing	out-of-vocabulary	words.	
In:	Brazilian	conference	on	intelligent	systems,	pp	418-434.	Springer
Łockiewicz	M,	Barzowska	N	(2024)	Typical	spelling	errors	of	grade	1	spellers	of	polish:	an	exploratory	study	
adapting	the	pomas	classification	to	the	polish	orthography.	Reading	and	Writing,	pp	1-25
Majumder	P,	Mitra	M,	Parui	SK,	Kole	G,	Mitra	P,	Datta	K	(2007)	Yass:	yet	another	suffix	stripper.	ACM	
Trans	Inform	Syst	(TOIS)	25(4):18
1 3
Page 45 of 48 89

---


<!-- PAGE 46 -->

J. Khan et al.
Maltseva	AV,	Makhnytkina	OV,	Shilkina	NE,	Lizunova	IA	(2020)	Social	media	sentiment	analysis	with	context	space	model.	In:	Electronic	governance	and	open	society:	challenges	in	Eurasia:	6th	international	
conference,	EGOSE	2019,	St.	Petersburg,	Russia,	November	13-14,	2019,	Proceedings	6,	pp	399-412.	
Springer
Mandl	T,	Modha	S,	Majumder	P,	Patel	D,	Dave	M,	Mandlia	C,	Patel	A	(2019)	Overview	of	the	HASOC	track	
at	fire	2019:	hate	speech	and	offensive	content	identification	in	Indo-European	languages.	In:	Proceedings	of	the	11th	annual	meeting	of	the	Forum	for	information	retrieval	evaluation,	pp	14-17
Mansur	Z,	Omar	N,	Tiun	S,	Alshari	EM	(2024)	A	normalization	model	for	repeated	letters	in	social	media	
hate	speech	text	based	on	rules	and	spelling	correction.	PLoS	ONE	19(3):0299652
Masadeh	R,	Sa'ad	Al-Azzam	BH	(2020)	A	hybrid	approach	of	lexicon-based	and	corpus-based	techniques	for	
Arabic	book	aspect	and	review	polarity	detection.	Int	J	9:2494
Maslej-Krešňáková	V,	Sarnovskỳ	M,	Butka	P,	Machová	K	(2020)	Comparison	of	deep	learning	models	and	
various	text	pre-processing	techniques	for	the	toxic	comments	classification.	Appl	Sci	10(23):8631
Mayfield	J,	McNamee	P	(2003)	Single	n-gram	stemming.	In:	Proceedings	of	the	26th	annual	international	
ACM	SIGIR	conference	on	research	and	development	in	informaion	retrieval,	pp	415-416
Meftah	S,	Semmar	N	(2018)	A	neural	network	model	for	part-of-speech	tagging	of	social	media	texts.	In:	Proceedings	of	the	eleventh	international	conference	on	language	resources	and	evaluation	(LREC	2018)
Melucci	M,	Orio	N	(2003)	A	novel	method	for	stemmer	generation	based	on	hidden	MARKOV	models.	In:	
Proceedings	of	the	twelfth	international	conference	on	information	and	knowledge	management,	pp	
131-138
Mielke	SJ,	Alyafeai	Z,	Salesky	E,	Raffel	C,	Dey	M,	Gallé	M,	Raja	A,	Si	C,	Lee	WY,	Sagot	B,	et	al.	(2021)	
Between	words	and	characters:	a	brief	history	of	open-vocabulary	modeling	and	tokenization	in	nlp.	
arXiv	preprint	arXiv:2112.10508
Mohammad	S	(2012)	#	emotional	tweets.	In:	*	SEM	2012:	the	first	joint	conference	on	lexical	and	computational	semantics-volume	1:	proceedings	of	the	main	conference	and	the	shared	task,	and	volume	2:	
proceedings	of	the	sixth	international	workshop	on	semantic	evaluation	(SemEval	2012),	pp	246-255
Mohammad	S,	Turney	P	(2010)	Emotions	evoked	by	common	words	and	phrases:	using	mechanical	turk	
to	create	an	emotion	lexicon.	In:	Proceedings	of	the	NAACL	HLT	2010	workshop	on	computational	
approaches	to	analysis	and	generation	of	emotion	in	text,	pp	26-34
Mohammad	SM,	et	al.	(2013)	Tracking	sentiment	in	mail:	How	genders	differ	on	emotional	axes.	arXiv	
preprint arXiv:1309.6347
Mohammad	SM,	Kiritchenko	S,	Zhu	X	(2013)	Nrc-canada:	building	the	state-of-the-art	in	sentiment	analysis	
of	tweets.	arXiv	preprint	arXiv:1308.6242
Moh	M,	Moh	T-S,	Khieu	B	(2020)	No"	love"	lost:	defending	hate	speech	detection	models	against	adversaries.	In:	2020	14th	International	conference	on	ubiquitous	information	management	and	communication	
(IMCOM),	pp	1-6.	IEEE
Moorhead	SA,	Hazlett	DE,	Harrison	L,	Carroll	JK,	Irwin	A,	Hoving	C	(2013)	A	new	dimension	of	health	
care:	systematic	review	of	the	uses,	benefits,	and	limitations	of	social	media	for	health	communication.	
J	Med	Internet	Res	15(4):1933
Moral	C,	Antonio	A,	Imbert	R,	Ramírez	J	(2014)	A	survey	of	stemming	algorithms	in	information	retrieval.	
Inform	Res:	Int	Electron	J	19(1):1
Mori	Y	(2020)	Perceptual	differences	about	kanji	instruction:	native	versus	nonnative,	and	secondary	versus	
postsecondary	instructors	of	Japanese.	Foreign	Lang	Ann	53(3):550-575
Muis	AO,	Lu	W	(2016)	Weak	semi-markov	CRFS	for	noun	phrase	chunking	in	informal	text.	In:	Proceedings	
of	the	2016	conference	of	the	North	American	chapter	of	the	association	for	computational	linguistics:	
human	language	technologies,	pp	714-719
Napitu	FE,	Suhardianto	S	(2020)	An	analysis	of	slang	words	abbreviation	in	American	caption	on	instagram:	
a	sociolinguistics	approach.	Sci	J:	Jurnal	Ilmiah	Mahasiswa	2(1)
Naseem	U,	Razzak	I,	Eklund	PW	(2021)	A	survey	of	pre-processing	techniques	to	improve	short-text	quality:	
a	case	study	on	hate	speech	detection	on	twitter.	Multimedia	Tools	Appl	80(28):35239-35266
Neal	T,	Sundararajan	K,	Fatima	A,	Yan	Y,	Xiang	Y,	Woodard	D	(2017)	Surveying	stylometry	techniques	and	
applications.	ACM	Comput	Surv	(CSuR)	50(6):1-36
Nikolaev	A,	Chuang	Y-Y,	Baayen	RH	(2022)	A	generating	model	for	finnish	nominal	inflection	using	distributional	semantics.	Mental	Lexicon	17(3):368-394
Nooralahzadeh	F,	Brun	C,	Roux	C	(2014)	Part	of	speech	tagging	for	French	social	media	data.	In:	Proceedings	of	COLING	2014,	the	25th	international	conference	on	computational	linguistics:	technical	papers,	
pp	1764-1772
Odell	MK	(1956)	The	profit	in	records	management.	Systems	(New	York)	20:20
1 3
89 Page 46 of 48

---


<!-- PAGE 47 -->

Textual variations in social media text processing applications:…
Owoputi	O,	O'Connor	B,	Dyer	C,	Gimpel	K,	Schneider	N,	Smith	NA	(2013)	Improved	part-of-speech	tagging	for	online	conversational	text	with	word	clusters.	In:	Proceedings	of	the	2013	conference	of	the	
North	American	chapter	of	the	association	for	computational	linguistics:	human	language	technologies,	
pp	380-390
Peacock	DC,	Khan	HU	(2019)	Effectiveness	of	social	media	sentiment	analysis	tools	with	the	support	of	
emoticon/emoji.	In:	16th	international	conference	on	information	technology-new	generations	(ITNG	
2019),	pp	491-494.	Springer
Pennell	DL,	Liu	Y	(2010)	Normalization	of	text	messages	for	text-to-speech.	In:	2010	IEEE	international	
conference	on	acoustics,	speech	and	signal	processing,	pp	4842-4845.	IEEE
Pericherla	S,	Ilavarasan	E	(2021)	Performance	analysis	of	word	embeddings	for	cyberbullying	detection.	In:	
IOP	conference	series:	materials	science	and	engineering,	vol	1085,	p	012008.	IOP	Publishing
Poria	S,	Hazarika	D,	Majumder	N,	Mihalcea	R	(2020)	Beneath	the	tip	of	the	iceberg:	current	challenges	and	
new	directions	in	sentiment	analysis	research.	IEEE	Trans	Affect	Comput	14(1):108-132
Pota	M,	Ventura	M,	Fujita	H,	Esposito	M	(2021)	Multilingual	evaluation	of	pre-processing	for	BERT-based	
sentiment	analysis	of	tweets.	Expert	Syst	Appl	181:115119
Priya	M,	Kalpana	R,	Srisupriya	T	(2017)	Hybrid	optimization	algorithm	using	n	gram	based	edit	distance.	In:	
2017	international	conference	on	communication	and	signal	processing	(ICCSP),	pp	0216-0221.	IEEE
Pruthi	D,	Dhingra	B,	Lipton	ZC	(2019)	Combating	adversarial	misspellings	with	robust	word	recognition.	
arXiv	preprint	arXiv:1905.11268
Puigcerver	J,	Toselli	AH,	Vidal	E	(2017)	Querying	out-of-vocabulary	words	in	lexicon-based	keyword	spotting.	Neural	Comput	Appl	28:2373-2382
Rehman	Z,	Anwar	W,	Bajwa	UI	(2011)	Challenges	in	Urdu	text	Tokenization	and	sentence	boundary	disambiguation.	In:	Proceedings	of	the	2nd	workshop	on	South	Southeast	Asian	natural	language	processing	
(WSSANLP),	pp	40-45
Reynolds	R,	Janda	L,	Nesset	T	(2022)	A	cognitive	linguistic	approach	to	analysis	and	correction	of	orthographic	errors.	Russian	J	Linguist	26(2):391-408
Rimrott	A,	Heift	T	(2008)	Evaluating	automatic	detection	of	misspellings	in	German
Roark	B,	Charniak	E	(2000)	Noun-phrase	co-occurrence	statistics	for	semi-automatic	semantic	lexicon	construction.	arXiv	preprint	cs/0008026
Rodríguez-Rubio	S,	Fernández-Quesada	N	(2020)	Towards	accuracy:	a	model	for	the	analysis	of	typographical	errors	in	specialised	Bilingual	dictionaries	two	case	studies.	Lexikos	30:386-415
Rosenthal	S,	Farra	N,	Nakov	P	(2019)	Semeval-2017	task	4:	sentiment	analysis	in	twitter.	arXiv	preprint	
arXiv:1912.00741
Said	N,	Ahmad	K,	Riegler	M,	Pogorelov	K,	Hassan	L,	Ahmad	N,	Conci	N	(2019)	Natural	disasters	detection	
in	social	media	and	satellite	imagery:	a	survey.	Multimedia	Tools	Appl	78(22):31267-31302
Saloot	MA,	Idris	N,	Aw	A	(2014)	Noisy	text	normalization	using	an	enhanced	language	model.	In:	Proceedings	of	the	international	conference	on	artificial	intelligence	and	pattern	recognition,	pp	111-122.	
SDIWC	Kuala	Lumpur,	Malaysia
Sanoussi	MSA,	Xiaohua	C,	Agordzo	GK,	Guindo	ML,	Al	Omari	AM,	Issa	BM	(2022)	Detection	of	hate	
speech	texts	using	machine	learning	algorithm.	In:	2022	IEEE	12th	annual	computing	and	communication	workshop	and	conference	(CCWC),	pp	0266-0273.	IEEE
Saputra	L,	Marlina	L	(2019)	An	analysis	of	slang	words	used	by	instagram	account	plesbol.	English	Language	and	Literature	8(3)
Sasu	L	(2011)	A	probabilistic	model	for	spelling	correction.	Bulletin	of	the	Transilvania	University	of	Brasov.	
Series	III:	Math	Comput	Sci	4(2):141
Shah	K,	Melo	G	(2020)	Correcting	the	autocorrect:	context-aware	typographical	error	correction	via	training	
data	augmentation.	arXiv	preprint	arXiv:2005.01158
Sharma	S,	Srinivas	P,	Balabantaray	RC	(2015)	Text	normalization	of	code	mix	and	sentiment	analysis.	In:	
2015	International	conference	on	advances	in	computing,	communications	and	informatics	(ICACCI),	
pp	1468-1473.	IEEE
Sikdar	A,	Chatterjee	N	(2020)	An	improved	Bayesian	trie	based	model	for	sms	text	normalization.	arXiv	
preprint arXiv:2008.01297
Silverman	K,	Naik	D,	Bellegarda	J,	Lenzo	K	(2013)	Systems	and	methods	for	text	normalization	for	text	to	
speech	synthesis.	Google	Patents.	US	Patent	8,355,919
Singh	J,	Gupta	V	(2019)	A	novel	unsupervised	corpus-based	stemming	technique	using	lexicon	and	corpus	
statistics.	Knowl-Based	Syst	180:147-162
Singh	A,	Kaur	M	(2019)	Content-based	cybercrime	detection:	a	concise	review.	Int	J	Innov	Technol	Explor	
Eng	8:1193-1207
Sosamphan	P,	Liesaputra	V,	Yongchareon	DS,	Mohaghegh	DM	(2016)	Evaluation	of	statistical	text	normalisation	techniques	for	twitter
1 3
Page 47 of 48 89

---


<!-- PAGE 48 -->

J. Khan et al.
Stamatatos	E	(2009)	A	survey	of	modern	authorship	attribution	methods.	J	Am	Soc	Inform	Sci	Technol	
60(3):538-556
Stone	PJ,	Dunphy	DC,	Smith	MS	(1966)	The	general	inquirer:	a	computer	approach	to	content	analysis
Sun	S,	Luo	C,	Chen	J	(2017)	A	review	of	natural	language	processing	techniques	for	opinion	mining	systems.	
Information	fusion	36:10-25
Symeonidis	S,	Effrosynidis	D,	Arampatzis	A	(2018)	A	comparative	evaluation	of	pre-processing	techniques	
and	their	interactions	for	twitter	sentiment	analysis.	Expert	Syst	Appl	110:298-310
Tan	SS	(2020)	Automatic	lexicon	construction	for	domain-specific	sentiment	analysis:	a	frame-based	
approach
Tao	J,	Zhou	L	(2020)	A	weakly	supervised	wordnet-guided	deep	learning	approach	to	extracting	aspect	terms	
from	online	reviews.	ACM	Trans	Manage	Inform	Syst	(TMIS)	11(3):1-22
Tessore	JP,	Esnaola	LM,	Russo	CC,	Baldassarri	S	(2019)	Comparative	analysis	of	preprocessing	tasks	over	
social	media	texts	in	Spanish.	In:	Proceedings	of	the	XX	international	conference	on	human	computer	
interaction,	pp	1-8
Toska	M	(2020)	A	rule-based	normalization	system	for	Greek	noisy	user-generated	text
Verma	S,	Bhattacharyya	P	(2009)	Incorporating	semantic	knowledge	for	sentiment	analysis.	Proceedings	of	
ICON
Viegas	F,	Alvim	MS,	Canuto	S,	Rosa	T,	Gonçalves	MA,	Rocha	L	(2020)	Exploiting	semantic	relationships	
for	unsupervised	expansion	of	sentiment	lexicons.	Inf	Syst	94:101606
Wang	S,	Lv	G,	Mazumder	S,	Liu	B	(2020)	Detecting	domain	polarity-changes	of	words	in	a	sentiment	lexicon.	arXiv	preprint	arXiv:2004.14357
Wankhade	M,	Rao	ACS,	Kulkarni	C	(2022)	A	survey	on	sentiment	analysis	methods,	applications,	and	challenges.	Artif	Intell	Rev	55(7):5731-5780
Waseem	Z,	Hovy	D	(2016)	Hateful	symbols	or	hateful	people?	Predictive	features	for	hate	speech	detection	
on	twitter.	In:	Proceedings	of	the	NAACL	student	research	workshop,	pp	88-93
Wiemerslage	A,	Silfverberg	M,	Yang	C,	McCarthy	AD,	Nicolai	G,	Colunga	E,	Kann	K	(2022)	Morphological	
processing	of	low-resource	languages:	where	we	are	and	what's	next.	arXiv	preprint	arXiv:2203.08909
Wijeratne	S,	Balasuriya	L,	Sheth	A,	Doran	D	(2017)	Emojinet:	an	open	service	and	API	for	emoji	sense	
discovery.	In:	Eleventh	international	AAAI	conference	on	web	and	social	media
Wijeratne	S,	Saggion	H,	Kiciman	E,	Sheth	AP	(2020)	Emoji	understanding	and	applications	in	social	media:	
lay	of	the	land	and	special	issue	introduction.	ACM	New	York,	NY
Wu	S,	Fei	H,	Ji	D	(2020)	Aggressive	language	detection	with	joint	text	normalization	via	adversarial	multitask	learning.	In:	Natural	language	processing	and	Chinese	computing:	9th	CCF	international	conference,	NLPCC	2020,	Zhengzhou,	China,	October	14-18,	2020,	Proceedings,	Part	I	9,	pp	683-696.	
Springer
Xie	F,	Jiang	X-M	(2007)	Error	analysis	and	the	EFL	classroom	teaching.	Online	Submiss	4(9):10-14
Yun	JT,	Duff	BR,	Vargas	PT,	Sundaram	H,	Himelboim	I	(2020)	Computationally	analyzing	social	media	text	
for	topics:	a	primer	for	advertising	researchers.	J	Interact	Advert	20(1):47-59
Zachos	G,	Paraskevopoulou-Kollia	E-A,	Anagnostopoulos	I	(2018)	Social	media	use	in	higher	education:	a	
review.	Educ	Sci	8(4):194
Zaidan	OF,	Callison-Burch	C	(2014)	Arabic	dialect	identification.	Comput	Linguist	40(1):171-202
Zamir	MT,	Ayub	MA,	Khan	J,	Ikram	MJ,	Ahmad	N,	Ahmad	K	(2023)	Document	provenance	and	authentication	through	authorship	classification.	arXiv	preprint	arXiv:2303.01197
Zamir	MT,	Ayub	MA,	Gul	A,	Ahmad	N,	Ahmad	K	(2024)	Stylometry	analysis	of	multi-authored	documents	
for	authorship	and	author	style	change	detection.	arXiv	preprint	arXiv:2401.06752
Zampieri	M,	Malmasi	S,	Nakov	P,	Rosenthal	S,	Farra	N,	Kumar	R	(2019)	Semeval-2019	task	6:	Identifying	and	categorizing	offensive	language	in	social	media	(offenseval).	arXiv	preprint	arXiv:1903.08983
Zangerle	E,	Mayerl	M,	Potthast	M,	Stein	B	(2021)	Overview	of	the	style	change	detection	task	at	pan
Zhai	F,	Potdar	S,	Xiang	B,	Zhou	B	(2017)	Neural	models	for	sequence	chunking.	In:	Proceedings	of	the	
AAAI	conference	on	artificial	intelligence,	vol	31
Zhou	Y,	Jiang	J-Y,	Chang	K-W,	Wang	W	(2019)	Learning	to	discriminate	perturbations	for	blocking	adversarial	attacks	in	text	classification.	arXiv	preprint	arXiv:1909.03084
Publisher's Note	Springer	Nature	remains	neutral	with	regard	to	jurisdictional	claims	in	published	maps	and	
institutional	affiliations.				
1 3
89 Page 48 of 48
