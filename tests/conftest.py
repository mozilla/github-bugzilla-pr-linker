import pytest
# there has to be a more correct way to structure this!
from app import app as app_module


@pytest.fixture
def app():
    return app_module.app
