import os
import time
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    background_image_url = os.environ.get("BACKGROUND_IMAGE_URL", "")
    group_name = os.environ.get("GROUP_NAME", "Group 18")
    group_slogan = os.environ.get("GROUP_SLOGAN", "Together, we got this!!!")
    cache_buster = int(time.time())  # helps bust browser cache
    return render_template(
        "index.html",
        group_name=group_name,
        group_slogan=group_slogan,
        background_image_url=background_image_url,
        cache_buster=cache_buster
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
