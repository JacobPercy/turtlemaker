from flask import Flask, request, render_template, send_file
import os
from main import main as run_turtle_script

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)

        turtle_code = run_turtle_script(headless=True, image_path=img_path)

        return render_template("result.html", turtle_code=turtle_code)

    return render_template("upload.html")


@app.route("/image")
def image():
    return send_file("turtle_polygons.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
