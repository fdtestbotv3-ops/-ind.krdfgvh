import asyncio
from aiohttp import web

# Simple CORS utilities
def add_cors_headers(resp: web.StreamResponse):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

async def handle_options(request: web.Request) -> web.Response:
    resp = web.Response(status=204)
    return add_cors_headers(resp)

async def state(request: web.Request) -> web.Response:
    data = {
        "status": "ok",
        "state": {
            "connected_online": True,
            "connected_to_whisper": False,
            "region": "IND"
        }
    }
    resp = web.json_response(data)
    return add_cors_headers(resp)

async def send_emote(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        body = {}

    server = body.get("server")
    team_code = body.get("team_code")
    emote_id = body.get("emote_id")
    uids = body.get("uids", [])
    repeat = body.get("repeat", 1)
    spam_delay_ms = body.get("spam_delay_ms", 120)

    if not server or not team_code:
        err = {
            "status": "error",
            "message": "Missing server or team_code",
        }
        resp = web.json_response(err, status=400)
        return add_cors_headers(resp)

    # Mock success response; integrate real bot logic here if available
    result = {
        "status": "ok",
        "message": "Join/emote request accepted",
        "server": server,
        "team_code": team_code,
        "emote_id": emote_id,
        "uids": uids,
        "repeat": repeat,
        "spam_delay_ms": spam_delay_ms,
    }
    resp = web.json_response(result)
    return add_cors_headers(resp)

def create_app() -> web.Application:
    app = web.Application()
    app.router.add_route('OPTIONS', '/state', handle_options)
    app.router.add_route('OPTIONS', '/send_emote', handle_options)
    app.router.add_get('/state', state)
    app.router.add_post('/send_emote', send_emote)
    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='127.0.0.1', port=8787)