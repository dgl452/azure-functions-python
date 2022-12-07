from fastapi import FastAPI, Request
import nest_asyncio
import azure.functions as func
from azure.functions import AsgiMiddleware

nest_asyncio.apply()

api = FastAPI()


@api.get("/say-hello")
async def index(request: Request):
    return {
        "info": "Hello Daniel! How Are you?",
    }


ASGI_MIDDLEWARE = AsgiMiddleware(api)


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return ASGI_MIDDLEWARE.handle(req, context)
