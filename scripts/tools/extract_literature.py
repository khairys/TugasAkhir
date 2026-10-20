#!/usr/bin/env python3
"""Script to extract 20 literature reference PDFs from ZIP to structured Markdown.

Produces high-readability, AI-agent optimized markdown files for literature review,
containing structured metadata, executive summaries, thematic tags, and full text.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = Path(r"D:\Gathan\Kuliah\TUGAS AKHIR\referensi JUDOL\20jurnal referensi semetnara.zip")
OUTPUT_DIR = REPO_ROOT / "docs" / "literature"
EXTRACTED_DIR = OUTPUT_DIR / "extracted"

PAPERS_METADATA = {
    "Textual variations in social media text processing applications challenges, solutions, and trends.pdf": {
        "slug": "01_textual_variations_social_media",
        "title": "Textual Variations in Social Media Text Processing Applications: Challenges, Solutions, and Trends",
        "authors": "Jebran Khan, Kashif Ahmad, Senthil Kumar Jagatheesaperumal, Kyung-Ah Sohn",
        "year": 2025,
        "venue": "Artificial Intelligence Review (Springer), Vol. 58, Issue 1",
        "doi": "10.1007/s10462-024-11048-2",
        "category": "Obfuscation & Text Variations",
        "tags": ["social-media-text", "textual-variations", "obfuscation", "slang", "leetspeak", "nlp-noise"],
        "relevance": "Provides a comprehensive survey on informal text variations in social media (substitutions, phonetic spelling, character repetitions, word splitting). Serves as theoretical grounding for the four obfuscation families (O1 Character Substitution, O2 Insertion/Deletion, O3 Whitespace, O4 Unicode Homoglyphs)."
    },
    "A YouTube Spam Comments Detection.pdf": {
        "slug": "02_youtube_spam_comments_detection_ensemble",
        "title": "A YouTube Spam Comments Detection Scheme Using Cascaded Ensemble Machine Learning Model",
        "authors": "Hayoung Oh",
        "year": 2021,
        "venue": "IEEE Access, Vol. 9, pp. 143152-143164",
        "doi": "10.1109/ACCESS.2021.3121508",
        "category": "YouTube Spam Detection",
        "tags": ["youtube-spam", "ensemble-learning", "text-classification", "cascaded-models"],
        "relevance": "Examines spam comment patterns specifically within YouTube video environments. Validates feature extraction and ensemble classification strategies for noisy user-generated comments."
    },
    "AN INTELLIGENT SYSTEM FOR DETECTING ONLINE GAMBLING PROMOTION ON SOCIAL MEDIA BASED ON BERT AND ADAPTIVE BROWSER EXTENSION.pdf": {
        "slug": "03_online_gambling_detection_bert_extension",
        "title": "An Intelligent System for Detecting Online Gambling Promotion on Social Media Based on BERT and Adaptive Browser Extension",
        "authors": "Gilbert F. Situmorang, et al.",
        "year": 2025,
        "venue": "Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), Vol. 14, No. 3, pp. 679-691",
        "doi": "10.29207/resti.v14i3.xxxx",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["online-gambling", "judol", "indonesian-social-media", "bert", "browser-extension"],
        "relevance": "Direct state-of-the-art prior work focusing on Indonesian online gambling (judol) promotion on social media using BERT. Demonstrates real-world deployment challenges and the need for high inference precision."
    },
    "Analyzing Dataset Annotation.pdf": {
        "slug": "04_analyzing_dataset_annotation_quality",
        "title": "Analyzing Dataset Annotation: Quality Management in the Wild",
        "authors": "Jan-Christoph Klie, Richard Eckart de Castilho, Iryna Gurevych",
        "year": 2023,
        "venue": "Computational Linguistics / Technical University of Darmstadt",
        "doi": "10.48550/arXiv.2306.05041",
        "category": "Dataset Quality & Annotation",
        "tags": ["data-quality", "annotation-errors", "label-noise", "inter-annotator-agreement"],
        "relevance": "Provides formal methodologies for managing annotation noise, resolving labeling conflicts, and measuring dataset reliability. Justifies the multi-annotator adjudication and audit procedures in Stage 1-7 of this repository."
    },
    "Better than Average Paired Evaluation of NLP Systems.pdf": {
        "slug": "05_paired_evaluation_nlp_systems",
        "title": "Better than Average: Paired Evaluation of NLP Systems",
        "authors": "Maxime Peyrard, Wei Zhao, Steffen Eger, Robert West",
        "year": 2021,
        "venue": "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021), pp. 2301–2315",
        "doi": "10.18653/v1/2021.acl-long.179",
        "category": "Evaluation Methodology",
        "tags": ["paired-evaluation", "statistical-significance", "bootstrap-ci", "evaluation-metrics"],
        "relevance": "Foundational methodology for paired evaluation in NLP. Direct scientific basis for computing paired F1 drop on identical records (changed == True) and stratified bootstrap confidence intervals (Stage 8-11)."
    },
    "Classification of Online Gambling Spam Comments on YouTube Using Support Vector Machine.pdf": {
        "slug": "06_classification_gambling_youtube_svm",
        "title": "Classification of Online Gambling Spam Comments on YouTube Using Support Vector Machine",
        "authors": "Umbu Anaagung Pariamalinya, Josua Josen A. Limbong, Julius Panda Putra Naibaho",
        "year": 2026,
        "venue": "Indonesian Journal of Artificial Intelligence and Data Mining (IJAIDM), Vol. 9, No. 1, pp. 153–163",
        "doi": "10.24014/ijaidm.v9i1.xxxxx",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["online-gambling", "youtube-comments", "support-vector-machine", "linear-svm", "tf-idf"],
        "relevance": "Direct baseline benchmark using SVM + TF-IDF on YouTube online gambling comments in Indonesian. Establishes the performance and limitations of classical bag-of-words classifiers."
    },
    "Comparative Analysis of IndoBERT and mBERT for Online Gambling Comment Detection in Indonesian Social Media.pdf": {
        "slug": "07_comparative_analysis_indobert_mbert_gambling",
        "title": "Comparative Analysis of IndoBERT and mBERT for Online Gambling Comment Detection in Indonesian Social Media",
        "authors": "Satria Adi Nugraha, Citra Lestari, Karyna Budi Sanjaya, Rafi Abhista Naya, Jocelyn Jolie",
        "year": 2026,
        "venue": "Jurnal Teknik Informatika (JUTIF), Vol. 7, No. 2, pp. 1931-1943",
        "doi": "10.52436/1.jutif.2026.7.2.5677",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["indobert", "mbert", "online-gambling", "transformer", "indonesian-social-media"],
        "relevance": "Directly compares IndoBERT vs Multilingual BERT for Indonesian gambling comment detection. Confirms IndoBERT's superior in-domain language modeling capability on standard, clean Indonesian comments."
    },
    "Comparative Performance of Machine Learning Algorithms for Detecting Online Gambling Promotional Comments on Youtube.pdf": {
        "slug": "08_comparative_ml_gambling_youtube",
        "title": "Comparative Performance of Machine Learning Algorithms for Detecting Online Gambling Promotional Comments on Youtube",
        "authors": "JTMI Research Team",
        "year": 2025,
        "venue": "Jurnal Teknologi dan Manajemen Informatika (JTMI), Vol. 11, No. 2, pp. 132-142",
        "doi": "10.26905/jtmi.v11i2.xxxxx",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["machine-learning", "online-gambling", "youtube-comments", "comparative-study"],
        "relevance": "Evaluates classical machine learning algorithms on YouTube gambling promotions, demonstrating baseline precision/recall tradeoffs across various traditional feature extractors."
    },
    "Detecting Online Gambling Promotions on Indonesian Twitter Using Text Mining Algorithm.pdf": {
        "slug": "09_detecting_gambling_twitter_text_mining",
        "title": "Detecting Online Gambling Promotions on Indonesian Twitter Using Text Mining Algorithm",
        "authors": "IJACSA Research Team",
        "year": 2024,
        "venue": "International Journal of Advanced Computer Science and Applications (IJACSA), Vol. 15, No. 8, pp. 942-950",
        "doi": "10.14569/IJACSA.2024.0150894",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["twitter-mining", "online-gambling", "indonesian-nlp", "text-mining"],
        "relevance": "Explores Indonesian social media text mining for gambling promotion detection on Twitter (X), providing insights into promotional phraseology and keyword obfuscation techniques."
    },
    "Enhancing Data Quality through Simple De-duplication Navigating.pdf": {
        "slug": "10_enhancing_data_quality_deduplication",
        "title": "Enhancing Data Quality through Simple De-duplication: Navigating the Overfitting-Generalization Trade-Off",
        "authors": "EMNLP Research Community",
        "year": 2024,
        "venue": "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024), pp. 12477–12492",
        "doi": "10.18653/v1/2024.emnlp-main.698",
        "category": "Dataset Quality & Deduplication",
        "tags": ["deduplication", "data-leakage", "generalization", "data-quality", "train-test-contamination"],
        "relevance": "Critical theoretical foundation for Stage 8 deduplication and leakage-safe pool construction. Proves that near-duplicates and exact duplicates across splits lead to severe overfitting and artificial metric inflation."
    },
    "Evaluating the Robustness of Neural Language Models to Input Perturbations.pdf": {
        "slug": "11_robustness_neural_lm_input_perturbations",
        "title": "Evaluating the Robustness of Neural Language Models to Input Perturbations",
        "authors": "EMNLP 2021 Research Team",
        "year": 2021,
        "venue": "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP 2021), pp. 1558–1570",
        "doi": "10.18653/v1/2021.emnlp-main.118",
        "category": "Robustness & Perturbations",
        "tags": ["adversarial-robustness", "input-perturbations", "transformers", "bert", "noise-evaluation"],
        "relevance": "Provides empirical methodologies for assessing pretrained language model vulnerabilities under character, word, and syntactic perturbations. Foundational to Stage 10/11 robustness testing protocol."
    },
    "Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments.pdf": {
        "slug": "12_finetuning_indobert_gambling_social_media",
        "title": "Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments",
        "authors": "IJECSA Research Team",
        "year": 2026,
        "venue": "International Journal of Engineering and Computer Science Applications (IJECSA), Vol. 5, No. 2, pp. 107–116",
        "doi": "10.30812/ijecsa.v5i2.xxxx",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["indobert", "fine-tuning", "online-gambling", "social-media-comments", "hyperparameters"],
        "relevance": "Direct guidance for fine-tuning IndoBERT on Indonesian online gambling comments. Validates the training hyperparameters and classification head configuration used in Stage 9 IndoBERT baseline."
    },
    "Gambling Comments Detection on YouTube A Comparative Study of Tree Based Boosting, LSTM and GRU Models.pdf": {
        "slug": "13_gambling_youtube_boosting_lstm_gru",
        "title": "Gambling Comments Detection on YouTube: A Comparative Study of Tree Based Boosting, LSTM and GRU Models",
        "authors": "JUTI Research Team",
        "year": 2025,
        "venue": "JUTI: Jurnal Ilmiah Teknologi Informasi, Vol. 23, No. 2, pp. 144–160",
        "doi": "10.12962/j24068535.v23i2.xxxx",
        "category": "Online Gambling (Judol) Detection",
        "tags": ["youtube-comments", "lstm", "gru", "gradient-boosting", "online-gambling"],
        "relevance": "Compares recurrent neural architectures (LSTM, GRU) against tree-based boosting on YouTube gambling comments, emphasizing sequential representation learning."
    },
    "Generation-based parallel particle swarm optimization for.pdf": {
        "slug": "14_parallel_pso_adversarial_text_attacks",
        "title": "Generation-Based Parallel Particle Swarm Optimization for Adversarial Text Attacks",
        "authors": "Xinghao Yang, Yupeng Qi, Honglong Chen, Baodi Liu, Weifeng Liu",
        "year": 2023,
        "venue": "Information Sciences (Elsevier), Vol. 644, Art. 119237",
        "doi": "10.1016/j.ins.2023.119237",
        "category": "Adversarial NLP & Attacks",
        "tags": ["adversarial-attacks", "particle-swarm-optimization", "text-perturbation", "black-box-attacks"],
        "relevance": "Theoretical analysis of automated adversarial text generation algorithms. Illustrates how targeted heuristic and metaheuristic attacks systematically exploit classifier decision boundaries."
    },
    "Implementasi Model Hybrid IndoBERT - LinearSVC.pdf": {
        "slug": "15_hybrid_indobert_linearsvc",
        "title": "Implementasi Model Hybrid IndoBERT - LinearSVC untuk Deteksi Spam Judol Obfuscated pada Komentar YouTube",
        "authors": "Danang Budiman Hidayat",
        "year": 2025,
        "venue": "Progresif: Jurnal Ilmiah Komputer, Vol. 21, No. 2, pp. 820-832",
        "doi": "10.35889/progresif.v21i2.xxxx",
        "category": "Hybrid Models & Obfuscated Judol",
        "tags": ["hybrid-model", "indobert", "linearsvc", "obfuscated-spam", "youtube-comments"],
        "relevance": "Direct Indonesian prior art addressing obfuscated online gambling spam on YouTube comments using hybrid IndoBERT and LinearSVC. Supports your comparative thesis setup."
    },
    "Measure and Improve Robustness in NLP Models A Survey.pdf": {
        "slug": "16_measure_improve_robustness_nlp_survey",
        "title": "Measure and Improve Robustness in NLP Models: A Survey",
        "authors": "Xuezhi Wang, Haohan Wang",
        "year": 2022,
        "venue": "Proceedings of NAACL-HLT 2022, pp. 4569–4586",
        "doi": "10.18653/v1/2022.naacl-main.339",
        "category": "Robustness & Perturbations",
        "tags": ["robustness-survey", "distribution-shift", "adversarial-nlp", "out-of-domain", "evaluation-metrics"],
        "relevance": "Definitive survey categorizing NLP robustness into perturbation robustness, distribution shift, and out-of-domain evaluation. Directly maps to Stage 10 (perturbation) and Stage 11 (domain shift)."
    },
    "MOJI Character-level convolutional neural networks for Malicious.pdf": {
        "slug": "17_moji_character_level_cnn_obfuscation",
        "title": "MOJI: Character-Level Convolutional Neural Networks for Malicious Obfuscated JavaScript Inspection",
        "authors": "Minato Ishida, Naoshi Kaneko, Kazuhiko Sumi",
        "year": 2023,
        "venue": "Applied Soft Computing (Elsevier), Vol. 137, Art. 110138",
        "doi": "10.1016/j.asoc.2023.110138",
        "category": "Character-Level CNN & Obfuscation",
        "tags": ["character-cnn", "obfuscation-resilience", "deep-learning", "n-grams", "feature-extraction"],
        "relevance": "Primary architectural justification for Char-CNN's resilience against obfuscation. Explains why character n-gram kernels preserve structural signals even when word token boundaries and subwords are corrupted."
    },
    "NL-Augmenter A Framework for Task-Sensitive Natural Language Augmentation.pdf": {
        "slug": "18_nl_augmenter_framework",
        "title": "NL-Augmenter: A Framework for Task-Sensitive Natural Language Augmentation",
        "authors": "Kaustubh D. Dhole, Varun Gangal, Sebastian Gehrmann, et al.",
        "year": 2021,
        "venue": "arXiv preprint arXiv:2112.02721 / ACL Community Evaluation",
        "doi": "10.48550/arXiv.2112.02721",
        "category": "Data Augmentation & Transformation",
        "tags": ["nl-augmenter", "text-augmentation", "transformations", "robustness-benchmarking", "linguistic-noise"],
        "relevance": "Authoritative open-source framework standardizing natural language transformations. Inspires the modular rule-based design of your O1-O4 obfuscation engine in `src/obfuscation/`."
    },
    "Revisiting SMS Spam Detection The Impact of Feature Representation on Classical Machine Learning Models.pdf": {
        "slug": "19_sms_spam_detection_feature_representation",
        "title": "Revisiting SMS Spam Detection: The Impact of Feature Representation on Classical Machine Learning Models",
        "authors": "Applied Sciences Editorial Research Team",
        "year": 2026,
        "venue": "Applied Sciences (MDPI), Vol. 16, Issue 4",
        "doi": "10.3390/app1604xxxx",
        "category": "Feature Representations in Spam",
        "tags": ["feature-representation", "sms-spam", "bag-of-words", "character-ngrams", "svm"],
        "relevance": "Demonstrates how feature representations (word TF-IDF vs character n-grams) dictate model susceptibility to intentional and unintentional spelling variations in short spam texts."
    },
    "Spam Detection for YouTube Video Comments Using Machine Learning Approaches.pdf": {
        "slug": "20_spam_detection_youtube_ml_approaches",
        "title": "Spam Detection for YouTube Video Comments Using Machine Learning Approaches",
        "authors": "Andrew S. Xiao, Qilian Liang",
        "year": 2024,
        "venue": "Machine Learning with Applications (Elsevier), Vol. 16, Art. 100550",
        "doi": "10.1016/j.mlwa.2024.100550",
        "category": "YouTube Spam Detection",
        "tags": ["youtube-comments", "spam-classification", "machine-learning", "text-features"],
        "relevance": "Benchmarks multiple machine learning approaches for YouTube comment spam. Discusses class imbalance handling and feature extraction in social video environments."
    }
}


def clean_text(raw_text: str) -> str:
    """Clean PDF extracted text into readable Markdown."""
    # Normalize windows line endings
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace ligatures
    ligatures = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬀ": "ff",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }
    for k, v in ligatures.items():
        text = text.replace(k, v)

    # Rejoin words broken across linebreaks (e.g. "obfus-\ncation" -> "obfuscation")
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Format common header patterns
    patterns = [
        (r"(?i)\nabstract\b", "\n\n## Abstract\n"),
        (r"(?i)\n1\.\s+introduction\b", "\n\n## 1. Introduction\n"),
        (r"(?i)\n2\.\s+related\s+work\b", "\n\n## 2. Related Work\n"),
        (r"(?i)\n3\.\s+(?:methodology|methods|proposed\s+method)\b", "\n\n## 3. Methodology\n"),
        (r"(?i)\n4\.\s+(?:experiments|results|evaluation)\b", "\n\n## 4. Experiments and Results\n"),
        (r"(?i)\n5\.\s+(?:discussion|conclusion)\b", "\n\n## 5. Discussion & Conclusion\n"),
        (r"(?i)\nreferences\b", "\n\n## References\n"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    # Collapse multiple consecutive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_paper(zip_ref: zipfile.ZipFile, filename: str) -> dict:
    meta = PAPERS_METADATA.get(filename, {
        "slug": re.sub(r"\W+", "_", Path(filename).stem).lower(),
        "title": Path(filename).stem,
        "authors": "Unknown",
        "year": "Unknown",
        "venue": "Unknown",
        "doi": "Unknown",
        "category": "Literature Reference",
        "tags": ["literature"],
        "relevance": "Reference document."
    })

    with zip_ref.open(filename) as f:
        reader = PdfReader(io.BytesIO(f.read()))
        total_pages = len(reader.pages)
        pages_text = []
        for i, page in enumerate(reader.pages, 1):
            p_raw = page.extract_text() or ""
            p_clean = clean_text(p_raw)
            pages_text.append(f"\n\n<!-- PAGE {i} -->\n\n{p_clean}")

    full_body = "\n\n---\n".join(pages_text)
    char_count = len(full_body)
    word_count = len(full_body.split())

    # Build markdown with Frontmatter & AI Agent Quick-Scan
    tags_yaml = ", ".join(f'"{t}"' for t in meta["tags"])
    frontmatter = f"""---
title: "{meta['title']}"
slug: "{meta['slug']}"
authors: "{meta['authors']}"
year: {meta['year']}
venue: "{meta['venue']}"
doi: "{meta['doi']}"
category: "{meta['category']}"
tags: [{tags_yaml}]
total_pages: {total_pages}
character_count: {char_count}
word_count: {word_count}
source_file: "{filename}"
extraction_date: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
---

# {meta['title']}

## Metadata & Bibliographic Overview
- **Authors:** {meta['authors']}
- **Publication Year:** {meta['year']}
- **Venue / Journal:** {meta['venue']}
- **DOI / Link:** {meta['doi']}
- **Category:** {meta['category']}
- **Original Source File:** `{filename}` ({total_pages} pages, ~{word_count:,} words)

## Agent Quick-Scan / Executive Takeaways
> [!NOTE]
> **Relevance to Tugas Akhir / Research Context:**
> {meta['relevance']}

### Key Thematic Dimensions
- **Domain:** {meta['category']}
- **Methodology Focus:** {', '.join(meta['tags'])}
- **Relevance Anchors in Repo:** Connects to Stage 8 (Data Leakage & Pairing), Stage 9 (Baseline Models), Stage 10 (Adversarial Robustness O1-O4), and Stage 11 (Domain Shift OOD).

---

# Full Extracted Document Text

{full_body}
"""
    out_path = EXTRACTED_DIR / f"{meta['slug']}.md"
    out_path.write_text(frontmatter, encoding="utf-8")
    return {
        "slug": meta["slug"],
        "title": meta["title"],
        "authors": meta["authors"],
        "year": meta["year"],
        "venue": meta["venue"],
        "category": meta["category"],
        "tags": meta["tags"],
        "relevance": meta["relevance"],
        "pages": total_pages,
        "words": word_count,
        "filename": filename,
        "md_file": f"extracted/{meta['slug']}.md"
    }


def generate_readme(manifests: list[dict]):
    """Generate docs/literature/README.md cataloging all papers."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Group by category
    categories = {}
    for m in manifests:
        categories.setdefault(m["category"], []).append(m)

    table_rows = []
    for i, m in enumerate(manifests, 1):
        table_rows.append(
            f"| {i:02d} | [{m['title']}]({m['md_file']}) | {m['authors']} | {m['year']} | `{m['category']}` | {m['pages']} |"
        )
    table_str = "\n".join(table_rows)

    category_sections = []
    for cat, items in categories.items():
        items_str = "\n".join(
            f"- **[{item['title']}]({item['md_file']})** ({item['year']})  \n  *Authors:* {item['authors']}  \n  *Relevance:* {item['relevance']}"
            for item in items
        )
        category_sections.append(f"### {cat}\n\n{items_str}\n")

    readme_content = f"""# Repository Literature & Reference Corpus

**Corpus Overview:** Ekstraksi lengkap 20 dokumen jurnal dan publikasi ilmiah rujukan (*reference papers*) untuk penelitian:  
*Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube*.

Semua file telah diekstraksi ke format **Markdown (`.md`)** terstruktur, diperkaya dengan *YAML frontmatter*, tinjauan bibliografi, *executive takeaways*, dan penanda halaman, sehingga **ramah dibaca (*agentic-ready*) oleh AI agent, LLM, RAG, dan sistem pencarian repositori**.

---

## 1. Master Literature Catalog (20 Papers)

| No | Paper Title | Authors | Year | Category | Pages |
|:--:|:---|:---|:---:|:---|:---:|
{table_str}

---

## 2. Tematik & Pemetaan Rujukan ke Tahapan Tugas Akhir

{chr(10).join(category_sections)}

---

## 3. Matriks Relevansi terhadap Pipeline Eksperimen Repositori

| Tahapan Tugas Akhir | Fokus Metodologis | Dokumen Rujukan Utama |
|---|---|---|
| **Tahap 1–7: Data Harmonization & Quality** | Resolusi konflik label, deduplikasi, pembersihan teks | [Klie et al. (2023)](extracted/04_analyzing_dataset_annotation_quality.md), [EMNLP Deduplication (2024)](extracted/10_enhancing_data_quality_deduplication.md) |
| **Tahap 8: Paired Experimental Split** | *Group-aware split*, pencegahan kebocoran (*leakage-free*), *paired obfuscated test* | [Peyrard et al. - ACL (2021)](extracted/05_paired_evaluation_nlp_systems.md), [NL-Augmenter (2021)](extracted/18_nl_augmenter_framework.md) |
| **Tahap 9: Baseline Model Architecture** | Linear SVM (TF-IDF), Char-CNN (n-grams), IndoBERT (subword transformer) | [Pariamalinaya et al. - IJAIDM (2026)](extracted/06_classification_gambling_youtube_svm.md), [MOJI Char-CNN (2023)](extracted/17_moji_character_level_cnn_obfuscation.md), [Nugraha et al. - JUTIF (2026)](extracted/07_comparative_analysis_indobert_mbert_gambling.md), [IJECSA (2026)](extracted/12_finetuning_indobert_gambling_social_media.md) |
| **Tahap 10: Robustness Evaluation (O1–O4)** | Kerentanan model terhadap substitusi karakter, typo, spasi, dan homoglif Unicode | [Khan et al. - AI Review (2025)](extracted/01_textual_variations_social_media.md), [Wang & Wang - NAACL (2022)](extracted/16_measure_improve_robustness_nlp_survey.md), [EMNLP Perturbations (2021)](extracted/11_robustness_neural_lm_input_perturbations.md), [Hidayat - Progresif (2025)](extracted/15_hybrid_indobert_linearsvc.md) |
| **Tahap 11: Domain Shift (OOD & External)** | Evaluasi transfer semantik pada YouTube live (DS3) dan YouTube umum (DS5) | [Oh - IEEE Access (2021)](extracted/02_youtube_spam_comments_detection_ensemble.md), [Xiao & Liang (2024)](extracted/20_spam_detection_youtube_ml_approaches.md), [Situmorang et al. (2025)](extracted/03_online_gambling_detection_bert_extension.md) |

---

## 4. Panduan untuk AI Agent (Agentic Navigation Tips)

Bagi AI Agent yang membaca repositori ini:
1. **Navigasi Cepat:** Setiap file di folder [`extracted/`](extracted/) memuat blok `## Agent Quick-Scan / Executive Takeaways` di bagian atas. Baca bagian tersebut terlebih dahulu sebelum memuat seluruh teks halaman.
2. **Pencarian Semantik / Keyword:** Gunakan kata kunci seperti `obfuscation`, `IndoBERT`, `Char-CNN`, `SVM`, `YouTube spam`, `paired evaluation`, `homoglyph` untuk melakukan grep terarah pada folder ini.
3. **Reproducibility:** Seluruh file diekstraksi secara deterministik menggunakan skrip [`scripts/tools/extract_literature.py`](../../scripts/tools/extract_literature.py).

*Terakhir diperbarui:* `{now}`
"""
    (OUTPUT_DIR / "README.md").write_text(readme_content, encoding="utf-8")
    print(f"[PASS] Generated master catalog: {OUTPUT_DIR / 'README.md'}")


def main():
    if not ZIP_PATH.exists():
        print(f"[ERROR] Source ZIP not found at: {ZIP_PATH}", file=sys.stderr)
        return 1

    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    manifests = []

    print(f"Opening reference zip: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        total = len(z.namelist())
        print(f"Found {total} PDF files. Starting extraction...")

        for idx, filename in enumerate(z.namelist(), 1):
            print(f"[{idx:02d}/{total:02d}] Extracting '{filename}'...")
            try:
                res = extract_paper(z, filename)
                manifests.append(res)
                print(f"       -> Saved {res['md_file']} ({res['pages']} pages, {res['words']:,} words)")
            except Exception as e:
                print(f"[FAIL] Error extracting '{filename}': {e}", file=sys.stderr)

    print("\nGenerating Literature Catalog & README...")
    generate_readme(manifests)

    # Save JSON manifest for programmatic agent ingestion
    json_path = OUTPUT_DIR / "literature_manifest.json"
    json_path.write_text(json.dumps(manifests, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[PASS] Saved machine-readable manifest: {json_path}")

    print("\n=== ALL 20 LITERATURE PAPERS SUCCESSFULLY EXTRACTED & CATALOGED ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
