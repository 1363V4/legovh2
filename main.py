import asyncio
from pathlib import Path

from stario import Context, RichTracer, Stario, Writer, asset, at, data, JsonTracer
from stario.html import H1, Body, Button, Div, Head, Html, Meta, P, Script, Title
from stario.http.router import Router

from watchfiles import run_process


def home_view():
    return Html(
        {"lang": "en"},
        Head(
            Meta({"charset": "UTF-8"}),
            Meta(
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ),
            Title("Hello World - Stario App"),
            Script({"type": "module", "src": "/static/" + asset("js/datastar.js")}),
        ),
        Body(
        ),
    )

async def home(c: Context, w: Writer):
    w.html(home_view())


async def main():
    # with RichTracer() as tracer:
    with JsonTracer() as tracer:
        app = Stario(tracer)

        app.assets("/static", Path(__file__).parent / "static")

        app.get("/", home)

        await app.serve(unix_socket="/run/legovh/legovh.sock")


def serve():
    asyncio.run(main())

if __name__ == "__main__":
    run_process(
        Path(__file__).parent,
        target=serve
    )
