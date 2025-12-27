import json
import logging
import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("webhook_receiver")

app = FastAPI(title="Webhook Receiver (Onboarding Template)")


@app.post("/webhooks")
async def receive_webhook(request: Request):
    """
    Day 2 minimal endpoint:
    - read raw body
    - parse JSON (safely)
    - log request_id, event_type, status
    - return 200
    """
    request_id = str(uuid.uuid4())

    raw_body = await request.body()
    body_text = raw_body.decode("utf-8", errors="replace")

    # parse JSON (keep it simple for day 2)
    try:
        payload = json.loads(body_text) if body_text else {}
    except json.JSONDecodeError:
        logger.info(
            "webhook_received",
            extra={
                "request_id": request_id,
                "status": "invalid_json",
            },
        )
        return JSONResponse(
            status_code=400,
            content={
                "request_id": request_id,
                "error": "invalid_json",
                "message": "Request body must be valid JSON.",
            },
        )

    event_type = payload.get("type") or payload.get("event_type") or "unknown"

    logger.info(
        "webhook_received",
        extra={
            "request_id": request_id,
            "event_type": event_type,
            "status": "ok",
        },
    )

    return {
        "request_id": request_id,
        "status": "ok",
        "event_type": event_type,
    }
