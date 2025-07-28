import os
from sentence_transformers import SentenceTransformer
import numpy as np

preprocessed_folder = "../dataset/match_info_text/"
embedding_folder = "../embeddings/"

# Ensure the output folder exists
os.makedirs(embedding_folder, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")  # use correct casing

documents = []
metadata = []

for filename in os.listdir(preprocessed_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(preprocessed_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                full_text = f.read().strip()
                documents.append(full_text)
                metadata.append({"source_file": filename})
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Embed all documents at once
print(f"\nEmbedding {len(documents)} documents...")
embeddings = model.encode(documents, show_progress_bar=True, normalize_embeddings=True)

# Save embeddings + metadata
np.save(os.path.join(embedding_folder, "embeddings.npy"), embeddings)
np.save(os.path.join(embedding_folder, "metadata.npy"), metadata)

print("\nEmbedding completed and saved.")
