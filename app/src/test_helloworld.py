import helloworld

def test_hello():
    response = helloworld.create_app().test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'<p>Hello, World!</p>'