[![PyPI version](https://badge.fury.io/py/aibom-cli.svg)](https://badge.fury.io/py/aibom-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# AIBOM

Generate EU AI Act Annex IV compliance documentation from your ML codebase in one command.

**[getaibom.com](https://getaibom.com)**

```bash
pip install aibom-cli
aibom scan .
```

## What it does

AIBOM scans your Python ML project and outputs a structured document listing the AI models, datasets, and frameworks used in your project. This provides the core inventory required for the technical documentation under Annex IV of the EU AI Act.

The tool detects components from major AI providers and libraries, helping you automatically generate a baseline "AI Bill of Materials" to accelerate your compliance workflow.

## Installation

```bash
pip install aibom-cli==0.2.0
```

Requires Python 3.9+

## Usage

```bash
# Scan a project, output JSON (default)
aibom scan ./my-project

# Save to file
aibom scan ./my-project --output report.json

# Markdown output
aibom scan ./my-project --format markdown --output report.md
```

## Example output

```json
{
  "aibom_version": "0.2.0",
  "generated_at": "2026-03-14T05:55:00Z",
  "project_path": "./my-project",
  "datasets": [
    {
      "name": "squad",
      "source": "huggingface",
      "source_url": "https://huggingface.co/datasets/squad",
      "detected_in": "train.py:4"
    }
  ],
  "models": [
    {
      "name": "gpt-4o",
      "provider": "openai",
      "model_card_url": null,
      "detected_in": "inference.py:12"
    }
  ],
  "apis": [
    {
      "provider": "openai",
      "endpoint_pattern": "chat.completions.create",
      "detected_in": "inference.py:12"
    }
  ]
}
```

## What is the EU AI Act?

The EU AI Act requires providers of high-risk AI systems to maintain technical documentation detailing the system's components, including the datasets and models used. AIBOM generates the dataset and model inventory component of that documentation automatically.

Relevant articles: Annex IV Section 2, Article 11, Article 13.

## Detection Coverage

AIBOM v0.2.0 detects usage of the following frameworks and providers:

| Provider / Framework | Type |
|---|---|
| **HuggingFace** | Models & Datasets |
| **OpenAI** | Models & API Usage |
| **Anthropic** | Models & API Usage |
| **Google Vertex AI** | Models & API Usage |
| **Cohere** | Models & API Usage |
| **TensorFlow** | Datasets (`tfds`) |
| **PyTorch** | Datasets (`torchvision`) |
| **scikit-learn** | Models & Datasets |
| **LangChain** | Components |
| **LlamaIndex** | Components |


## License

MIT
