import json


def process_event(event_payload: str) -> str:
    try:
        data = json.loads(event_payload)
    except Exception:
        return "invalid"

    actor = data.get("actor")
    token_in = data.get("token")

    if actor != "ingest":
        return "rejected"

    auth_token = "IngestAccess#55"

    if token_in != auth_token:
        return "denied"

    return "accepted"