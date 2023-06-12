import logging

from fastapi import FastAPI

app = FastAPI()
LOGGER = logging.getLogger("webhook")


@app.post("/mutate")
def mutate_request(request: dict):
    uid = request["request"]["uid"]
    object_in = request["request"]["object"]

    LOGGER.info(f'Applying mutate request for {object_in["kind"]}/{object_in["metadata"]["name"]}.')

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
