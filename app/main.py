import sys
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
from typing import List
from evo2 import Evo2


evo2_model = Evo2(model_name="evo2_7b", local_path="/evo2/evo2_7b/evo2_7b.pt")

app = FastAPI()


# Simulated Bearer Token
BEARER_TOKEN = "581e45f1-bb33-4c49-8727-499fe2dd3c51"


# Verify Bearer Token
async def verify_bearer_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization.split(" ")[1]
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Bearer token")



class GenerateModel(BaseModel):
    prompt_seqs: List[str] = []
    n_tokens: int = 500
    temperature: float = 1.0
    top_k: int = 4
    top_p: float = 1.0


class ScoringModel(BaseModel):
    seqs: List[str] = []
    batch_size: int = 1


@app.post("/evo2_7b/generate")
async def generate(data: GenerateModel, authorization: str = Depends(verify_bearer_token)):
    output = evo2_model.generate(
        prompt_seqs=data.prompt_seqs,
        n_tokens=data.n_tokens,
        temperature=data.temperature,
        top_k=data.top_k,
        top_p=data.top_p,
    )
    sequences = output.sequences
    logprobs_mean = [float(x) for x in output.logprobs_mean]
    logits = [x.detach().cpu().numpy() for x in output.logits]
    response = {"sequences": sequences, "logprobs_mean": logprobs_mean, "logits": None}
    print(response)
    return response


@app.post("/evo2_7b/scoring")
async def scoring(data: ScoringModel, authorization: str = Depends(verify_bearer_token)):
    output = evo2_model.score_sequences(
        seqs=data.seqs,
        batch_size=data.batch_size,
    )
    output = [float(x) for x in output]
    response = {"scores": output, "seqs": data.seqs}
    return response

