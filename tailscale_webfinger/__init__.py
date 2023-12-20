""" Tailscale webfinger responder

based on info here: https://www.authelia.com/integration/openid-connect/tailscale/
"""

import os
from typing import Any, Dict, Union
from fastapi import FastAPI, Request, Response


app = FastAPI()


KANDIM_FRONTEND = os.getenv("KANIDM_DOMAIN", "idp.example.com")
TAILSCALE_CLIENT_ID = os.getenv("CLIENT_ID", "tailscale")

OIDC_URL = f"https://{KANDIM_FRONTEND}/oauth2/openid/{TAILSCALE_CLIENT_ID}/.well-known/openid-configuration"


@app.get("/.well-known/webfinger")
async def webfinger(request: Request) -> Union[Response, Dict[str, Any]]:
    resource = request.query_params.get("resource")
    rel = request.query_params.get("rel")

    if rel is None or resource is None:
        return Response(
            status_code=400, content="Bad Request: either rel or resource were empty"
        )
    elif resource.split(":")[0] != "acct":
        return Response(
            status_code=400, content="Bad Request, resource must be an acct URI"
        )
    return {
        "subject": resource,
        "links": [
            {
                "rel": rel,
                "href": OIDC_URL,
            }
        ],
    }
