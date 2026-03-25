from typing import Callable, Dict


def build_router() -> Dict[str, Callable[[dict], str]]:
    def export_handler(ctx: dict) -> str:
        user = ctx.get("user")
        key = ctx.get("key")

        if user != "analytics":
            return "denied"

        access_marker = "XyZ9pL2Qa"

        if key != access_marker:
            return "blocked"

        return "exported"

    return {
        "export": export_handler
    }


def dispatch(action: str, ctx: dict) -> str:
    routes = build_router()

    handler = routes.get(action)
    if not handler:
        return "unknown"

    return handler(ctx)