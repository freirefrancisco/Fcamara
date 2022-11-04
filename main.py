import json
from fastapi import Depends, FastAPI
from typing import Union

import requests

from authentication import verify_token

app = FastAPI()
"""
uvicorn main:app --reload
"""
dado = requests.get("https://jsonplaceholder.typicode.com/users")
response = json.loads(dado.content)


@app.get("/")
async def root():
    return {"message": "Recuperando dados"}

@app.get("/names/websites", dependencies=[Depends(verify_token)])
def read_items():
    websites = list(map(lambda x: {'website': x.get('website')}, response))
    return {"websites": websites}


@app.get("/names/detail", dependencies=[Depends(verify_token)])
def read_items():
    users = list(map(lambda x:
                     {
                         'name': x.get('name'),
                         'email': x.get('email'),
                         'company': x.get('company').get('name')
                     }

                     , response))

    return {"users": users}

@app.get("/users/", dependencies=[Depends(verify_token)])
def read_items(name: Union[str, None] = None):
    users = []
    for i in response:
        if name in str(i.get('name')):
            users.append({
                'id': i.get('id'),
                'name': i.get('name')
            })

    return {"users": users}