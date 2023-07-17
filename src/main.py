import os
import logging

from fastapi import FastAPI
import uvicorn

app = FastAPI()
LOGGER = logging.getLogger("webhook")


@app.post("/mutate")
def mutate_request(request: dict):
    uid = request["request"]["uid"]
    object_in = request["request"]["object"]

    LOGGER.info(f'Applying mutate request for {object_in["kind"]}')

    return {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,
            "allowed": True,
            "patchType": "JSONPatch",
            "status": {"message": "Okay it worked!"},
            "patch": [],
        },
    }

def run_server():
    port = os.getenv("SERVER_PORT", 80)
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    ssl_keyfile = os.getenv("SSL_KEYFILE")
    ssl_certifile = os.getenv("SSL_CERTIFILE")
    extra_args = {}
    if ssl_keyfile and ssl_certifile:
        extra_args = {
            "ssl_certfile": ssl_certifile,
            "ssl_keyfile": ssl_keyfile 
        }
    uvicorn.run(
        app=app,
        host=host,
        port=port,
        **extra_args
    )

if __name__ == "__main__":
    run_server()
