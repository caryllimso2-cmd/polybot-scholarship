# Model Customization Note — PEFT / LoRA / QLoRA

## Recommendation

For PolyBot, retrieval grounding is the first priority because scholarship
facts must come from current source documents. Fine-tuning should not be used
as a substitute for an updatable knowledge base.

## If fine-tuning is attempted

A parameter-efficient method such as LoRA or QLoRA could adapt an
instruction-tuned open-source model using a small set of curated examples.

Potential targets:
- scholarship-question response style
- refusal of unsupported questions
- source-aware formatting
- concise student-friendly explanations

## Why not fine-tune the facts?

Scholarship deadlines, benefits, and requirements can change. Storing these
facts in the retrievable knowledge base makes updates easier than retraining
the model.

## Memory constraints

QLoRA can reduce training memory requirements through quantization and
low-rank adapters. Any actual experiment should report the model, dataset,
GPU/CPU memory, training configuration, and evaluation results.

This project currently documents the rationale rather than claiming a
fine-tuning experiment that was not performed.
