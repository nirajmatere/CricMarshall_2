# RAG Approach

1. User input
2. Decide if LLM required more context to answer the question? If no --> answer.
3. Find the context (match info)
4. Decide if LLM required more context to answer the question? If no --> answer.
5. Find more context (scorecard)
6. Decide if LLM required more context to answer the question? If no --> answer.
7. Conclude: Not able to answer.

### Pre-requisites
- embeddings of important details of match-info
- embedding of input query
- find the scorecard of the match corrosponding to the similar embeddings using file name
- give the scorecard lines to the LLM along with question and system prompt.
- get answer
