import re
import pandas as pd


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_raw(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def preprocess_dataframe(df: pd.DataFrame, text_column: str = "description") -> pd.DataFrame:
    df = df.copy()
    df[text_column] = df[text_column].fillna("").astype(str)
    df["clean_text"] = df[text_column].apply(clean_text)
    return df


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Preprocess raw product descriptions")
    parser.add_argument("--input", default="../data/raw/shopmania.csv", help="Raw CSV file path")
    parser.add_argument("--output", default="../data/labeled/preprocessed.csv", help="Output CSV file path")
    parser.add_argument("--text-column", default="description", help="Name of the text column")
    args = parser.parse_args(argv)

    raw_df = load_raw(args.input)
    processed_df = preprocess_dataframe(raw_df, text_column=args.text_column)
    processed_df.to_csv(args.output, index=False)
    print(f"Preprocessed {len(processed_df)} rows and saved to {args.output}")


if __name__ == "__main__":
    main()
