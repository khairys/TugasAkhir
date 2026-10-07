# AUTHOR OVERLAP DIAGNOSTIC REPORT v1

**Stage 8: Group-Aware Split Diagnostic Analysis**
- **Date**: `2026-10-07 15:43:25`
- **Methodology Rule**: Diagnostic only (Author is NOT a hard grouping constraint due to non-equivalent metadata across source datasets).

---

## 1. Author Metadata Inventory
- **Train Distinct Authors**: `6,595`
- **Validation Distinct Authors**: `1,005`
- **Test Distinct Authors**: `975`

---

## 2. Cross-Partition Author Overlap Diagnostics
| Partition Pair | Overlapping Authors Count | Overlap % (relative to smaller partition) |
| --- | --- | --- |
| Train ∩ Validation | `287` | `28.56%` |
| Train ∩ Test | `287` | `29.44%` |
| Validation ∩ Test | `80` | `8.21%` |

---

## 3. Analysis & Methodological Note
- The primary hard constraint is `leakage_group_id` (which clusters exact duplicates, whitespace variants, normalized text, and near-duplicate templates with 100% strict disjointness).
- Author metadata varies widely across raw YouTube crawls (e.g. anonymous/random channel handles vs bot networks). Because bots deliberately use multiple distinct burner accounts to post identical templates, `leakage_group_id` provides superior protection against data leakage compared to author identifiers.
- The author overlap is documented here as an empirical diagnostic and does not violate the primary grouping rule.
