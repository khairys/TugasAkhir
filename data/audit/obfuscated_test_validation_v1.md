# OFFICIAL OBFUSCATED TEST SET VALIDATION REPORT v1

**Stage 8: Final Experimental Lock - Official Obfuscated Test Verification**
- **Date**: `2026-10-07 15:49:20`
- **Frozen Normal Test Anchor**: `data/processed/test_normal_v1.csv` (4,116 records)
- **Obfuscated Test Directory**: `data/processed/obfuscated_test_v1/`
- **Conditions Evaluated**: 8 (O1-O4 x MILD/STRONG)
- **Decision Threshold**: >= 90.0% transformation success rate

---
## 1. Automated Integrity Assertions
| Assertion | Requirement | Status |
| --- | --- | --- |
| ASSERT 1 | All source_record_id exist in frozen normal test | PASS |
| ASSERT 2 | Original text matches frozen test byte-for-byte | PASS |
| ASSERT 3 | Canonical labels match frozen test exactly | PASS |
| ASSERT 4 | Zero duplicate source_record_id within conditions | PASS |
| ASSERT 5 | Zero leakage from Train or Validation partitions | PASS |
| ASSERT 6 | Canonical labels strictly preserved (0 changed) | PASS |
| ASSERT 7 | 100% Deterministic regeneration confirmed | PASS |
| ASSERT 8 | Normal data strictly matches unchanged status | PASS |
| ASSERT 9 | Valid family, severity, and seed metadata | PASS |
| ASSERT 10 | Main pool candidate v2 hash strictly preserved | PASS |

---
## 2. Transformation Success Rate & Condition Status
| Condition | Family | Severity | Total | Successful | No Target | Success Rate | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `O1_MILD` | `O1_CHAR_SUBSTITUTION` | `MILD` | 4,116 | 3,973 | 143 | 96.53% | **READY** |
| `O1_STRONG` | `O1_CHAR_SUBSTITUTION` | `STRONG` | 4,116 | 3,973 | 143 | 96.53% | **READY** |
| `O2_MILD` | `O2_CHAR_INSERT_DELETE` | `MILD` | 4,116 | 3,982 | 134 | 96.74% | **READY** |
| `O2_STRONG` | `O2_CHAR_INSERT_DELETE` | `STRONG` | 4,116 | 3,992 | 124 | 96.99% | **READY** |
| `O3_MILD` | `O3_WHITESPACE` | `MILD` | 4,116 | 3,985 | 131 | 96.82% | **READY** |
| `O3_STRONG` | `O3_WHITESPACE` | `STRONG` | 4,116 | 3,992 | 124 | 96.99% | **READY** |
| `O4_MILD` | `O4_UNICODE_ORTHOGRAPHIC` | `MILD` | 4,116 | 3,992 | 124 | 96.99% | **READY** |
| `O4_STRONG` | `O4_UNICODE_ORTHOGRAPHIC` | `STRONG` | 4,116 | 3,992 | 124 | 96.99% | **READY** |

---
## 3. Final Decision
### OBFUSCATED_TEST_STATUS: `READY` ✅
- All 8 conditions meet the >= 90.0% methodological threshold.
- Paired evaluation anchor is strictly verified against `data/processed/test_normal_v1.csv`.
- Official test sets are frozen and locked for Stage 9 model evaluation.