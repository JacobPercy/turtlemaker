import cv2
import numpy as np
from skimage.segmentation import slic
from skimage.color import label2rgb

def live_slic_with_contour_edges(camera_index=0, num_segments=200, compactness=5, 
                                  canny_thresh1=50, canny_thresh2=150):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame.")
            break

        frame = cv2.resize(frame, (640, 480))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        segments = slic(frame_rgb, n_segments=num_segments, compactness=compactness, start_label=1)
        segmented_img = label2rgb(segments, image=frame_rgb, kind='avg')
        segmented_bgr = cv2.cvtColor(segmented_img, cv2.COLOR_RGB2BGR).astype(np.uint8)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, canny_thresh1, canny_thresh2)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(segmented_bgr, contours, -1, (0, 0, 0), 1, lineType=cv2.LINE_AA)

        cv2.imshow('SLIC Superpixels with Black Contour Edges', segmented_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    live_slic_with_contour_edges()
