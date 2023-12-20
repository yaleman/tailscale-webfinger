import os
from fastapi.testclient import TestClient

from tailscale_webfinger import app


def test_main():
    os.environ["KANIDM_DOMAIN"] = "idp.example.com"
    os.environ["CLIENT_ID"] = "foobar"

    client = TestClient(app)

    response = client.get(
        "/.well-known/webfinger?rel=http://openid.net/specs/connect/1.0/issuer&resource=acct:foo@bar"
    )
    assert response.status_code == 200
    assert response.json() == {
        "subject": "acct:foo@bar",
        "links": [
            {
                "rel": "http://openid.net/specs/connect/1.0/issuer",
                "href": "https://idp.example.com/oauth2/openid/foobar/.well-known/openid-configuration",
            }
        ],
    }


def test_err():
    os.environ["KANIDM_DOMAIN"] = "idp.example.com"
    os.environ["CLIENT_ID"] = "foobarzot"

    client = TestClient(app)

    response = client.get("/.well-known/webfinger?")
    assert response.status_code == 400

    response = client.get("/.well-known/webfinger?rel=asdfasdf")
    assert response.status_code == 400
