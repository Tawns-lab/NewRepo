# Architecture

## Core abstraction

The engine separates evidence into independent score channels:

1. **Phonological evidence** — how closely the observed phone sequence matches a lexical candidate.
2. **Contextual evidence** — whether supplied contextual tokens support the candidate.
3. **Prior evidence** — a caller-supplied lexical prior.

Keeping these channels separate is critical. A language model or embedding system may later replace the simple context scorer without modifying the phonological scorer.

## Candidate lifecycle

```text
Observed phones
    ↓ normalize
Normalized phone sequence
    ↓ compare
Candidate lexical entries
    ↓ score independently
phonology | context | prior
    ↓ weighted composition
Raw candidate score
    ↓ softmax
Confidence-ranked hypotheses
```

## Why phoneme-level reasoning?

A transcript is already a decision. Homophones demonstrate the problem immediately:

```text
/N AY T/
  ├── night
  └── knight
```

An ASR transcript may expose only one path. PRE keeps both paths available until other evidence can distinguish them.

## Extension interfaces

Natural next interfaces are:

- `Phonemizer`: text → phones
- `AcousticProvider`: audio → N-best phone sequences
- `ContextScorer`: candidate + context → score
- `ConfusionModel`: phone pair → substitution cost
- `ProvenanceRecorder`: transformation → immutable trace
- `HypothesisSink`: ranked hypotheses → downstream consumer

## Provenance direction

A mature engine should make a hypothesis traceable:

```text
input bytes / transcript
  ↓ provider identity + version
phone sequence
  ↓ normalization policy
normalized phones
  ↓ lexicon version
candidate set
  ↓ scorer identities + weights
ranked hypotheses
```

That is a roadmap requirement, not a feature claimed by v0.1.0.
