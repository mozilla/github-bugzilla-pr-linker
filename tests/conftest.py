import pytest
from app import app as app_module


@pytest.fixture
def app():
    return app_module.app
