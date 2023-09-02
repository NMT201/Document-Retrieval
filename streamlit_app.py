
import streamlit as st
import json
import requests
from src.utils.database import sign_in, get_uuid_by_email, get_item_firestore, get_document_image, get_match_sentence
from src.config import settings
from uuid import uuid4



def init_session_state():
    if "is_login" not in st.session_state:
        st.session_state["is_login"] = False
    if "submit_upload_key" not in st.session_state:
        st.session_state["submit_upload_key"] = uuid4
        
def login():
    if not st.session_state["is_login"]:
        with placeholder.form("login"):
            st.markdown("#### Enter your credentials")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            sign_in_status = sign_in(user_email=email, password=password, api_key=settings.FIREBASE_API_KEY)
            if sign_in_status:
                st.session_state["is_login"] = True
                st.session_state["user_uid"] = get_uuid_by_email(email)
            else:
                st.error(json.loads(sign_in_status.text)["error"]["message"].replace("_", " "))

def upload_document(user_uid, documents_files):
    for file in documents_files:
        firestore_items = get_item_firestore()
        exist_filenames = [i.to_dict()["filename"] for i in firestore_items]
        if file.name in exist_filenames:
            continue
        payload = {"document_file": file.read()}
        params = {
            "filename": file.name,
            "user_uid": user_uid
        }
        response = requests.put(f"http://{settings.API_HOST}:{settings.API_PORT}/upload", files=payload, params=params)
        
def retrieve_document(query):
    response = requests.get(f"http://{settings.API_HOST}:{settings.API_PORT}/retrive", params={"query": query})
    return response.json()

def main():
    upload_tab, retrive_tab = st.tabs(["Upload Document", "Retrive Document"])
    with upload_tab:
        file_upload = st.file_uploader("**Upload Documents Here**", accept_multiple_files = True, key=st.session_state["submit_upload_key"])
        submit_upload = st.button("Submit")
        if submit_upload:
            if file_upload:
                upload_document(st.session_state["user_uid"], file_upload)

    with retrive_tab:
        query_entry = st.text_input("Type your query :")
        submit_retrive = st.button("Submit", key = "submit_retrive")
        if submit_retrive:
            if query_entry:
                revelent_documents = retrieve_document(query_entry)
                if revelent_documents:
                    for doc_idx, doc in enumerate(revelent_documents):
                        st.title(f"Document #{doc_idx}")
                        st.text(f"Score : {doc['score']}")
                        st.text(f'Match sentence found in document : "{get_match_sentence(doc["doc_id"], doc["match_sentence_index"])}"')
                        st.text("Document image")
                        st.image(get_document_image(doc["doc_id"]))
                        
                        

if __name__ == "__main__":
    placeholder = st.empty()
    init_session_state()
    login()
    if st.session_state["is_login"]:
        placeholder.empty()
        main()