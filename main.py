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
    Source,
    Span,
    Style,
    Title,
    Ul,
    Video
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
            }),
            Script({
                'type': "module",
                'src': f"/static/{asset('js/index.js')}"
            }),
        ),
        Body(
            {'class': ["gc"]},
            data.signals({'theme': False}),
            data.attr({'light': "$theme"}),
            Div(
                {'id': "dialog"},
                {'class': ["gp-m"]},
                data.on("avatar", "show(el); setTimeout(() => el.style.opacity = 0, 4000)", window=True),
                "Wow! Put me down!"
            ),
            Main(
                {'class': ["gc gm-m gt-l"]},
                Div(
                    {'class': ["gg01d gc gt-xl"]},
                    Img({
                        'id': "avatar",
                        'src': f"/static/{asset("/img/avatar-big.png")}",
                        'alt': "it's-a me!"
                    }),
                    Div(
                        {'id': "welcome"},
                        {'class': ["gc"]},
                        Span("Hello"),
                        Span("There"),
                        Span(
                            {'id': "sun"},
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
                    ),
                    Img({
                                            'src': f"/static/{asset("/img/rocket.avif")}",
                                            'alt': "rocket"
                                        }),
                ),
                P(
                    {'class': ["gt-m"]},
                    "Contact me on the Datastar discord!"
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
                        P("Good principles when building with Datastar"),
                        A(
                            {'class': "button"},
                            {"href": 'https://tao.leg.ovh/'},
                            "Play now!"
                        )
                    )
                ),
                Img({
                    'id': "dave",
                    'src': f"/static/{asset("/img/dave.png")}",
                    'alt': "dave meme"
                }),
                Hr(),
                Div(
                    {'id': "supporters"},
                    {'class': ["gt-m"]},
                    H2("😺 Supporters 😺"),
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
                H2("Thanks! You're a data star 😉"),
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
            data.on("keydown", arrow_navigation, window=True, throttle="500ms"),
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

def mclein_view():
    return Html(
        {"lang": "en"},
        Head(
            Meta({'charset': "UTF-8"}),
            Meta({"name": "viewport", "content": "width=device-width, initial-scale=1"}),
            Meta({"property": "og:title", "content": "MCL31N"}),
            Meta({"property": "og:description", "content": "THE FUTURE IN YOUR HANDS"}),
            Meta({"property": "og:url", "content": "https://mcle.in"}),
            Meta({"property": "og:image", "content": "https://mcle.in/static/img/mclein_card.png"}),
            Meta({"property": "og:type", "content": "website"}),
            Title("McLein"),
            Link({
                'rel': "icon",
                'href': f"/static/{asset('img/mclein_logo.jpg')}"
            }),
            Link({
                'rel': "stylesheet",
                'href': f"/static/{asset('css/mclein.css')}"
            }),
            Script({
                'type': "module",
                'src': f"/static/{asset('js/datastar.js')}"
            }),
        ),
        Body(
            {'class': ["gf gc gz"]},
            # Div({'id': "video"}),
            Video(
                {'id': "video"},
                {"autoplay": True, "muted": True, "loop": True, "playsinline": True, "disablePictureInPicture": True},
                Source({
                    'src': f"/static/{asset('mp4/mclein_bg.mp4')}",
                    'type': "video/mp4"
                })
            ),
            Main(
                {'class': ["gc"]},
                H1(
                    "MCL31N"
                ),
                # P(
                #     {'id': "tagline"},
                #     data.on("click", at.get("/video")),
                #     "Enter"
                # ),
                P(
                    "The future in your hands"
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

async def mclein(c: Context, w: Writer):
    w.html(mclein_view())

async def video(c, w):
    w.patch(
        Video(
            {'id': "video"},
            {"autoplay": True, "muted": True, "loop": True, "playsinline": True, "disablePictureInPicture": True},
            Source({
                'src': f"/static/{asset('mp4/mclein_bg.mp4')}",
                'type': "video/mp4"
            })
        )
    )
    w.patch(
        P({'id': "tagline"}, "Future is in your hands")
    )

async def pape(c,w):
    w.html(
        Html(
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
                    'href': f"/static/{asset('css/wp.css')}"
                })
            ),
            Body(
                {'class': ["gc gt-xxl"]},
                Main(
                    P("L"),
                    P("O"),
                    P("U"),
                    P("I"),
                    P("S"),
                    P("S"),
                    P("N"),
                    P("S"),
                    P("H"),
                    P("N"),
                )
            ),
        )
    )

# APP

async def main():
    # with RichTracer() as tracer:
    with JsonTracer() as tracer:
        app = Stario(tracer)

        leg_router = Router()
        leg_router.get("/", index)
        leg_router.get("/wp", pape)
        leg_router.assets("/static", Path(__file__).parent / "static")
        app.host("leg.ovh", leg_router)

        tao_router = Router()
        tao_router.get("/*", tao)
        tao_router.assets("/static", Path(__file__).parent / "static")
        app.host("tao.leg.ovh", tao_router)

        mclein_router = Router()
        mclein_router.get("/", mclein)
        mclein_router.get("/video", video)
        mclein_router.assets("/static", Path(__file__).parent / "static")
        app.host("mcle.in", mclein_router)

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
