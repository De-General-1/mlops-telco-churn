.PHONY: all fetch preprocess train

all: fetch preprocess train

fetch:
	python scripts/fetch_data.py

preprocess: fetch
	python scripts/preprocess_validate.py

train: preprocess
	python scripts/train_evaluate.py
