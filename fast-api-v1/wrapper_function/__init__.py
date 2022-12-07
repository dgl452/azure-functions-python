import nest_asyncio
import base64
import azure.functions as func
import requests
from fastapi import FastAPI, Request
from typing import Union
from azure.functions import AsgiMiddleware
import azure.durable_functions as df

nest_asyncio.apply()

api = FastAPI()


@api.get("/export")
async def index(request: Request, starter: Union[str, None] = None):
    starter_bytes_enc = starter.encode("ascii")
    starter_bytes = base64.b64decode(starter_bytes_enc)
    starter_decoded = starter_bytes.decode("ascii")
    client = df.DurableOrchestrationClient(starter_decoded)
    instance_id = await client.start_new("orchestrator", None, None)
    return {
        "expoerter_id": instance_id,
    }


@api.get("/export/{id}/status")
async def index(request: Request, id: str):
    status = requests.get(
        f"http://localhost:7071/runtime/webhooks/durabletask/instances/{id}"
    )

    return status.json()


ASGI_MIDDLEWARE = AsgiMiddleware(api)


async def main(
    req: func.HttpRequest, context: func.Context, starter: str
) -> func.HttpResponse:
    starter_bytes = starter.encode("ascii")
    starter_base64_bytes = base64.b64encode(starter_bytes)
    base64_starter = starter_base64_bytes.decode("ascii")
    req._HttpRequest__url = f"{req._HttpRequest__url}?starter={ base64_starter }"
    return ASGI_MIDDLEWARE.handle(req, context)
