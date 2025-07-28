from search_index_4 import search_index
from generate_answer_5 import generate_answer
from is_context_required import is_context_required
import asyncio

async def marshall(query):
    # query = input("Enter your query: ")
    answer = ''
    can_answer_without_context = await is_context_required(query)  
    if can_answer_without_context.lower() == 'no':
        print("Can answer without context: ", can_answer_without_context)
        answer_available, context = await search_index(query=query)

        if 'no' in answer_available.lower():
            answer = await generate_answer(query=query, context_text=str(context))
        else:
            answer = answer_available

    else:
        answer = can_answer_without_context

    print(answer)
    return answer

async def main():
    query = input("Enter your query: ")
    answer = await marshall(query)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
