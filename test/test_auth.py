import pytest
from app import socketio, app
from config import config


@pytest.fixture(scope="session")
def api():
    app.config["TESTING"] = True
    socketio.test_client(app)

    api_client = app.test_client()
    socketio_client = socketio.test_client(app)
    return api_client, socketio_client


def test_valid_email(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": "rzbsys@unist.ac.kr"})
    assert res.status_code == 200


def test_not_valid_email(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": "not valid email"})
    assert res.status_code == 400, res.data


def test_not_unist_email(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": "rzbsys@notunist.ac.kr"})
    assert res.status_code == 400
