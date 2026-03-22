import pytest

@pytest.fixture
def collector():
    from tests import BooksCollector
    return BooksCollector()
