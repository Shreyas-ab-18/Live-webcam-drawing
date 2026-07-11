# Live Webcam Drawing

A real-time air-drawing application built with Python and OpenCV. It tracks a
colored marker (e.g. a blue bottle cap or sticky note) through the webcam feed
using HSV color-space thresholding and contour detection, and lets you draw
on-screen by moving the marker in front of the camera.

## How it works
- `ColorTracker` converts each frame to HSV and isolates pixels within a target
  color range, then finds the largest contour in that mask to locate the marker.
- `DrawingCanvas` accumulates line strokes between consecutive marker positions
  frame-to-frame and composites them back onto the live video feed.

## Run it
```bash
pip install -r requirements.txt
python draw.py
```

## Controls
| Key | Action |
|-----|--------|
| `1` / `2` / `3` | Switch draw color (blue / green / red) |
| `+` / `-` | Increase / decrease brush thickness |
| `c` | Clear the canvas |
| `q` | Quit |

## Notes
- Default tracking color is tuned for a blue object under normal indoor
  lighting. Adjust `lower_hsv` / `upper_hsv` in `draw.py` for your marker/lighting.
- Requires a connected webcam.
