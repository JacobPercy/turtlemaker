from flask import Flask, request, render_template, send_file
import os
from main import main as run_turtle_script

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print(os.listdir(UPLOAD_FOLDER))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'image' not in request.files:
            return "No image uploaded", 400

        file = request.files["image"]
        if file.filename == "":
            return "Empty filename", 400

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        #delete other files in the upload folder
        for f in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(file_path) and f != file.filename:
                os.remove(file_path)

        file.save(img_path)
        code = run_turtle_script(headless=True, image_path=img_path)
        return render_template("result.html", code=code)

    return render_template("upload.html")




@app.route("/image")
def image():
    return send_file("turtle_polygons.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

