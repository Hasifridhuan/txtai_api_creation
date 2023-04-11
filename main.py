from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from txtai.embeddings import Embeddings

from pydantic import BaseModel
import warnings
import sqlite3
import uvicorn
import re

warnings.filterwarnings("ignore")

def extract_material_number(description):
    if description.startswith('5') and description[1:].isdigit() and len(description) == 8:
        return description
    else:
        return None

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


class EmbeddingsLoader:
    def __init__(self):
        self.embeddings = None
    
    def load(self):
        if not self.embeddings:
            self.embeddings = Embeddings()
            self.embeddings.load(path="final", cloud=None)

embeddings_loader = EmbeddingsLoader()

@app.on_event("startup")
async def startup_event():
    # Load the embeddings object lazily during startup
    embeddings_loader.load()
    
                        
@app.get("/ping")
async def ping() -> JSONResponse:
    return JSONResponse(content={"ping": "pong - 200 OK Response"})


@app.post("/dev/ProductDesc/")
async def read_data(data: product_description, request: Request, embed=Depends(lambda: embeddings_loader.embeddings),
                    current_user: str = Depends(get_current_user)):
    
    # Define a regular expression to match numbers starting with 5 and having 8 digits
    try:
        # start_time = time.time()
        if data.product_description[0].startswith('5') and data.product_description[0].isdigit() and len(data.product_description[0]) == 8:
            # Extract the number from the product description
            return {"data": {"result": data.product_description}}
        else:
            query = data.product_description
            results = embed.search(query, 1)
            print(results)
            material_index = results[0][0]  # get the index of the most similar material
            conn = sqlite3.connect('data/materials.db')
            c = conn.cursor()
            c.execute('SELECT text FROM materials WHERE id=?', (material_index,))
            material = c.fetchone()[0]  # fetch the material text
            # elapsed_time = time.time() - start_time
            # print(elapsed_time)
            conn.close()
            material = material.split(".")

            return {"data": {"result": material[0]}}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/dev/ProductDescProba/")
async def read_data(data: product_description, request: Request, embed=Depends(lambda: embeddings_loader.embeddings),
                    current_user: str = Depends(get_current_user)):
    
    material_list = []
    try:
         # start_time = time.time()
        if data.product_description[0].startswith('5') and data.product_description[0].isdigit() and len(data.product_description[0]) == 8:
            # Extract the number from the product description
            return {"data": {"result": data.product_description}}
        else:
            query = data.product_description
            # start_time = time.time()
            results = embed.search(query, 10)
            # elapsed_time = time.time() - start_time
            # print(f"Loaded model in {elapsed_time:.2f} seconds")

            conn = sqlite3.connect('data/materials.db')
            c = conn.cursor()
            for r in results:
                material_index = r[0]
                c.execute('SELECT text FROM materials WHERE id=?', (material_index,))
                material = c.fetchone()[0]
                material = material.split(".")[0]
                conf_percent = round(r[1]*100,2)
                material_list.append({"material": material, "conf_percent": conf_percent})
            conn.close()

            return {"data": {"result": material_list}}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5555, reload=False)