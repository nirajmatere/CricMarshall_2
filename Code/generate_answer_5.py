import os
import asyncio

from llm_client import client

from dotenv import load_dotenv
load_dotenv()


async def generate_answer(query, context_text):
    # with open("../Context/context.log", "r", encoding="utf-8") as f:
    #     context_text = f.read()
    user_query = query
    response = client.chat.completions.create(
        model=os.environ["OLLAMA_MODEL"], 
        messages=[
            {"role": "system", "content": "You are a assistant that anmswers questions about cricket matches. You always verify that if there is a date provided in the question, then it must match with the date in the context, if date does not match, just say, 'there is no record of this match vailable to me, Sorry for the inconvenience.' You only answer the question and do not include any unnecessary information."},
            {"role": "user", "content": "Here is the context:\n" + context_text},
            {"role": "user", "content": "Now answer this question: " + user_query}
        ]
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content

async def main():
    query = ""
    context = ""
    await generate_answer(query, context)

if __name__ == "__main__":
    asyncio.run(main())