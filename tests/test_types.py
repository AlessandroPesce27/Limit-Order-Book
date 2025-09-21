from typing import get_args
from lob.types import Side

def test_side_allowed_values():
    assert set(get_args(Side)) == {"B", "S"}