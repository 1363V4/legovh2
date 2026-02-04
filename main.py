import asyncio
from dataclasses import dataclass
from pathlib import Path

from stario import Context, RichTracer, Stario, Writer, asset, at, data
from stario.html import H1, Body, Button, Div, Head, Html, Meta, P, Script, Title
from stario.toys import toy_inspector
from stario.http.router import Router

from watchfiles import run_process


def page(*children):
    """Base HTML page with Datastar."""
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
            {
                "style": "font-family: system-ui; padding: 2rem; max-width: 600px; margin: 0 auto;"
            },
            *children,
        ),
    )


def home_view():
    return page(
        toy_inspector()
    )

async def home(c: Context, w: Writer):
    w.html(home_view())


async def main():
    with RichTracer() as tracer:
        app = Stario(tracer)

        app.assets("/static", Path(__file__).parent / "static")

        # Routes
        legovh = Router()
        legovh.get("/", home_view)
        mm = Router()
        mm.get("/", home_view)

        # Start server
        app.host("*.leg.ovh", legovh)
        app.host("mm.leg.ovh", mm)
        await app.serve(
            unix_socket="legovh.sock"
        )


def serve():
    asyncio.run(main())

if __name__ == "__main__":
    run_process(
        Path(__file__).parent,
        target=serve
    )
