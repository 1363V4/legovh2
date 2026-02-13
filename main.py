import json
import asyncio
from pathlib import Path

from watchfiles import run_process

from stario import Context, RichTracer, Stario, Writer, JsonTracer
from stario.http.router import Router

from stario import asset, at, data
from stario.html import (
    A,
    B,
    Body,
    Button,
    Div,
    H1,
    H2,
    H3,
    Head,
    Hr,
    Html,
    Img,
    Li,
    Link,
    Main,
    Meta,
    P,
    Script,
    Span,
    Style,
    Title,
    Ul,
)


def index_view():
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
                'href': f"/static/{asset('img/avatar.avif')}"
            }),
            Link({
                'rel': "stylesheet",
                'href': f"/static/{asset('css/index.css')}"
            }),
            Script({
                'type': "module",
                'src': f"/static/{asset('js/datastar.js')}"
            })
        ),
        Body(
            {'class': ["gc"]},
            data.signals({'theme': False}),
            data.attr({'light': "$theme"}),
            Main(
                {'class': ["gc gm-m gt-l"]},
                Div(
                    {'class': ["gg01d gc gt-xl"]},
                    Img({
                        'id': "avatar",
                        'src': f"/static/{asset("/img/avatar.avif")}",
                        'alt': "it's-a me!"
                    }),
                    Div(
                        {'id': "welcome"},
                        {'class': ["gc"]},
                        Span("Hello"),
                        Span("There"),
                        Span(
                            data.text("$theme ? '🌕' : '🌞'"),
                            data.on("click", "$theme = !$theme")
                        ),
                    )
                ),
                H1(
                    "Welcome to the website of ",
                    B("Louis Sunshine")
                ),
                P(
                    "I make ",
                    A(
                        {'href': "https://www.youtube.com/@louis_sunshine"},
                        "Youtube videos"
                    ),
                    " about ",
                    A(
                        {'href': "https://data-star.dev/"},
                        "Datastar"
                    )
                ),
                P(
                    {'class': ["gt-m"]},
                    "Contact: louissnshn @gmail"
                ),
                Hr(),
                H2("My projects"),
                Div(
                    {'class': ["project gc gm-m gp-m"]},
                    Img({
                        'src': f"/static/{asset("/svg/yinyang.svg")}",
                        'alt': "tao"
                    }),
                    Div(
                        {'class': ["project-description"]},
                        H3("The Tao"),
                        P("Zen programming"),
                        P("good principles when building with Datastar"),
                        A(
                            {'class': "button"},
                            {"href": 'https://tao.leg.ovh/'},
                            "Play now!"
                        )
                    )
                ),
                Hr(),
                Div(
                    {'id': "supporters"},
                    {'class': ["gt-m"]},
                    P("😺 O.G. Supporters 😺"),
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


async def tao_view(state):
    reps = int(state['reps'])
    custom_css = f'''
:root {{
    --light: {reps / 100}
}}
::view-transition-group(*) {{
	animation-duration: {2 - 2 * reps / 100}s;
}}
    '''

    match (state.get("previous"), state.get("next")):
        case (None, None):
            arrow_navigation = "null"
        case (None, _):
            arrow_navigation = f"evt.key == 'ArrowRight' ? window.location = '{state['next']}' : null"
        case (_, None):
            arrow_navigation = f"evt.key == 'ArrowLeft' ? window.location = '{state['previous']}' : null"
        case (_, _):
            arrow_navigation = f"evt.key == 'ArrowLeft' ? window.location = '{state['previous']}' : evt.key == 'ArrowRight' ? window.location = '{state['next']}' : null"
    if reps == 100:
        arrow_navigation = "null"

    return Html(
        {'lang': "en"},
        Head(
            Meta({'charset': "UTF-8"}),
            Meta(
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ),
            Title("The Tao"),
            Link({
                'rel': "icon",
                'href': f"/static/{asset('svg/yinyang.svg')}"
            }),
            Link({
                'rel': "stylesheet",
                'href': f"/static/{asset('css/tao.css')}"
            }),
            Script({
                'type': "module",
                'src': f"/static/{asset('js/datastar.js')}"
            }),
            Style(
                custom_css
            )
        ),
        Body(
            {'class': "gc"},
            data.on("keydown", arrow_navigation, window=True, throttle="1s"),
            Div(
                {'id': "container"},
                H1(state["title"]),
                P(state["content"]),
                Div(
                    {'id': "arrow-container"},
                    A(
                        {'href': state.get("previous")},
                        "⬅️",
                    ) if state.get("previous") else P(),
                    A(
                        {'href': state.get("next")},
                        "➡️",
                    ) if state.get("next") else None,
                ),
            )
        )
    )

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

        leg_router = Router()
        leg_router.get("/", index)
        leg_router.assets("/static", Path(__file__).parent / "static")
        app.host("leg.ovh", leg_router)

        tao_router = Router()
        tao_router.get("/*", tao)
        tao_router.assets("/static", Path(__file__).parent / "static")
        app.host("tao.leg.ovh", tao_router)

        await app.serve(unix_socket="/run/legovh/legovh.sock")
        # await app.serve()

def serve():
    asyncio.run(main())

if __name__ == "__main__":
    # serve()
    run_process(
        Path(__file__).parent,
        target=serve
    )
