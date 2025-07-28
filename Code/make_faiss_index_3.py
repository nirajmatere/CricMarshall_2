import numpy as np
import faiss
import os

try:
    # Step 1: Load embeddings
    embedding_path = "../embeddings/embeddings.npy"
    embeddings = np.load(embedding_path)

    # Step 2: Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Step 3: Add embeddings to index
    index.add(embeddings)

    print(f"FAISS index created and {index.ntotal} vectors added.")

    # Step 4: Optional — save index to disk
    os.makedirs("../faiss_index/", exist_ok=True)
    faiss.write_index(index, "../faiss_index/match_index.index")
    print("Index saved to ../faiss_index/match_index.index")

except Exception as e:
    print("Error in making FAISS index:", e)
