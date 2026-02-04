import asyncio
from pathlib import Path

from stario import Context, RichTracer, Stario, Writer, asset, at, data, JsonTracer
from stario.html import H1, Body, Button, Div, Head, Html, Meta, P, Script, Title, Link, Main, Button, Span, Progress, A, Ul, Li
from stario.http.router import Router

from watchfiles import run_process


def home_view():
    return Html(
        {"lang": "en"},
        Head(
            Meta({'charset': "UTF-8"}),
            Meta(
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ),
            Title("The Tao"),
            Link({
                'rel': "icon",
                'href': f"/static/{asset('img/favicon.ico')}"
            }),
            Link({
                'rel': "stylesheet",
                'href': f"/static/{asset('css/site.css')}"
            }),
            Script({
                'type': "module",
                'src': f"/static/{asset('js/datastar.js')}"
            })
        ),
        Body(
            Main(
                Div(
                    {'id': "welcome"},
                    Span("Hello"),
                    Span("There")
                ),
                Div(
                    Progress(
                        {
                            'max': 100,
                            'value': 0,
                        },
                        "0%"
                    ),
                    P("text")
                ),
                Div(
                    {'id': "donations"},
                    A(
                        {'href': "https://checkout.revolut.com/pay/439edbe5-bda3-4616-aa07-7c2123f5514e"},
                        Button("In EUR")
                    ),
                    A(
                        {'href': "https://checkout.revolut.com/pay/439edbe5-bda3-4616-aa07-7c2123f5514e"},
                        Button("In EUR")
                    ),
                ),
                Div(
                    {'id': "supporters"},
                    P("😺 Supporters 😺"),
                    Ul(
                        Li("Michael Spanner"),
                        Li("Michael Spanner"),
                        Li("Michael Spanner"),
                    )

                )
            )
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
