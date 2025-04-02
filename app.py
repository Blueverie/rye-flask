from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")
	
@app.route("/test")
def test():
	return "11235"
	
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