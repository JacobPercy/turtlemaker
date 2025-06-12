# 🐢 TurtleMaker 🐢

![Turtle Drawing Demo](demo/Demo3.gif)

TurtleMaker uses Python’s turtle graphics module and opencv to convert any image into a polygon format that can be drawn on turtle cavas.
This pipeline uses:
- SLIC superpixel segmentation
- Polygon simplification

---

## Demo Video

[Watch the demo](demo/Demo1.mp4)

---

## Example Output

![Mountains](demo/mountains3.png)

---

## Running the Website Locally

```console

git clone https://github.com/JacobPercy/turtlemaker.git
cd turtlemaker
```

Then run

```console
cd tm
python app.py
```

Open your browser and go to:

http://127.0.0.1:5000

Upload an image to see it rendered in turtle graphics form, and get the generated code to recreate it.

---
