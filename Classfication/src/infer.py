import argparse
import pandas as pd
import joblib


def load_model(model_path: str):
    return joblib.load(model_path)


def infer(model_path: str, input_text: str, text_column: str = "clean_text"):
    pipeline = load_model(model_path)
    vectorizer = pipeline["vectorizer"]
    model = pipeline["model"]
    text_vector = vectorizer.transform([input_text])
    prediction = model.predict(text_vector)[0]
    probabilities = model.predict_proba(text_vector)[0]
    return prediction, probabilities


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infer product category from text")
    parser.add_argument("--model-path", default="../models/baseline.joblib", help="Baseline model path")
    parser.add_argument("--input-text", required=True, help="Input text to classify")
    args = parser.parse_args()

    prediction, probabilities = infer(args.model_path, args.input_text)
    pipeline = load_model(args.model_path)
    print(f"Prediction: {prediction}")
    print("Probabilities:")
    for label, prob in zip(pipeline["model"].classes_, probabilities):
        print(f"  {label}: {prob:.4f}")
