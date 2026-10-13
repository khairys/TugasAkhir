# Final Research Results

## 1. Research objective and protocol

This study evaluates how robust Indonesian YouTube-comment classifiers are to controlled text obfuscation when detecting online-gambling promotion. The binary labels are `0 = Non-Promotion` and `1 = Promotion`.

The canonical comparison contains three model systems:

- **Linear SVM** with word-level TF-IDF features.
- **Char-CNN**, a character-level convolutional neural network.
- **IndoBERT**, the original fine-tuned `indobenchmark/indobert-base-p2` baseline.

The frozen normal test set contains 4,116 records, including 495 Promotion and 3,621 Non-Promotion examples. It is evaluated with eight paired obfuscation conditions: O1 character substitution, O2 character insertion/deletion, O3 whitespace manipulation, and O4 Unicode/orthographic manipulation, each at MILD and STRONG severities. Paired robustness metrics are calculated only for records with `changed == True`; the number of successfully changed pairs ranges from 3,973 to 3,992 per condition.

## 2. Normal-test baseline

| Model | Promotion F1 | Precision | Recall | Accuracy | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Linear SVM | 0.9428 | 0.9721 | 0.9152 | 0.9866 | 13 | 42 |
| **Char-CNN** | **0.9786** | **0.9877** | **0.9697** | **0.9949** | **6** | **15** |
| IndoBERT | 0.9605 | 0.9634 | 0.9576 | 0.9905 | 18 | 21 |

Source: `reports/stage10/test_normal_metrics.csv`.

## 3. Paired robustness over eight obfuscation conditions

The F1 values below use the successfully transformed pairs (`changed == True`). These are condition-specific paired-set F1 values, not metrics pooled over every record in the test set.

| Condition | Linear SVM | **Char-CNN** | IndoBERT |
|---|---:|---:|---:|
| O1 mild — character substitution | 0.9137 | **0.9766** | 0.9386 |
| O1 strong — character substitution | 0.8749 | **0.9608** | 0.8617 |
| O2 mild — character insertion/deletion | 0.9154 | **0.9792** | 0.9558 |
| O2 strong — character insertion/deletion | 0.8734 | **0.9785** | 0.9424 |
| O3 mild — whitespace manipulation | 0.9099 | **0.9782** | 0.9396 |
| O3 strong — whitespace manipulation | 0.8498 | **0.9806** | 0.9396 |
| O4 mild — Unicode homoglyphs | 0.9039 | **0.9776** | 0.7878 |
| O4 strong — Unicode homoglyphs | 0.8596 | **0.9786** | 0.6323 |

| Model | Mean paired F1 | Mean absolute F1 drop | Mean F1 retention |
|---|---:|---:|---:|
| **Char-CNN** | **0.9763** | **0.0037** | **99.62%** |
| Linear SVM | 0.8876 | 0.0569 | 93.98% |
| IndoBERT | 0.8771 | 0.0839 | 91.27% |

The means are unweighted arithmetic averages across the eight conditions; they are not one pooled F1 score.

### Finding 1 — Char-CNN is the strongest model on this test protocol

Char-CNN has the best normal-test Promotion F1 and wins all eight paired obfuscation conditions. Its mean paired F1 is 0.9763, with mean F1 retention of 99.62%. This is consistent with character-level representations handling the tested character substitutions, insertions/deletions, spacing changes, and Unicode substitutions comparatively well.

### Finding 2 — Unicode homoglyphs are the most severe failure family for IndoBERT

IndoBERT paired F1 falls to 0.6323 under O4 strong. The main observed failure mode is a large increase in false positives, rather than a similarly large loss of recall. This suggests that Unicode/orthographic perturbations are especially important to consider when interpreting IndoBERT robustness under the specific transformations used in this study.

### Finding 3 — The selected model lineup is now fixed

The original IndoBERT baseline is retained as the third model. A later training experiment had increased clean-text F1 by only about 0.08 percentage points, while its mean paired F1 and mean retention were lower and its results were worse on O1–O3 despite modest improvement on O4. This is descriptive evidence from one frozen test split, not a formal statistical comparison. The decision and supporting values are recorded in [the model-selection decision](MODEL_SELECTION_DECISION.md); the unused experiment's code and output artifacts are not part of the cleaned working repository.

## 4. Answers to the research questions

1. **How robust are the selected model systems to text obfuscation?** Robustness differs by model representation. Char-CNN is strongest in the tested conditions, Linear SVM shows moderate degradation, and IndoBERT is particularly sensitive to Unicode homoglyphs.
2. **Which obfuscation family is most damaging?** O4 Unicode/orthographic manipulation is the most damaging family for the selected IndoBERT baseline. Char-CNN remains comparatively stable across all four families.
3. **Which model has the best supported robustness in this experiment?** Char-CNN, based on the current frozen test suite and paired F1 values. This conclusion is limited to the selected models, specific data sources, transformation rules, and test distribution.

## 5. Limitations

- The evaluation uses one frozen split and one training seed. No formal paired significance test or multi-seed stability analysis was run.
- The four obfuscation families are controlled transformations and do not represent every possible real-world evasion strategy.
- The study compares complete model systems (representation, architecture, preprocessing, and training recipe), not architectures in isolation.
- These test results do not establish deployment performance or prevalence in the wider YouTube population.
- The train and validation CSV files tracked in this repository were observed not to match the hashes recorded in the official split manifest. The original frozen split snapshot must be recovered and verified before claiming end-to-end reproducibility.
- The IndoBERT model weight file is not tracked in Git. It must be supplied as a verified external artifact before inference can be reproduced from a clean checkout.

## 6. Final conclusion

On the tested frozen protocol, robustness is model- and perturbation-dependent. Char-CNN is markedly more robust than word-level TF-IDF Linear SVM and the IndoBERT subword model across the eight tested transformations. Unicode homoglyph obfuscation remains a critical failure mode for IndoBERT, especially because of false-positive inflation.

The standard future comparison consists of exactly **Linear SVM, Char-CNN, and IndoBERT**. The primary scientific analysis is documented, but the cleaned repository should not be described as fully reproducible until the split hashes, IndoBERT weight handoff, and runtime validation checks have been resolved.
