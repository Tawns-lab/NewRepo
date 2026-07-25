# Contributing

Phonemic Reasoning Engine is intentionally modular.

Good first contributions:

- phoneme normalization adapters
- language-specific lexicons
- learned confusion matrices
- evaluation corpora
- improved segmentation
- context scorers
- provenance tracing
- benchmark tooling

## Design rule

Do not collapse uncertainty unless the public API makes that collapse visible.

A contribution that changes hypothesis ranking should expose enough information to explain why the rank changed.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

Open an issue before large architectural changes.
