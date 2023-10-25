import pytest
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app(test_config=True)
    with app.app_context():
        db.create_all()  # You might want to use something like Flask-Migrate to handle database creation
        yield app
        db.session.remove()

    
@pytest.fixture()
def client(app):
    return app.test_client()

# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()