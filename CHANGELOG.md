# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-14

### Added
- PyTorch detection (`import torch`, `torch.hub.load()` with model name extraction)
- Keras detection (`import keras`, `from tensorflow import keras`)
- XGBoost detection (`import xgboost`)
- LightGBM detection (`import lightgbm`)

## [0.2.0] - 2026-03-14

### Added
- Scikit-learn detection
- LangChain detection
- LlamaIndex detection
- Google Vertex AI detection
- Cohere detection

## [0.1.0] - 2026-03-13

### Added
- HuggingFace detection (transformers, datasets)
- OpenAI API detection (new and legacy SDK)
- Anthropic API detection (new SDK)
- TensorFlow Datasets detection
- torchvision detection
- JSON and Markdown output formats
- --output flag to write to file
- --format flag (json/markdown)
