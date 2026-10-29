# Distance Metric Comparison

## Dataset and query

Use the PolyBot scholarship document embeddings generated from
`sentence-transformers/all-MiniLM-L6-v2`.

Compare:
- Cosine similarity
- Euclidean distance
- Dot product

## Expected interpretation

### Cosine
Measures the angle between vectors and is commonly used for semantic
text retrieval. Because embeddings are normalized in this project,
cosine similarity is a natural choice.

### Euclidean
Measures straight-line distance between vectors. It can be useful,
but magnitude can influence distance when vectors are not normalized.

### Dot Product
Measures vector alignment and magnitude together. With normalized
embeddings, dot product is closely related to cosine similarity.

## Recommendation

Use **Cosine** for the PolyBot vector collection because the project
normalizes embeddings and the task is semantic document retrieval.

## Required evidence

Run:

```powershell
python src/test_query.py
```

with at least three scholarship-related queries and record the top
results and scores for Cosine, Euclidean, and Dot Product in the final
version of this report. Do not claim measured results until they have
actually been run on the final dataset.
