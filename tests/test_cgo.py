import pytest
from ammolite import reset, draw_cgo, \
                     get_cylinder_cgo, get_cone_cgo, get_sphere_cgo

@pytest.mark.parametrize("cgo_func, param", [
    (get_cylinder_cgo, [(0,0,0), (1,1,1), 5, (1,1,1), (1,1,1)]),
    (get_cone_cgo, [(0,0,0), (1,1,1), 5, 10, (1,1,1), (1,1,1), True, True]),
    (get_sphere_cgo, [(0,0,0), 5, (1,1,1)]),
])
def test_draw_single_cgo(cgo_func, param):
    """
    Test drawing a single CGO.
    """
    reset()
    draw_cgo([cgo_func(*param)])


def test_draw_multiple_cgo():
    """
    Test drawing multiple CGOs.
    """
    reset()
    draw_cgo([
        get_sphere_cgo((0,0,0), 5, (1,1,1)),
        get_sphere_cgo((100,100,100), 10, (1,1,1))
    ])


@pytest.mark.parametrize("cgo_func, param", [
    (get_cylinder_cgo, [(0,0,0), (1,1,1), 5, (1,1), (1,1,1)]),
    (get_cylinder_cgo, [(0,0,0), (1,1,1), 5, (1,1,1), (1,1,1,0)]),
    (get_cylinder_cgo, [(0,0), (1,1,1), 5, (1,1,1), (1,1,1,0)]),
    (get_cylinder_cgo, [(0,0,0), (1,1,1,0), 5, (1,1,1), (1,1,1,0)]),
])
def test_draw_invalid_cgo(cgo_func, param):
    """
    Check if an exception is raised if an input value has the wrong
    length.
    """
    reset()
    with pytest.raises(IndexError):
        draw_cgo([cgo_func(*param)])