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


## CI/CD Integration

Automate your compliance documentation by running AIBOM in your CI/CD pipeline. This ensures your AI Bill of Materials is always up-to-date.

Here’s a quick example for GitHub Actions:

```yaml
name: AIBOM Scan

on:
  push:
    branches:
      - main

jobs:
  aibom-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install aibom-cli
      - run: aibom scan . --format markdown --output aibom-report.md
      - uses: actions/upload-artifact@v4
        with:
          name: aibom-report
          path: aibom-report.md
```

For GitLab CI and Jenkins examples, see the [CI/CD integration guide](docs/cicd.md).

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

## Developer FAQ

**Does AIBOM scan all Python files recursively?**

Yes. The `aibom scan .` command scans for Python files recursively within the specified directory.

**Does it work with virtual environments or requirements.txt?**

No. Version 0.2.0 performs an AST (Abstract Syntax Tree) scan on Python files directly. It does not analyze virtual environments or parse dependencies from `requirements.txt`.

**Can I scan a single file instead of a whole project?**

No, single-file scanning is not supported in v0.2.0. The tool currently operates on directories.

**What does the JSON output schema look like?**

The JSON output contains `aibom_version`, `generated_at`, `project_path`, and three arrays for discovered assets: `datasets`, `models`, and `apis`.

**Is this an official EU AI Act compliance tool?**

No. AIBOM is an open-source, community-driven project and is not an official tool for EU AI Act compliance.

**Can I contribute new framework detections?**

Yes, contributions are encouraged. See our `CONTRIBUTING.md` file for details on how to get started.
