import asyncio
import os
from datetime import datetime

import nest_asyncio
import openai
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from apis.demo_service import generate_output
from helpers.db import db
from models.batch_upload_status import BatchUploadStatus

# set up OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

batch_upload_bp = Blueprint('batch_upload', __name__)

from firebase_admin import storage
import pandas as pd


def update_status_data_to_firebase_collection(docId, status, url="-"):
    doc_ref = db.collection('batch_upload_status').document(docId)
    now = datetime.now()
    doc_ref.update({"updated_at": now,
                    "status": status, "url": url})
    # TODO: send link to email to user


def upload_file_to_firebase_storage(filename, docId, json_data):
    # Setting up the blob
    file_name = filename.split(".")[0]
    now = datetime.now()
    bucket = storage.bucket('writegpt-cai.appspot.com')  # storage bucket
    blob = bucket.blob(file_name + "-output" + str(now) + ".csv")

    df = pd.DataFrame.from_dict(json_data)
    # Upload the blob from the content of the byte.
    blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')
    blob.make_public()
    url = blob.public_url
    print("generated file url", blob.public_url)
    print("Updating db status and url.......")
    update_status_data_to_firebase_collection(docId, "Success", url)


def save_status_data_to_firebase_collection(filename, user_id):
    doc_ref = db.collection('batch_upload_status').document()
    doc_id = doc_ref.id
    now = datetime.now()
    collection_bup = BatchUploadStatus(filename=filename, created_at=now, updated_at="",
                                       status="In Progress", url="-",
                                       user_id=user_id)
    collection_bup.save()
    return collection_bup.id


def reformat_knowledge_base(knowledge_base):
    formatted_knowledge_base = []

    knowledge_base = knowledge_base.replace("\r\n", "\n")
    knowledge_base_rows = knowledge_base.split("\n\n")

    for row in knowledge_base_rows:
        data = row.split(":")
        formatted_knowledge_base.append({"title": data[0], "description": data[1]})

    return formatted_knowledge_base


async def generate_output_and_write_csv(df, filename, doc_id):
    print("Running.......")
    data = []
    for index, row in df.iterrows():
        # get info from row and parse it to api
        json_data = {
            "url": row["url"],
            "sender_info": row["sender_info"],
            "recipient_info": row["recipient_info"],
            "word_count": row["word_count"],
        }

        if row["search_on_google"] != '' and row["search_on_google"] is not None:
            if not isinstance(row["search_on_google"], bool):
                search_on_google = row["search_on_google"].upper()
            else:
                search_on_google = row["search_on_google"]
            json_data["search_on_google"] = search_on_google

        if row["prompt"] is not None or row["prompt"] != "":
            json_data["prompt"] = row["prompt"]

        if row["template"] is not None or row["template"] != "":
            json_data["template"] = row["template"]

        if row["knowledge_base"] is not None or row["knowledge_base"] != "":
            json_data["knowledge_base"] = reformat_knowledge_base(row["knowledge_base"])

        output = generate_output(json_data)
        json_data["output"] = output
        data.append(json_data)
        print("generating another response from file.............")
    # TODO - add try catch
    print("uploading file to firebase.....")
    upload_file_to_firebase_storage(filename, doc_id, json_data)


@batch_upload_bp.route('/', methods=['POST'])
@jwt_required()
async def parse_csv_recieve_output():
    user_id = get_jwt_identity()
    file = request.files['batch_csvfile']
    if not file:
        return 'No file uploaded.', 400
    filename = file.filename

    if not filename.endswith('.csv'):
        return 'Invalid file type, please upload a CSV file.', 400
    df = pd.read_csv(file)
    doc_id = save_status_data_to_firebase_collection(filename, user_id)
    # print("Saved collection", doc_id)
    # run the scraper in an event loop
    # TODO start: fix asyncio it should run in background
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(generate_output_and_write_csv(df, filename, doc_id))
    loop.run_until_complete(task)
    # TODO end: fix asyncio it should run in background

    return {"status": "In Progress", "documentID": doc_id}
