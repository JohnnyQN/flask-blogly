import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Assuming you have app and db setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/test_db'
db = SQLAlchemy(app)

@pytest.fixture(scope='function')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables before each test
        yield client
        with app.app_context():
            db.drop_all()  # Drop tables after each test

def test_create_tag(test_client):
    response = test_client.post('/tags/new', data={'name': 'Technology'})
    assert b'Tag \'Technology\' added.' in response.data

def test_view_tag(test_client):
    tag = Tag(name='Science')
    db.session.add(tag)
    db.session.commit()
    response = test_client.get('/tags/1')  # Adjust URL as needed
    assert b'Science' in response.data

def test_edit_tag(test_client):
    tag = Tag(name='Health')
    db.session.add(tag)
    db.session.commit()
    response = test_client.post('/tags/edit/1', data={'name': 'Wellness'})
    assert b'Tag updated to Wellness' in response.data

def test_delete_tag(test_client):
    tag = Tag(name='Travel')
    db.session.add(tag)
    db.session.commit()
    response = test_client.post('/tags/delete/1')
    assert b'Tag deleted.' in response.data
