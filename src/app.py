# import os
# import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_rfc7807 import middleware


# __dir__ = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

from src.api import routes

app = FastAPI(title='Unicloud - Automatic License Plate Recognition',
                redoc_url='/api-doc', 
                docs_url='/docs',
                openapi_url='/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
middleware.register(app)
app.include_router(routes.router, prefix='')
