import json
import asyncio
from pathlib import Path

from stario import Context, RichTracer, Stario, Writer, JsonTracer
from stario.http.router import Router

from watchfiles import run_process

from views import index_view, tao_view


# HANDLERS

async def index(c: Context, w: Writer):
    w.html(index_view())

async def tao(c: Context, w: Writer):
    json_database_path = Path(__file__).parent / "data.json" 
    json_database = json.loads(json_database_path.read_text())

    reps = c.req.cookies.get('reps', 0)

    match c.req.tail:
        case "":
            state = json_database["state"]
        case tail if tail in json_database:
            if tail == "state":
                reps = min(int(reps) + 10, 100)
            state = json_database[tail]
        case _:
            html_response = "404 not found (your fault, this dog can fetch)"
            w.html(html_response)
            return
    
    state['reps'] = reps
    html_response = await tao_view(state)
    w.cookie("reps", reps, httponly=True, secure=True)
    w.html(html_response)

# APP

async def main():
    # with RichTracer() as tracer:
    with JsonTracer() as tracer:
        app = Stario(tracer)
        app.assets("/static", Path(__file__).parent / "static")

        legovh = Router()
        legovh.get("/*", index)
        app.host("legovh.com", legovh)

        tao_router = Router()
        tao_router.get("/*", tao)
        app.host("tao.legovh.com", tao_router)

        await app.serve(unix_socket="/run/legovh/legovh.sock")
        # await app.serve()


def serve():
    asyncio.run(main())

if __name__ == "__main__":
    run_process(
        Path(__file__).parent,
        target=serve
    )
