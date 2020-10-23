from flask import Flask, request, jsonify
import os, json, sys
from PIL import Image, ExifTags
from io import BytesIO
import requests
from google.cloud import storage
import datetime
app = Flask(__name__)

@app.route('/', methods = ['POST'])
def compress():
    if request.method == 'POST':
        url = request.form["url"]
        public_id = request.form["public_id"]
        image = open_image(url)
        buffer = BytesIO()
        image.save(buffer, "JPEG", quality=50)
        upload_blob(buffer, public_id)
        return {"size": buffer.getbuffer().nbytes}
    else:
        image_resized = None

    return send_file(image_resized, mimetype='image/gif')

def open_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

def upload_blob(buffer, public_id):
    bucket_name = "sumica_dev_image"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(public_id)
    buffer.seek(0)
    buffer_bytes = buffer.read()
    blob.upload_from_string(
        data=buffer_bytes,
        content_type='image/jpeg',
        client=storage_client
    )
    blob.make_public()

if __name__ == '__main__':
      app.run(host="0.0.0.0")
