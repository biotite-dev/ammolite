import pytest
import ammolite
from ammolite.startup import get_and_set_pymol_instance


def test_get_and_set_pymol_instance():
    """
    Test :func:`get_and_set_pymol_instance()` with a provided *PyMOL*
    instance.
    It is not possible to test this with another instance, since this
    would require duplicate *PyMOL* launching.
    """
    ammolite.reset()
    assert ammolite.pymol is get_and_set_pymol_instance(ammolite.pymol)


def test_get_and_set_pymol_instance_typecheck():
    """
    Expect an exception, if :func:`get_and_set_pymol_instance()` is
    given a non-*PyMOL* instance as parameter.
    """
    ammolite.reset()
    with pytest.raises(ammolite.DuplicatePyMOLException):
        assert get_and_set_pymol_instance(42)