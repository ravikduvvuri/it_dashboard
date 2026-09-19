import argparse
import pandas as pd
from sentence_transformers import SentenceTransformer
import joblib
from pathlib import Path


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def build_embeddings(input_path: str, output_path: str, text_column: str = "clean_text", model_name: str = "all-MiniLM-L6-v2"):
    df = load_data(input_path)
    df = df.dropna(subset=[text_column])

    model = SentenceTransformer(model_name)
    embeddings = model.encode(df[text_column].tolist(), show_progress_bar=True)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model_name": model_name, "embeddings": embeddings, "texts": df[text_column].tolist()}, output_path)
    print(f"Saved embeddings to {output_path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build sentence embeddings for product descriptions")
    parser.add_argument("--input", default="../data/labeled/preprocessed.csv", help="Preprocessed CSV path")
    parser.add_argument("--output", default="../models/embeddings.joblib", help="Output embeddings path")
    parser.add_argument("--text-column", default="clean_text", help="Text column name")
    parser.add_argument("--model-name", default="all-MiniLM-L6-v2", help="SentenceTransformer model name")
    args = parser.parse_args(argv)

    build_embeddings(args.input, args.output, args.text_column, args.model_name)


if __name__ == "__main__":
    main()
