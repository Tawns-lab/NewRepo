# Phonemic Reasoning Engine

An experimental OSS engine that reasons over **phonological structure before committing to lexical meaning**.

Traditional speech pipelines often collapse quickly from acoustic signal → transcript. PRE keeps ambiguity alive longer:

```text
speech / phoneme input
        ↓
phonemic normalization
        ↓
candidate generation
        ↓
phonological similarity
        ↓
context + semantic priors
        ↓
confidence-ranked interpretations
```

The goal is not to replace ASR. The goal is to expose and reason over ambiguity that ordinary transcription tends to hide: homophones, near-homophones, substitutions, accent variation, uncertain segmentation, and pronunciation drift.

## What works now

- Normalized phoneme sequences
- Exact homophone lookup
- Weighted phoneme edit distance
- Configurable confusable-phone pairs
- Context-aware lexical reranking
- Confidence-normalized hypotheses
- Basic utterance segmentation with dynamic programming
- CLI demo
- Unit tests
- Zero runtime dependencies

## Example

```python
from phonemic_reasoning_engine import PhonemicReasoningEngine, Lexicon

lexicon = Lexicon.from_entries([
    ("night", ["N", "AY", "T"], {"dark", "sleep", "evening"}, 0.9),
    ("knight", ["N", "AY", "T"], {"armor", "castle", "medieval"}, 0.6),
])

engine = PhonemicReasoningEngine(lexicon)
result = engine.reason(["N", "AY", "T"], context=["castle", "armor"])

for hypothesis in result.hypotheses:
    print(hypothesis.word, round(hypothesis.confidence, 3))
```

The phoneme sequence alone cannot distinguish `night` from `knight`. Context can.

## Design principles

1. **Ambiguity is data.** Do not erase alternatives prematurely.
2. **Phonological evidence is separate from semantic evidence.**
3. **Every score should be inspectable.**
4. **Providers are replaceable.** ASR, G2P, lexicons, embeddings, and language models should plug in rather than define the core.
5. **Reasoning outputs are hypotheses, not facts.**

## Architecture

```text
observed phoneme stream
        ↓
normalizer
        ↓
candidate generator
        ↓
phonological scorer
        ↓
contextual reranker
        ↓
ranked hypotheses + score decomposition
```

## Installation

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev]"
pytest
```

## CLI

```bash
pre-demo
```

## Scoring model

```text
raw_score(w) =
    phonology_weight * phonological_similarity
  + context_weight   * contextual_similarity
  + prior_weight     * lexical_prior
```

The engine converts raw scores to probabilities with softmax while retaining every score component for inspection.

## Roadmap

- ARPAbet ↔ IPA normalization
- Learned phoneme confusion matrices
- Accent/dialect profiles
- Prosodic scoring
- N-best ASR lattice ingestion
- Neural semantic reranking adapter
- Streaming hypothesis revision
- Cross-lingual phonological representations
- Evaluation harnesses
- Provenance objects for every hypothesis and transformation

## Non-goals

This project does not claim to infer hidden intent from voice characteristics. It reasons over explicit phonological alternatives and supplied context.

## License

MIT
