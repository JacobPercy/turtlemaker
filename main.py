import turtle
import cv2
import sys
import numpy as np
from skimage.segmentation import slic
from PIL import Image

min_size = 1000
max_size = 2000
num_segments = 2000
compactness = 10
fast_mode = True

def resize_image_to_range(image, min_size, max_size):
    h, w = image.shape[:2]
    max_dim = max(w, h)

    if max_dim > max_size:
        scale = max_size / max_dim
    elif max_dim < min_size:
        scale = min_size / max_dim
    else:
        scale = 1.0  # already within range

    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized

def extract_expanded_slic_polygons(image, num_segments=num_segments, compactness=compactness, expand=2):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    segments = slic(image_rgb, n_segments=num_segments, compactness=compactness, start_label=1)

    polygons = []
    avg_colors = []

    for label in np.unique(segments):
        mask = (segments == label).astype(np.uint8) * 255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*expand + 1, 2*expand + 1))
        expanded_mask = cv2.dilate(mask, kernel)

        contours, _ = cv2.findContours(expanded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue
        largest = max(contours, key=cv2.contourArea)

        epsilon = 1.5
        approx = cv2.approxPolyDP(largest, epsilon, True)
        polygon = [(int(pt[0][0]), int(pt[0][1])) for pt in approx]
        polygons.append(polygon)

        avg_color = cv2.mean(image, mask=mask.astype(np.uint8))[:3]
        avg_colors.append(avg_color)

    return polygons, avg_colors

def rgb_to_hex(color):
    b, g, r = [int(c) for c in color]
    return f"#{r:02x}{g:02x}{b:02x}"

def setup_turtle_canvas(width, height):
    screen = turtle.Screen()
    screen.setup(width, height)
    screen.title("Python Turtle Drawer")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.shape("turtle")
    t.speed(0)
    t.penup()
    if(fast_mode):
        turtle.tracer(0, 0)
    return t, screen

def draw_polygon(t, polygon, color, img_width, img_height):
    def to_turtle_coords(x, y):
        return x - img_width / 2, img_height / 2 - y
    
    x0, y0 = polygon[0]
    t.penup()
    t.goto(to_turtle_coords(x0, y0))
    t.pencolor(color)
    t.fillcolor(color)
    t.pendown()

    t.begin_fill()
    for x, y in polygon[1:]:
        t.goto(to_turtle_coords(x, y))
    t.goto(to_turtle_coords(x0, y0))
    t.end_fill()

    t.penup()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py path_to_image num_segments compactness")
        return

    path = sys.argv[1]

    image = cv2.imread(path)
    if image is None:
        print("Error: Image not found.")
        return

    image = resize_image_to_range(image, min_size, max_size)
    img_height, img_width = image.shape[:2]

    polygons, avg_colors = extract_expanded_slic_polygons(image, num_segments=num_segments, compactness=compactness)

    t, screen = setup_turtle_canvas(img_width, img_height)

    for polygon, color in zip(polygons, avg_colors):
        hex_color = rgb_to_hex(color)
        draw_polygon(t, polygon, hex_color, img_width, img_height)

    turtle.update()

    ps_path = "turtle_polygons.ps"
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=ps_path)

    png_path = "turtle_polygons.png"
    img = Image.open(ps_path)
    img.save(png_path, 'png')

    print(f"Drew {len(polygons)} polygons with turtle. Saved to {png_path}")

    turtle.done()

if __name__ == "__main__":
    main()
