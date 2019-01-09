import hashlib
import hmac
import json
import os
import urllib.parse

import pytest
import responses
from flask import url_for


def test_homepage(client):
    response = client.get(url_for(".homepage"))
    assert response.status_code == 200


@responses.activate
@pytest.mark.usefixtures("config")
def test_postreceive_happy_path(client):
    responses.add(
        responses.GET,
        "https://bugzilla.example.com/rest/bug/12345678/comment",
        json={"bugs": {12_345_678: {"comments": []}}},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://bugzilla.example.com/rest/bug/12345678/attachment",
        json={"attachments": {"10001": "This is an attachment"}},
        status=201,
    )

    payload = {
        "action": "opened",
        "number": 123,
        "pull_request": {
            "url": "https://api.github.com/repos/mozilla-services/tecken/pulls/1294",
            "id": 228_342_167,
            "number": 1294,
            "state": "open",
            "title": "fixes bug 12345678 - Yada yada",
            "user": {"login": "renovate[bot]"},
            "_links": {
                "html": {"href": "https://github.com/mozilla-services/tecken/pull/1294"}
            },
        },
    }

    s = "payload=" + urllib.parse.quote_plus(json.dumps(payload))
    digest = hmac.new(
        os.environ["GITHUB_WEBHOOK_SECRET"].encode("utf-8"),
        s.encode("utf-8"),
        digestmod=hashlib.sha1,
    ).hexdigest()
    response = client.post(
        url_for(".postreceive"),
        # data=json.dumps(payload),
        data={"payload": json.dumps(payload)},
        headers={
            "X-Hub-Signature": f"sha1={digest}",
            "content-type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 201
