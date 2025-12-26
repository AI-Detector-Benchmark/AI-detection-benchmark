# Data Notes

`controlled_demo_essays_10.csv` includes an `intent` column that marks the
target aspect each short essay was designed to test. Use it to select the
corresponding prompt:

- `grammar` -> `v1.ai_refined_grammar`
- `vocabulary` -> `v1.ai_refined_vocabulary`
- `cohesion` -> `v1.ai_refined_cohesion`
- `syntax` -> `v1.ai_refined_syntax`
- `full_rewrite` -> `v1.ai_full_rewrite`

Other files in `data/` may be symlinks to local storage (e.g., Kaggle originals
or splits like `train.csv`, `test.csv`, `stratified_*.csv`, and `few_samples.csv`).
These are used for local development and may not resolve on other machines.

If you download the **Feedback Prize – English Language Learning** dataset from
Kaggle, keep the original `train.csv` under `data/` and follow the competition's
terms of use. Raw Kaggle essays are not redistributed in this repo.
