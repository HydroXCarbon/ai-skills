# TSV Status and Scoring Protocol

### TSV status protocol

| Outcome | TSV status | Git |
|---------|-----------|-----|
| Better score | `keep` (promote after comparison) | keep commit |
| Equal score | `discard` | reset |
| Worse score | `discard` | reset |
| Crash | `crash` | reset |

**Never retroactively change old rows.** Status is permanent once the next run starts.

### Score comparison rule

Always compare against the score of the **last `keep` row** in `results.tsv`, not the previous row. A discard that happened to score higher than baseline doesn't change the bar.
