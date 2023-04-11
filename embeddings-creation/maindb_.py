from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from txtai.embeddings import Embeddings

from pydantic import BaseModel
import pandas as pd
import warnings
import time
import json

warnings.filterwarnings("ignore")

app = FastAPI()

class product_description(BaseModel):
    product_description: List[str]

security = HTTPBearer()

# Authenticate the request based on a bearer token
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if token.scheme != 'Bearer':
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    if token.credentials != 'CKSOGhPm37FOxjrW056TwrqPwVGhI2Q3UPgdzPQ0GXI=':
        raise HTTPException(status_code=401, detail="Invalid token")
    return "Authenticated user"

@app.on_event("startup")
async def startup_event():
    global embeddings
    global df

    embeddings = Embeddings()

    start_time = time.time()
    embeddings.load(path="models/final", cloud=None)
    elapsed_time = time.time() - start_time

    print(f"Loaded model in {elapsed_time:.2f} seconds")

    with open("data/output_material.json", "r") as f:
        data = json.load(f)["material"]

    df = []
    i = 0
    for text in data:
        df.append((i, text, None))
        i = i + 1

@app.get("/ping")
async def ping() -> JSONResponse:
    return JSONResponse(content={"ping": "pong - 200 OK Response"})

@app.post("/dev/ProductDesc/")
async def read_data(data: product_description, request: Request, embed=Depends(lambda: embeddings),
                    df=Depends(lambda: df), current_user: str = Depends(get_current_user)):
    try:
        query = data.product_description
        # start_time = time.time()
        results = embeddings.search(query, 1)
        # elapsed_time = time.time() - start_time

        # print(f"Search result in {elapsed_time:.2f} seconds")
        # for r in results:
        #     print(f"Material: {df[r[0]][1]}")
        #     print(f"Similarity: {r[1]}")
        #     print()
        
        material = results[0]
        material = df[material[0]][1]

        return {"data": {"result": material}}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/dev/ProductDescProba/")
async def read_data(data: product_description, request: Request, embed=Depends(lambda: embeddings),
                    df=Depends(lambda: df), current_user: str = Depends(get_current_user)):
    
    material_list = []
    try:
        query = data.product_description
        # start_time = time.time()
        results = embeddings.search(query, 10)
        # elapsed_time = time.time() - start_time

        # print(f"Search result in {elapsed_time:.2f} seconds")
        for r in results:
            material = {"material":df[r[0]][1],
                        "conf_percent":round(r[1]*100,2)}
            material_list.append(material)

        return {"data": {"result": material_list}}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")