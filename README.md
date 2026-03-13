# AIBOM

Generate EU AI Act Annex IV compliance documentation from your ML codebase in one command.

```bash
pip install aibom-cli
aibom scan ./your-project
```

## What it does

AIBOM scans your Python ML project and outputs a structured document listing:

- **Datasets** — HuggingFace datasets, TensorFlow datasets, PyTorch torchvision datasets
- **Models** — HuggingFace pretrained models, OpenAI models, Anthropic models
- **External APIs** — OpenAI, Anthropic, Google AI, Cohere, Replicate

This covers the dataset and model documentation requirements in EU AI Act Annex IV, Section 2.

## Installation

```bash
pip install aibom-cli
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
  "aibom_version": "0.1.0",
  "generated_at": "2026-03-13T13:51:17Z",
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
      "name": "gpt-4",
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

The EU AI Act requires providers of high-risk AI systems to maintain technical documentation including the datasets and models used. AIBOM generates the dataset and model inventory component of that documentation automatically.

Relevant articles: Annex IV Section 2, Article 11, Article 13.

Full enforcement for high-risk AI systems begins August 2027. Foundation model transparency rules are in effect since August 2025.

## Detection coverage

| Source | Detected via |
|--------|-------------|
| HuggingFace datasets | `load_dataset()` calls |
| HuggingFace models | `from_pretrained()` calls |
| OpenAI (new SDK) | `client.chat.completions.create()` |
| OpenAI (legacy) | `openai.ChatCompletion.create()` |
| Anthropic | `client.messages.create()` |
| TensorFlow datasets | `tfds.load()` calls |
| PyTorch torchvision | `torchvision.datasets.*` |

## License

MIT
