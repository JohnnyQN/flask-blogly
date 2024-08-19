import pytest
from app import app, db, User, Post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///test_blogly"
    app.config['DEBUG_TB_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_homepage(client):
    """Test the homepage redirects to the list of users."""
    response = client.get('/')
    assert response.status_code == 302  # Check for redirect
    response = client.get(response.location)  # Follow the redirect
    assert b'Blogly &ndash; Users' in response.data  # Match the exact title from HTML

def test_user_creation(client):
    """Test creating a new user."""
    response = client.post('/users/new', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'profile_picture': 'http://example.com/image.png'
    }, follow_redirects=True)  # Follow redirect if needed
    assert b'John Doe' in response.data  # Assuming the user is displayed on the users list
