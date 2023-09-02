import pickle
import cv2
import logging
from uuid import uuid4

from src.modules.sentence_embedding import SentenceEmbedding, get_most_similarity
from src.modules.text_extract import TextExtractor
from src.utils.database import upload_file_storage, init_db, download_file_storage, put_item_firestore, get_item_firestore

def save_document(embedding_model, text_extractor, document_image, doc_id, user_uid, filename):
    document_content = text_extractor.get_document_content(document_image)
    if document_content:
        document_embeddings, sentence_tokenize = embedding_model.get_embedding(document_content)
        put_item_firestore(user_uid=user_uid, doc_id=doc_id, doc_content=sentence_tokenize, filename=filename)
        pickled = pickle.dumps(document_embeddings)
        upload_file_storage(f"embedding/{doc_id}.pickle", pickled, 'application/pickle')
        image_string = cv2.imencode('.jpg', document_image)[1].tostring()
        upload_file_storage(f"image/{doc_id}.jpg", image_string, 'application/jpg')


def retrieve_document(embedding_model, query):
    firestore_items = get_item_firestore()
    list_filename = [i.id for i in firestore_items]
    embedding_data = []
    for filename in list_filename:
        embed = pickle.loads(download_file_storage(f"embedding/{filename}.pickle"))
        embedding_data.append(embed)
    
    result = get_most_similarity(query, embedding_model, embedding_data)
    relevent_documents = []
    
    for res in result:
        relevent_documents.append({
            "score": -res[0],
            "doc_id": list_filename[res[1]],
            "match_sentence_index": res[2]
        })
    
    return relevent_documents

if __name__ == "__main__":
    
    embedding_model = SentenceEmbedding('paraphrase-MiniLM-L3-v2', "cuda")
    text_extractor = TextExtractor("cpu", "/home/tri/work/Document-Analysis/models/en_PP-OCRv3_rec_infer", "/home/tri/work/Document-Analysis/models/en_PP-OCRv3_det_infer", "/home/tri/work/Document-Analysis/models/en_dict.txt")
    
    init_db("/home/tri/work/Document-Analysis/src/firebase_credential.json", "total-method-364103.appspot.com")
    # image = cv2.imread('/home/tri/work/Document-Analysis/src/test/DocBank_samples/2.tar_1801.00617.gz_idempotents_arxiv_4_ori.jpg')
    image = cv2.imread("/home/tri/work/Document-Analysis/src/test/DocBank_samples/7.tar_1601.03015.gz_crs_19_ori.jpg")
    # save_document_embedding(embedding_model, text_extractor, image, "list_ten1", "12359125982980")
    print(retrieve_document(embedding_model, "For homogeneous volatilities and drift"))
    