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
                        Span("🌞"),
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
                        Button("Play now!")
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
                'href': f"/static/{asset('img/favicon.ico')}"
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
        # That was the head part, very easy
        Body(
            {'class': "gc"}, # using 'gc' from our utility CSS gold.css
            Div(
                {'id': "container"},
                H1(state["title"]), # we get the state, we put it here
                P(state["content"]),
                Div(
                    {'id': "arrow-container"},
                    A(
                        {'href': state.get("previous")},
                        "⬅️",
                    ) if state.get("previous") else P(), # an empty P not to mess up the grid
                    A(
                        {'href': state.get("next")},
                        "➡️",
                    ) if state.get("next") else None, # None or "" will not get rendered by Stario. Practical!
                ),
            )
        )
    )
