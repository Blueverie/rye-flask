from flask import Flask, request, jsonify
import boto3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


# Configure DigitalOcean Spaces
DO_SPACES_REGION = "nyc3"  # Change to your region
DO_SPACES_ENDPOINT = f"https://{DO_SPACES_REGION}.digitaloceanspaces.com"
DO_SPACES_BUCKET = "fsm"  # Replace with your Space name
DO_SPACES_KEY = "DO801GMF3HV9VD66EBYT"  # Replace with your Access Key
DO_SPACES_SECRET = "CI9o3cuUrgvGbxF8MQIkV6KRSWF+Iesy5kH+YqYh+vs"  # Replace with your Secret Key

s3_client = boto3.client(
    's3',
    region_name=DO_SPACES_REGION,
    endpoint_url=DO_SPACES_ENDPOINT,
    aws_access_key_id=DO_SPACES_KEY,
    aws_secret_access_key=DO_SPACES_SECRET
)

# Route for image upload
@app.route('/upload', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({"error": "No images part in the request"}), 400

    files = request.files.getlist('images')
    image_urls = []

    for file in files:
        filename = secure_filename(file.filename)
        s3_client.upload_fileobj(
            file,
            DO_SPACES_BUCKET,
            filename,
            ExtraArgs={'ACL': 'public-read'}
        )
        image_url = f"{DO_SPACES_ENDPOINT}/{DO_SPACES_BUCKET}/{filename}"
        image_urls.append(image_url)

    return jsonify({"image_urls": image_urls})

if __name__ == '__main__':
    app.run(debug=True)	