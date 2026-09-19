import argparse
import openai


def classify_with_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a product classification assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()


def build_prompt(text: str) -> str:
    return (
        "Classify the following luxury retail product description into one of the predefined categories: Handbags, Apparel, Footwear, "
        "Accessories, Jewelry, Fragrance, Watches. Provide only the category name.\n\n"
        f"Product description: {text}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send low-confidence classification cases to an LLM")
    parser.add_argument("--input-text", required=True, help="Input text to classify")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model name")
    args = parser.parse_args()

    prompt = build_prompt(args.input_text)
    print(classify_with_llm(prompt, model=args.model))
