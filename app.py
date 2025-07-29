import os
import boto3
from flask import Flask, render_template

app = Flask(__name__)

s3_image_url = os.environ.get("S3_IMAGE_URL")
group_name = os.environ.get("GROUP_NAME", "Your Group Name")
group_slogan = os.environ.get("GROUP_SLOGAN", "Your Slogan")
image_file = "static/background.jpg"

print(f"Background Image URL: {s3_image_url}")

def download_image_from_s3(url):
    # Ensure folder exists
    os.makedirs(os.path.dirname(image_file), exist_ok=True)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = url.split('/')[2].split('.')[0]
    key = '/'.join(url.split('/')[3:])
    s3.download_file(bucket_name, key, image_file)

if s3_image_url:
    download_image_from_s3(s3_image_url)

@app.route("/")
def index():
    return render_template("index.html", group_name=group_name, group_slogan=group_slogan)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
