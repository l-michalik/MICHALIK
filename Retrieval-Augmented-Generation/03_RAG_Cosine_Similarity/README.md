# Cosine Similarity-Based Activity Recommender

## Description

This project uses cosine similarity to compare a user query with a list of predefined activity descriptions. It identifies the most relevant document from the corpus and then sends the query and selected document to a locally hosted LLaMA2 model (via Ollama API) to generate a short recommendation.

## Functionality

- Tokenizes input text and computes word frequency using `Counter`.
- Calculates cosine similarity between a query and each document in the corpus.
- Selects the document with the highest similarity score.
- Sends the query and selected document to a LLaMA2 model running at `http://localhost:11434` for generating a recommendation.
- Streams and prints the final response from the model.

## Usage

1. Define your input query, e.g.:
   ```python
   query = "What is the best way to spend a day in Poland?"
   ```

2. Run the script. It will:
   - Compute cosine similarities between the query and the corpus.
   - Print the most relevant activity.
   - Call the local LLaMA2 model with a prompt containing the activity and the user query.
   - Stream and display the AI-generated response.

3. Example output:
   ```
   Query: What is the best way to spend a day in Poland?
   Response: [Most similar activity from the corpus]
   [Generated recommendation from LLaMA2]
   ```

## Functions

### `cosine_similarity(query, document)`

Calculates cosine similarity between a query and a single document using term frequency.

### `return_response(query, corpus)`

Finds and returns the document from the corpus with the highest cosine similarity to the input query.