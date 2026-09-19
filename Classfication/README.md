# Product Classification Prototype

This folder contains a starter pipeline for luxury retail product classification using Python, classical ML, semantic embeddings, and LLM fallback.

## Structure

- `data/raw/`: raw product description data
- `data/labeled/`: labeled training examples and evaluation data
- `src/`: Python scripts for preprocessing, training, inference, and LLM fallback
- `config/taxonomy.json`: sample taxonomy definitions
- `notebooks/`: optional exploratory notebooks

## Quick start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place raw description data in `data/raw/`.
3. Add labeled examples in `data/labeled/`.
4. Run the orchestrator under `src/`.

## Recommended flow

1. `src/preprocess.py`
2. `src/train_baseline.py`
3. `src/train_embeddings.py`
4. `src/infer.py`
5. `src/llm_fallback.py`

## Orchestrator usage

From the `Classfication` folder, run:

```bash
python src/run_pipeline.py preprocess
python src/run_pipeline.py train-baseline
python src/run_pipeline.py train-embeddings
python src/run_pipeline.py infer --input-text "Leather tote bag with gold hardware"
python src/run_pipeline.py llm --input-text "Leather tote bag with gold hardware"
```
