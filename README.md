# Live Webcam Drawing

Draw in the air using a colored marker and webcam. OpenCV HSV thresholding and
contour detection track the marker and render strokes onto a persistent canvas.

## Requirements

- Python 3.10+
- Webcam
- Desktop session capable of opening OpenCV windows

## Setup and run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python draw.py
```

## Controls

| Key | Action |
|---|---|
| `1`, `2`, `3` | Select blue, green, or red |
| `+` / `-` | Increase / decrease brush thickness |
| `c` | Clear the canvas and reset the current stroke |
| `q` | Quit |

The default HSV range targets a blue object. Lighting, camera quality, and
marker shade affect tracking. Adjust the HSV bounds in `ColorTracker`.

## Tests

```bash
pip install pytest
pytest
```

The unit tests cover canvas clearing, stroke reset, HSV configuration validation, and invalid frame handling. Webcam integration requires a physical camera and must be tested on the target machine.
