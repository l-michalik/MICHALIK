# Movie Plot Embedding Generator

## Target
To create dense vector embeddings from movie plot summaries using a pre-trained NLP model.

## What It Does
- Loads a movie dataset from Hugging Face (`MongoDB/embedded_movies`)
- Filters out rows with missing plot summaries (`fullplot`)
- Removes the original embedding column (`plot_embedding`)
- Generates sentence embeddings using the `all-MiniLM-L6-v2` model from `sentence-transformers`
- Stores the embeddings in a new `embedding` column in the DataFrame
