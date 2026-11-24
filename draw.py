"""Live webcam drawing using HSV color tracking and OpenCV."""
import cv2
import numpy as np


class ColorTracker:
    """Find the largest blob inside a configurable HSV range."""
    def __init__(self, lower_hsv, upper_hsv, min_area=800):
        self.lower_hsv = np.asarray(lower_hsv, dtype=np.uint8)
        self.upper_hsv = np.asarray(upper_hsv, dtype=np.uint8)
        self.min_area = min_area

    def locate(self, frame_bgr):
        if frame_bgr is None or frame_bgr.size == 0:
            raise ValueError("A non-empty BGR frame is required.")
        hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, mask
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < self.min_area:
            return None, mask
        (x, y), radius = cv2.minEnclosingCircle(largest)
        return (int(x), int(y), int(radius)), mask


class DrawingCanvas:
    """Canvas that stores strokes between frames."""
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Canvas dimensions must be positive.")
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_point = None

    def stroke_to(self, point, color, thickness):
        if point is None:
            self.prev_point = None
            return
        if self.prev_point is not None:
            cv2.line(self.canvas, self.prev_point, point, color, thickness)
        self.prev_point = point

    def clear(self):
        self.canvas[:] = 0
        self.prev_point = None

    def merge_onto(self, frame):
        if frame is None or frame.shape != self.canvas.shape:
            raise ValueError("Frame dimensions must match the drawing canvas.")
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        bg = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        return cv2.add(bg, fg)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError("Could not open webcam. Check camera index and permissions.")
    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        tracker = ColorTracker([100, 120, 70], [130, 255, 255])
        canvas = DrawingCanvas(width, height)
        colors = {ord("1"): (255, 0, 0), ord("2"): (0, 255, 0), ord("3"): (0, 0, 255)}
        draw_color, thickness = (0, 0, 255), 6
        print("Webcam Drawing started. Press q to quit, c to clear.")
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Camera frame could not be read; stopping.")
                break
            frame = cv2.flip(frame, 1)
            point, mask = tracker.locate(frame)
            center = (point[0], point[1]) if point else None
            if point:
                cv2.circle(frame, center, point[2], (0, 255, 255), 2)
            canvas.stroke_to(center, draw_color, thickness)
            cv2.imshow("Live Webcam Drawing", canvas.merge_onto(frame))
            cv2.imshow("Tracking Mask", mask)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                canvas.clear()
            elif key in colors:
                draw_color = colors[key]
            elif key in (ord("+"), ord("=")):
                thickness = min(thickness + 2, 40)
            elif key == ord("-"):
                thickness = max(thickness - 2, 2)
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
