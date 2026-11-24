import numpy as np
from draw import DrawingCanvas


def test_clear_resets_pixels_and_previous_point():
    canvas = DrawingCanvas(40,30)
    canvas.stroke_to((2,2),(0,0,255),2)
    canvas.stroke_to((20,20),(0,0,255),2)
    canvas.clear()
    assert not np.any(canvas.canvas)
    assert canvas.prev_point is None


def test_missing_point_breaks_stroke():
    canvas = DrawingCanvas(40,30)
    canvas.stroke_to((2,2),(0,0,255),2)
    canvas.stroke_to(None,(0,0,255),2)
    assert canvas.prev_point is None
