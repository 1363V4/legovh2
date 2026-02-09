import asyncio
from functools import cache
from pathlib import Path

from stario import Context, RichTracer, Stario, Writer, asset, at, data, JsonTracer
from stario.html import H1, Body, Button, Div, Head, Html, Meta, P, Script, Title, Link, Main, Button, Span, Progress, A, Ul, Li, Img, Hr
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
            Title("leg.ovh"),
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
            {'class': ["gc"]},
            Main(
                {'class': ["gc gm-l gt-l"]},
                Div(
                    {'id': "welcome"},
                    {'class': ["gt-xl"]},
                    Span("Hello"),
                    Span("There"),
                    Span("🌞"),
                ),
                P(
                    "Become a supporter of the ",
                    A(
                        {'href': "https://www.youtube.com/@louis_sunshine"},
                        "channel"
                    ),
                    "!"
                ),
                Div(
                    Progress(
                        {
                            'max': 100,
                            'value': 57,
                        },
                        "57%"
                    ),
                    P(
                        {'class': ["gt-s"]},
                        "230$ left in 2026"
                    )
                ),
                Div(
                    {'id': "donations"},
                    {'class': ["gc"]},
                    A(
                        {'href': "https://checkout.revolut.com/pay/439edbe5-bda3-4616-aa07-7c2123f5514e"},
                        Button("In EUR")
                    ),
                    A(
                        {'href': "https://checkout.revolut.com/pay/6cf1abf4-7cf5-46e3-9f05-5287eee0ddd4"},
                        Button("In USD")
                    ),
                ),
                Div(
                    {'id': "supporters"},
                    {'class': ["gt-m"]},
                    P("😺 Supporters 😺"),
                    Ul(
                        Li("Michael Spanner"),
                        Li("Ben Croker"),
                        Li("Delaney Gillilan"),
                        Li("ndendic"),
                        Li("Anders Murphy"),
                        Li("Adam Bobowski"),
                        Li("C. Gampert"),
                        Li("Andy G."),
                    )
                ),
                Hr(),
                P("Thanks! You're a data star 😉"),
                Div(
                    {'id': "reopening"},
                    {'class': ["gc"]},
                    Img(
                        {'src': f"/static/{asset('img/stario.png')}"}
                    ),
                    Div(
                        P("GRAND REOPENING!"),
                        P(
                            {'class': ["gt-m"]},
                            "Now with added Stario™"
                        )
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
