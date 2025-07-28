from llm_client import client
import os

async def is_context_required(query):
    user_query = query
    response = client.chat.completions.create(
        model=os.environ["OLLAMA_MODEL"], 
        messages=[
            {"role": "system", "content": "You are intelligent cricket expert. You have to decide if you can answer the user question? if you cannot answer without any additional context, then just answer 'no', otherwise answer the user question. You only answer the question and do not include any unnecessary information."},
            {"role": "user", "content": "This is user question: " + user_query}
        ]
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content
