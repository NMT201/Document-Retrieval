import os
from fastapi import APIRouter, HTTPException, Security, status, UploadFile, File
import logging
import cv2
import numpy as np
from src.document import save_document, retrieve_document
from src.api import EMBEDDING_MODEL, TEXT_EXTRACTOR
from uuid import uuid4

logger = logging.getLogger(__name__)
# logger.setLevel()
router = APIRouter()

@router.put('/upload')
async def upload(user_uid: str, filename: str, document_file: UploadFile = File(...)):
    if document_file:
        contents = await document_file.read()
        nparr = np.fromstring(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        save_document(document_image=image, embedding_model=EMBEDDING_MODEL,text_extractor=TEXT_EXTRACTOR, doc_id=str(uuid4()), user_uid=user_uid, filename=filename)


@router.get('/retrive')
async def retrive(query: str):
    if query.strip():
        relevent_document = retrieve_document(embedding_model=EMBEDDING_MODEL, query=query)
        return relevent_document
