.PHONY: all fetch preprocess train

all: fetch preprocess train

fetch:
	python3 scripts/fetch_data.py

preprocess: fetch
	python3 scripts/preprocess_validate.py

train: preprocess
	python3 scripts/train_evaluate.py
	
clean:
	rm -rf data/*.csv __pycache__/