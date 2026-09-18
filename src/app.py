"""Production sentiment inference pipeline for WeLoveReviews."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

import pandas as pd
from transformers import pipeline

MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"
MODEL_REVISION = "8f6f4e3a8f70be4b65d3a4a8762b6d781cda240d"
DEFAULT_INPUT = Path("data/raw/reviews.csv")
DEFAULT_OUTPUT = Path("data/processed/reviews_with_sentiment.csv")


def sentiment_band(stars: int) -> str:
	if stars <= 2:
		return "Negative"
	if stars == 3:
		return "Neutral"
	return "Positive"


def _label_to_stars(label: str) -> int:
	match = re.search(r"([1-5])", str(label))
	if not match:
		raise ValueError(f"Unexpected model label: {label!r}")
	return int(match.group(1))


def _chunks(values: list[str], size: int) -> Iterable[list[str]]:
	for start in range(0, len(values), size):
		yield values[start : start + size]


def build_classifier(device: int = -1):
	"""Load the model once, before the per-review inference loop."""
	return pipeline(
		task="sentiment-analysis", model=MODEL_ID, tokenizer=MODEL_ID,
		revision=MODEL_REVISION, device=device,
	)


def enrich_reviews(reviews: pd.DataFrame, classifier, batch_size: int = 16) -> pd.DataFrame:
	required = {"review_id", "rating", "review_text"}
	missing = required.difference(reviews.columns)
	if missing:
		raise ValueError(f"Input CSV is missing required columns: {sorted(missing)}")
	result = reviews.copy()
	texts = result["review_text"].fillna("").astype(str).tolist()
	predictions = []
	for batch in _chunks(texts, batch_size):
		predictions.extend(classifier(batch, truncation=True, max_length=512))
	result["predicted_stars"] = [_label_to_stars(item["label"]) for item in predictions]
	result["sentiment_band"] = result["predicted_stars"].map(sentiment_band)
	return result


def run_pipeline(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT,
				 batch_size: int = 16, device: int = -1) -> pd.DataFrame:
	reviews = pd.read_csv(input_path)
	enriched = enrich_reviews(reviews, build_classifier(device), batch_size)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	enriched.to_csv(output_path, index=False)
	return enriched


def main() -> None:
	parser = argparse.ArgumentParser(description="Enrich reviews with pretrained sentiment.")
	parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
	parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
	parser.add_argument("--batch-size", type=int, default=16)
	parser.add_argument("--device", type=int, default=-1)
	args = parser.parse_args()
	if args.batch_size < 1:
		parser.error("--batch-size must be positive")
	enriched = run_pipeline(args.input, args.output, args.batch_size, args.device)
	print(f"Processed {len(enriched):,} reviews -> {args.output}")
	print(enriched["sentiment_band"].value_counts().reindex(
		["Positive", "Neutral", "Negative"], fill_value=0))


if __name__ == "__main__":
	main()
