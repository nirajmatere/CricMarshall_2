from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import asyncio
import os

from llm_client import client

index = faiss.read_index("../faiss_index/match_index.index")
metadata = np.load("../embeddings/metadata.npy", allow_pickle=True)
model = SentenceTransformer('all-miniLM-L6-v2')
folder_csv_info = "../dataset/csv_dataset/"
folder_txt_info = "../dataset/match_info_text/"

async def get_filenames_and_match_info(query, top_k=10):
    query_embedding = model.encode([query], normalize_embeddings=True)
    distances, indices = index.search(query_embedding, k=top_k)
    filenames = []
    match_info = []

    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        meta = metadata[idx]
        filename = meta['source_file']
        filenames.append(filename)
        file_path = os.path.join(folder_txt_info, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            match_info.append(f.read())

    return filenames, match_info

async def get_scorecards(filenames):
    scorecards = []
    for filename in filenames:
        scorecard_filename = os.path.join(folder_csv_info, filename.replace(".txt", "_scorecard.csv"))
        with open(scorecard_filename, 'r', encoding='utf-8') as f:
            scorecards.append(f.read())

    return scorecards

async def is_scorecard_required_for_LLM(query, match_info):
    user_query = query
    response = client.chat.completions.create(
        model=os.environ["OLLAMA_MODEL"], 
        messages=[
            {"role": "system", "content": "You are a decision maker. Your task is to decide if the provided context is enough to generate the answer? If not enough, then just answer 'no'. If the context is enough, then just answer the question without any additional dialogue. You only answer the question and do not include any unnecessary information."},
            {"role": "user", "content": "Here is the context:\n" + match_info},
            {"role": "user", "content": "And this is question: " + user_query}
        ]
    )

    with open("../Context/context.log", "w", encoding="utf-8") as f:
        f.write(match_info)

    # print(response.choices[0].message.content)
    return response.choices[0].message.content


async def search_index(query):
    filenames, match_info = await get_filenames_and_match_info(query, 3)

    answer_available = await is_scorecard_required_for_LLM(query, str(match_info))
    
    if 'no' in answer_available.lower():
        print("Answer Avalability decision: ", answer_available)
        scorecards = await get_scorecards(filenames)
        context = []
        for info, scorecard in zip(match_info, scorecards):
            match_information = {
                'match_info': info,
                'match_scorecard': scorecard,
            }
            context.append(match_information)

        with open("../Context/context.log", "w", encoding="utf-8") as f:
            f.write(str(context))

        return answer_available, context
    
    else:
        return answer_available, ""

async def main():
    query = input("Enter user query")
    await search_index(query)


if __name__ == "__main__":
    asyncio.run(main())