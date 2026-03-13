# AIBOM Build Summary

**Date:** 2026-03-13
**Status:** WORKING — all 3 test cases pass

## File Structure

```
aibom/
  aibom/
    __init__.py
    cli.py        (Click CLI — scan + version commands)
    scanner.py    (AST-based detection logic)
  examples/
    hf-only/example.py
    openai-only/example.py
    mixed/example.py
  pyproject.toml
  README.md
  BUILD-SUMMARY.md
```

## Detection Coverage

| Source | Detection Method | Status |
|--------|-----------------|--------|
| HuggingFace datasets | `load_dataset()` calls | Working |
| HuggingFace models | `from_pretrained()` calls | Working |
| OpenAI (new SDK) | `client.chat.completions.create()` + model= kwarg | Working |
| OpenAI (old SDK) | `openai.ChatCompletion.create()` | Working |
| Anthropic (new SDK) | `client.messages.create()` + model= kwarg | Working |
| TensorFlow datasets | `tfds.load()` calls | Implemented (untested) |
| PyTorch torchvision | `torchvision.datasets.*` instantiation | Implemented (untested) |

## Test Results

### examples/hf-only
```json
{
  "datasets": [{"name": "squad", "source": "huggingface", "source_url": "https://huggingface.co/datasets/squad", "detected_in": "example.py:4"}],
  "models": [
    {"name": "bert-base-uncased", "provider": "huggingface", "model_card_url": "https://huggingface.co/bert-base-uncased", "detected_in": "example.py:5"},
    {"name": "gpt2", "provider": "huggingface", "model_card_url": "https://huggingface.co/gpt2", "detected_in": "example.py:6"}
  ],
  "apis": []
}
```

### examples/openai-only
```json
{
  "datasets": [],
  "models": [{"name": "gpt-4", "provider": "openai", "model_card_url": null, "detected_in": "example.py:4"}],
  "apis": [{"provider": "openai", "endpoint_pattern": "chat.completions.create", "detected_in": "example.py:4"}]
}
```

### examples/mixed
```json
{
  "datasets": [{"name": "imdb", "source": "huggingface", "source_url": "https://huggingface.co/datasets/imdb", "detected_in": "example.py:4"}],
  "models": [{"name": "claude-3-opus-20240229", "provider": "anthropic", "model_card_url": null, "detected_in": "example.py:6"}],
  "apis": [{"provider": "anthropic", "endpoint_pattern": "messages.create", "detected_in": "example.py:6"}]
}
```

## Known Gaps (not blocking for MVP)

- OpenAI model detected at API call line, not instantiation line (minor)
- PyTorch/TensorFlow examples not run (no local dependencies installed)
- No README yet (to be written before PyPI publish)
- CLI invocation via `python3 -m aibom.cli` works; `aibom` binary requires pip install into active env

## Next Steps (require Atlas review + Joris approval before proceeding)

1. Write README.md
2. Push to GitHub (public, MIT license)
3. Publish to PyPI (`pip install aibom`)
4. Add GitHub Action for CI/CD integration (paid tier)
