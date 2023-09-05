import os

from pydantic import BaseSettings

from src.utils.database import init_db

BASE_PATH = os.path.dirname(__file__)


class PaddleConfig(BaseSettings):
    REC_MODEL_DIR = os.path.abspath("./models/en_PP-OCRv3_rec_infer")
    REC_CHAR_DICT_PATH = os.path.abspath("./libs/PaddleOCR/ppocr/utils/en_dict.txt")
    DET_MODEL_DIR = os.path.abspath("./models/en_PP-OCRv3_det_infer/")


class Settings(BaseSettings):
    EMBEDDING_MODEL_NAME = 'paraphrase-MiniLM-L3-v2'
    DEVICE = "cpu"
    PADDLEOCR = PaddleConfig()
    DB_CREDENTIAL_PATH = os.path.abspath("./src/firebase_credential.json")
    STORAGE_BUCKET = "total-method-364103.appspot.com"
    FIREBASE_API_KEY = "AIzaSyCqEosMlb-kCXmDYj0l2pCFJZm0H7SJx00"
    API_HOST = "0.0.0.0"
    API_PORT = 5000
    
    
settings = Settings()
init_db(settings.DB_CREDENTIAL_PATH, settings.STORAGE_BUCKET)
