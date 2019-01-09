import pytest

# there has to be a more correct way to structure this!
from app import app as app_module

# NOTE! The app.py file reads os.environ with python-decouple.
# If you want to override any of those for the specific case of unit testing,
# set your environment variables in the pytest.ini file under 'env='


@pytest.fixture
def app():
    return app_module.app
