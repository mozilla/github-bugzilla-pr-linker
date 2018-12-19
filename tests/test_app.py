from flask import url_for


def test_homepage(client):
    response = client.get(url_for(".homepage"))
    assert response.status_code == 200
