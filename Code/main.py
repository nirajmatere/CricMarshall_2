from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from input import marshall

app = FastAPI()

# Allow frontend (e.g., running on localhost or Vercel) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(data: QueryRequest):
    answer = await marshall(data.query)
    return {"answer": answer}
