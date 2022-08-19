from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


import add_data
import configs


app = FastAPI()

client = configs.client


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(add_data.router, prefix="/add_data")

@app.get("/")
async def get_routes():
    routes = {
        "Search API":"/search",
        "Add Data": "/add_data",
        "Swagger_Docs": "/docs"
    }
    return routes

@app.get("/search")
async def search(q: str, index : Optional[str] = None, page: Optional[int] = 1, per_page: Optional[int] = 10,):
    result = {}
    if not q:
            raise HTTPException(status_code=400, detail="Query not found")
    if index:
        if not client.indices.exists(index=index):
            raise HTTPException(status_code=400, detail="Index not found")
    try:
        query = {"from":(page-1)*per_page,"size":per_page,"query": {"query_string": {"query": q}}}
        if index:
            resp = client.search(body=query,index=index)
        else:
            resp = client.search(body=query)
        data = resp["hits"]["hits"]
        result['data'] = data
        result['meta'] = {'total':resp["hits"]["total"]["value"]}
        print(result["meta"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

