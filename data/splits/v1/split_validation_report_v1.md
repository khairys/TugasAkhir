# SPLIT VALIDATION REPORT v1

**Stage 8: Final Experimental Lock - Group-Aware Split Validation**
- **Date**: `2026-10-07 15:43:26`
- **Split Directory**: `data/splits/v1/`
- **Main Pool**: `data/processed/main_pool_candidate_v2.csv` (SHA-256: `0f07bc2e11a61804d5b46b2e6eb1e80c2f1ce3de4ce50cffaf5b67bfc1fde6ec`)
- **Normal Test Freeze**: `data/processed/test_normal_v1.csv` (SHA-256: `6d5a2c8b386193147013fb7a6002e4fa0375969f00d46a0cc86eea674e8c3780`)

---

## 1. Hard Assertions Status
| Assertion | Description | Status |
| --- | --- | --- |
| ASSERT 1 | Total rows across partitions == 41,152 | PASS |
| ASSERT 2 | Exact record_id disjointness across Train, Val, Test | PASS |
| ASSERT 3 | Strict leakage_group_id disjointness (Train ∩ Val = 0) | PASS |
| ASSERT 4 | Strict leakage_group_id disjointness (Train ∩ Test = 0, Val ∩ Test = 0) | PASS |
| ASSERT 5 | Valid canonical labels (both classes > 0 in all partitions) | PASS |
| ASSERT 6 | Complete isolation of label review queue records (0 leakage) | PASS |
| ASSERT 7 | Source main pool SHA-256 hash verified unchanged | PASS |
| ASSERT 8 | Unique and consistent (source_dataset, source_row_id) mappings | PASS |

---

## 2. Partition Summary
- **Train Set (v1)**: `32,920` rows (Promotion: `3,960`, Non-Promotion: `28,960`)
- **Validation Set (v1)**: `4,116` rows (Promotion: `495`, Non-Promotion: `3,621`)
- **Test Set (v1)**: `4,116` rows (Promotion: `495`, Non-Promotion: `3,621`)

---

## 3. Decision
**SPLIT_STATUS: VALIDATED_AND_FROZEN ✅**
