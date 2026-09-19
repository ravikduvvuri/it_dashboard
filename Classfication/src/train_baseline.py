import argparse
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def train_baseline(input_path: str, label_column: str, text_column: str, model_path: str):
    df = load_data(input_path)
    df = df.dropna(subset=[text_column, label_column])
    X_train, X_test, y_train, y_test = train_test_split(
        df[text_column], df[label_column], test_size=0.2, random_state=42, stratify=df[label_column]
    )

    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_tfidf, y_train)

    predictions = model.predict(X_test_tfidf)
    print(classification_report(y_test, predictions))

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"vectorizer": vectorizer, "model": model}, model_path)
    print(f"Saved baseline model to {model_path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Train a baseline product classification model")
    parser.add_argument("--input", default="../data/labeled/preprocessed.csv", help="Preprocessed CSV path")
    parser.add_argument("--label-column", default="category", help="Label column name")
    parser.add_argument("--text-column", default="clean_text", help="Text column name")
    parser.add_argument("--model-path", default="../models/baseline.joblib", help="Output model path")
    args = parser.parse_args(argv)

    train_baseline(args.input, args.label_column, args.text_column, args.model_path)


if __name__ == "__main__":
    main()
