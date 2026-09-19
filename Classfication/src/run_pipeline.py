import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

import preprocess
import train_baseline
import train_embeddings
import infer
import llm_fallback


def run_preprocess(args):
    preprocess.main(["--input", args.input, "--output", args.output, "--text-column", args.text_column])


def run_train_baseline(args):
    train_baseline.main([
        "--input", args.input,
        "--label-column", args.label_column,
        "--text-column", args.text_column,
        "--model-path", args.model_path,
    ])


def run_train_embeddings(args):
    train_embeddings.main([
        "--input", args.input,
        "--output", args.output,
        "--text-column", args.text_column,
        "--model-name", args.model_name,
    ])


def run_infer(args):
    prediction, probabilities = infer.infer(args.model_path, args.input_text)
    print(f"Prediction: {prediction}")
    model_obj = infer.load_model(args.model_path)
    print("Probabilities:")
    for label, prob in zip(model_obj["model"].classes_, probabilities):
        print(f"  {label}: {prob:.4f}")


def run_llm(args):
    prompt = llm_fallback.build_prompt(args.input_text)
    print(llm_fallback.classify_with_llm(prompt, model=args.model))


def main():
    parser = argparse.ArgumentParser(description="Run the classification pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preprocess_parser = subparsers.add_parser("preprocess")
    preprocess_parser.add_argument("--input", default="../data/raw/shopmania.csv")
    preprocess_parser.add_argument("--output", default="../data/labeled/preprocessed.csv")
    preprocess_parser.add_argument("--text-column", default="description")
    preprocess_parser.set_defaults(func=run_preprocess)

    train_parser = subparsers.add_parser("train-baseline")
    train_parser.add_argument("--input", default="../data/labeled/preprocessed.csv")
    train_parser.add_argument("--label-column", default="category")
    train_parser.add_argument("--text-column", default="clean_text")
    train_parser.add_argument("--model-path", default="../models/baseline.joblib")
    train_parser.set_defaults(func=run_train_baseline)

    embeds_parser = subparsers.add_parser("train-embeddings")
    embeds_parser.add_argument("--input", default="../data/labeled/preprocessed.csv")
    embeds_parser.add_argument("--output", default="../models/embeddings.joblib")
    embeds_parser.add_argument("--text-column", default="clean_text")
    embeds_parser.add_argument("--model-name", default="all-MiniLM-L6-v2")
    embeds_parser.set_defaults(func=run_train_embeddings)

    infer_parser = subparsers.add_parser("infer")
    infer_parser.add_argument("--model-path", default="../models/baseline.joblib")
    infer_parser.add_argument("--input-text", required=True)
    infer_parser.set_defaults(func=run_infer)

    llm_parser = subparsers.add_parser("llm")
    llm_parser.add_argument("--input-text", required=True)
    llm_parser.add_argument("--model", default="gpt-4o-mini")
    llm_parser.set_defaults(func=run_llm)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
