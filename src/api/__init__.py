from src.modules.sentence_embedding import SentenceEmbedding
from src.modules.text_extract import TextExtractor
from src.config import settings


EMBEDDING_MODEL = SentenceEmbedding(settings.EMBEDDING_MODEL_NAME, settings.DEVICE)
TEXT_EXTRACTOR = TextExtractor(settings.DEVICE, settings.PADDLEOCR.REC_MODEL_DIR, settings.PADDLEOCR.DET_MODEL_DIR, settings.PADDLEOCR.REC_CHAR_DICT_PATH)
