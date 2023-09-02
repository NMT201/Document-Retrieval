import json
import cv2
import numpy as np
import firebase_admin
import requests
from firebase_admin import auth, credentials, firestore, storage


def init_db(credential_path: str, storeage_bucket: str):
    cred = credentials.Certificate(credential_path)
    firebase_admin.initialize_app(cred, {'storageBucket': storeage_bucket})


def upload_file_storage(blob_name, data, content_type):
    storage_bucker = storage.bucket()
    blob = storage_bucker.blob(blob_name)
    blob.upload_from_string(data, content_type=content_type)


def download_file_storage(blob_name):
    storage_bucker = storage.bucket()
    blob = storage_bucker.blob(blob_name)
    return blob.download_as_bytes()


def put_item_firestore(doc_id: str, user_uid: str, doc_content: list, filename: str):
    db = firestore.client()
    doc_ref = db.collection("doc_info").document(doc_id)
    put_data = {
        "user_uid": user_uid,
        "doc_content": doc_content,
        "filename": filename
    }
    doc_ref.set(put_data)
    

def get_item_firestore():
    db = firestore.client()
    doc_ref = db.collection("doc_info")
    docs = doc_ref.stream()
    return docs


def sign_up(email: str, password: str):
    return auth.create_user(email=email, password=password)
    

def sign_in(user_email: str, password: str, api_key:str):
    payload = {
        "email": user_email,
        "password": password, 
        "returnSecureToken": True
    }
    payload = json.dumps(payload).encode()
    header = { "Content-Type": "application/json" }
    response = requests.post(url=f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}", data=payload, headers=header)
    return response


def get_uuid_by_email(user_email):
    return auth.get_user_by_email(user_email).uid


def get_document_image(doc_id):
    storage_bucker = storage.bucket()
    blob = storage_bucker.blob(f"image/{doc_id}.jpg")
    buffer = blob.download_as_bytes()
    img = np.frombuffer(buffer, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)  
    return img


def get_match_sentence(doc_id, index):
    for doc in get_item_firestore():
        if doc.id == doc_id:
            return doc.to_dict()["doc_content"][index]

if __name__ == "__main__":
    init_db("/home/tri/work/Document-Analysis/src/firebase_credential.json", 'total-method-364103.appspot.com')
    print(get_match_sentence("59465f30-681e-4be5-93a7-e21a8da8f65b", 0))