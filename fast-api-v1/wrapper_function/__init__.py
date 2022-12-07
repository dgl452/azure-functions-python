import nest_asyncio
import base64
import azure.functions as func
import requests
import azure.durable_functions as df
from fastapi import FastAPI, Request
from typing import Union
from azure.functions import AsgiMiddleware


nest_asyncio.apply()

api = FastAPI()


def encode_starter(starter: str):
    starter_bytes = starter.encode("ascii")
    starter_base64_bytes = base64.b64encode(starter_bytes)
    return starter_base64_bytes.decode("ascii")


def decode_starter(encoded_starter: str):
    starter_bytes_enc = encoded_starter.encode("ascii")
    starter_bytes = base64.b64decode(starter_bytes_enc)
    return starter_bytes.decode("ascii")


@api.post("/export")
async def create_export(request: Request, starter: Union[str, None] = None):
    client = df.DurableOrchestrationClient(decode_starter(starter))
    instance_id = await client.start_new("orchestrator", None, None)
    return {
        "expoerter_id": instance_id,
    }


@api.get("/export")
async def get_exports(request: Request):
    instances = requests.get(
        f"http://localhost:7071/runtime/webhooks/durabletask/instances/"
    )
    return instances.json()


@api.get("/export/{id}/status")
async def get_export_status(request: Request, id: str):
    status = requests.get(
        f"http://localhost:7071/runtime/webhooks/durabletask/instances/{id}"
    )
    return status.json()


ASGI_MIDDLEWARE = AsgiMiddleware(api)


async def main(
    req: func.HttpRequest, context: func.Context, starter: str
) -> func.HttpResponse:
    req._HttpRequest__url = (
        f"{req._HttpRequest__url}?starter={ encode_starter(starter) }"
    )
    return ASGI_MIDDLEWARE.handle(req, context)
