import nest_asyncio
import base64
import azure.functions as func
import azure.durable_functions as df
from fastapi import FastAPI, Request, Depends
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


def get_starter(request: Request) -> str:
    b64_starter = str(request.url).split("starter=")[1]
    return decode_starter(b64_starter)


@api.post("/export")
async def create_export(starter: str = Depends(get_starter)):
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("orchestrator", None, None)
    return {
        "expoerter_id": instance_id,
    }


@api.get("/export")
async def get_exports(starter: str = Depends(get_starter)):
    client = df.DurableOrchestrationClient(starter)
    instances = await client.get_status_all()
    return instances


@api.get("/export/{id}/status")
async def get_export_status(id: str, starter: str = Depends(get_starter)):
    client = df.DurableOrchestrationClient(starter)
    instance = await client.get_status(
        id, show_history=True, show_history_output=True, show_input=True
    )
    return instance


ASGI_MIDDLEWARE = AsgiMiddleware(api)


async def main(
    req: func.HttpRequest, context: func.Context, starter: str
) -> func.HttpResponse:
    req._HttpRequest__url = (
        f"{req._HttpRequest__url}?starter={ encode_starter(starter) }"
    )
    return ASGI_MIDDLEWARE.handle(req, context)
