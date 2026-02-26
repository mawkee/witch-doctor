import pytest

from witch_doctor import WitchDoctor


@pytest.fixture(autouse=True)
def reset_witch_doctor_state():
    """Reset state before each test."""
    WitchDoctor._reset()
    yield
    WitchDoctor._reset()
