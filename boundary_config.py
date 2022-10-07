import numpy as np
import cv2
import os
from shapely.geometry import Polygon
from frame_preprocess import frame_resize


boundary_poly = [(339, 800), (233, 515), (299, 515), (958, 729), (890, 801), (886, 800)]
person_poly = [(343, 562), (306, 562), (306, 458), (343, 458)]
# ============================================================================
target_dim = 960
image_dir = "images"
image_name = "workplace_safety.jpg"
image_path = os.path.join(image_dir, image_name)
image = cv2.imread(image_path)
image = np.asarray(image)
image = frame_resize(image, target_dim, "yolov5")
overlay = image.copy()
h, w = image.shape[:2]
print(f"Height, Width: {h} x {w}")

canvas = (h, w)

boundary_color = (0, 0, 255)
worker_color = (0, 255, 0)

# ============================================================================

class PolygonDrawer(object):
    def __init__(self, window_name):
        self.window_name = window_name

        self.done = False 
        self.current = (0, 0) 
        self.points = [] 

    def on_mouse(self, event, x, y, buttons, user_param):

        if self.done: 
            return

        if event == cv2.EVENT_MOUSEMOVE:
            self.current = (x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we're done
            if self.points == []:
                self.points = boundary_poly
            print("Completing polygon with %d points." % len(self.points))
            print(f"Point List = {self.points}")
            work_boundary = Polygon(self.points)
            person_boundary = Polygon(person_poly)
            if person_boundary.intersects(work_boundary):
                print("Person is inside the work area")
            self.done = True

    def run(self):
        cv2.namedWindow(self.window_name)
        cv2.imshow(self.window_name, image)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while(not self.done):
            canvas = image
            if (len(self.points) > 0):
                cv2.polylines(canvas, np.array([self.points]), False, boundary_color, 1)
            cv2.imshow(self.window_name, canvas)
            if cv2.waitKey(50) == 27: # ESC hit
                self.done = True

        if (len(self.points) > 0):
            cv2.fillPoly(overlay, np.array([self.points]), boundary_color)
            cv2.fillPoly(overlay, np.array([person_poly]), worker_color)
            alpha = 0.3
            polygon_overlay = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
        cv2.imshow(self.window_name, polygon_overlay)
        # Waiting for the user to press any key
        cv2.waitKey(30000)

        cv2.destroyWindow(self.window_name)
        return polygon_overlay

if __name__ == "__main__":
    pd = PolygonDrawer("Polygon")
    final_img = pd.run()
    cv2.imwrite("polygon.png", final_img)
    print("Polygon = %s" % pd.points)