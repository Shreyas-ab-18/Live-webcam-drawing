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


import pytest
from draw import ColorTracker


@pytest.mark.parametrize("lower,upper", [
    ([1, 2], [3, 4]),
    ([100, 20, 30], [90, 200, 200]),
    ([-1, 0, 0], [10, 10, 10]),
    ([0, 0, 0], [10, 10, 256]),
])
def test_color_tracker_rejects_invalid_hsv_bounds(lower, upper):
    with pytest.raises(ValueError):
        ColorTracker(lower, upper)


def test_color_tracker_rejects_nonpositive_min_area():
    with pytest.raises(ValueError):
        ColorTracker([0, 0, 0], [255, 255, 255], min_area=0)


def test_color_tracker_rejects_non_bgr_frame():
    tracker = ColorTracker([0, 0, 0], [255, 255, 255])
    with pytest.raises(ValueError):
        tracker.locate(np.zeros((10, 10), dtype=np.uint8))
