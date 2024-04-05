import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify
import plotly.express as px

from helpers import create_user_avatar

dummy_data = px.data.iris()

LOTS_OF_TEXT = """
In the sprawling expanse of the universe, our tiny blue planet Earth is but a speck of dust. Yet, upon this minuscule orb, the dance of life unfolds in magnificent complexity. From the depths of the oceans to the peaks of the tallest mountains, life thrives in all its diversity. Each organism, from the tiniest bacterium to the mightiest whale, plays its part in the intricate web of existence.

Humanity, with its remarkable intelligence and boundless curiosity, has emerged as a dominant force on Earth. Through millennia of innovation and discovery, we have reshaped the world around us, harnessing the power of nature and bending it to our will. From the invention of the wheel to the exploration of outer space, our quest for knowledge and understanding knows no bounds.

Yet, for all our achievements, we stand at a crossroads. The same ingenuity that has propelled us to such great heights now threatens to be our undoing. Climate change, pollution, and dwindling resources loom large on the horizon, casting a shadow over the future of our planet. If we are to ensure the survival of our species and the myriad others with whom we share this world, we must act swiftly and decisively.
"""

SOME_TEXT = "In the sprawling expanse of the universe, our tiny blue planet Earth is but a speck of dust. Yet, upon this minuscule orb, the dance of life unfolds in magnificent complexity. From the depths of the oceans to the peaks of the tallest mountains, life thrives in all its diversity. Each organism, from the tiniest bacterium to the mightiest whale, plays its part in the intricate web of existence."


def create_left_header():
    return dmc.Grid([
        create_user_avatar(size='lg'),
        dmc.Stack([
            dmc.Text("Rappi eval", weight=700, size="xl", style={"margin-bottom": "0.1"}),
            dmc.Text("Amihai", weight=300, size="l", style={"margin-top": "0.1"}),
        ], style={"margin-left": "1rem", "gap": "2px"}, spacing="xs")
    ], style={'margin-top': '1rem', 'border-bottom': '1px solid lightgray', 'padding-bottom': '1rem', 'width': '100%'})


def create_folder_header():
    return dmc.Group([
        DashIconify(icon='bi:folder-fill', color='gray', width=30),
        dmc.Title('Rappi', order=2, color='gray')
    ])


def create_available_reports():
    return dmc.Stack([
        dmc.Group([
            DashIconify(icon='bi:file-earmark-text-fill', color='gray', width=20),
            dmc.Title('Rappi eval', order=3, color='gray')
        ]),
        dmc.Group([
            DashIconify(icon='bi:file-earmark-text-fill', color='gray', width=20),
            dmc.Title('Rappi buyers eval', order=3, color='gray')
        ]),
    ], style={'margin-left': '1rem'}
    )


def create_left_panel():
    return dmc.Stack([
        create_left_header(),
        dmc.Space(h=50),
        create_folder_header(),
        create_available_reports()

    ], style={'background': '#FBFBFA', 'border-right': '1px solid gray', 'height': '100vh'})


def create_right_header():
    return dmc.Stack([
        dmc.Title('Rappi eval', order=1, color='gray', align='center',
                  style={'margin-bottom': '1rem', 'font-size': 'xxx-large'}),
        dmc.Text(LOTS_OF_TEXT, color='gray', size='md', weight=400)
    ], style={'margin-top': '1rem', 'border-bottom': '1px solid lightgray', 'padding-bottom': '1rem', 'width': '100%'}
    )


def create_graph_block():
    return dmc.Stack([
        dmc.Group([
            dmc.Title('Graph', order=2, color='gray', align='center',
                      style={'margin-bottom': '1rem'}),
            # dmc.ActionIcon(
            #         DashIconify(icon='lets-icons:comment-light', color='gray', width=40),
            #         size='xl',
            # )
        ], position='apart'),
        dmc.Text('This is a graph', color='gray', size='md', weight=400, align='left'),
        dcc.Graph(figure=px.scatter(dummy_data, x="sepal_width", y="sepal_length"))
    ], style={'margin-top': '1rem',
              'padding-bottom': '1rem',
              'width': '100%'}
    )


def create_comment():
    return dmc.Stack([
        dmc.Group([
            create_user_avatar(size='sm'),
            dmc.Text('Amihai', color='gray', size='md', weight=700, align='left')
        ]),
        dmc.Text(SOME_TEXT, color='gray', size='md', weight=400, align='left')
    ], style={'margin-bottom': '1rem'})


def create_comment_input():
    return dmc.Textarea(
            placeholder='Write a comment...',
            label='',
            radius='md',
            rightSection=dmc.ActionIcon(
                    DashIconify(icon='material-symbols-light:send', color='gray', width=20),
                    size='xl'
            ),
            rightSectionWidth=50
    )


def create_comment_card():
    return dmc.Card([
       dmc.CardSection([
           dmc.Group([
               dmc.Text('Discussion', color='gray', size='md', weight=400, align='left'),
               dmc.ActionIcon(
                       DashIconify(icon="carbon:close"),
                       color="gray",
                       variant="transparent",
                )],
               position="apart"),
       ],
           withBorder=True,
           inheritPadding=True,
           py="xs",
       ),
       dmc.Stack([
           create_comment(),
           create_comment(),
           create_comment(),
           create_comment(),
       ], style={'overflow-y': 'auto', 'height': '500px', 'margin-bottom': '1rem'}),

       create_comment_input()
    ], radius='lg', withBorder=False, style={'height': '100%'}
    )


def create_graph_comment_block():
    return dmc.Grid([
        dmc.Col([
            create_graph_block(),
        ], span=8),
        dmc.Col([
            create_comment_card()
        ], span='auto', style={'height': '100%'})
    ], gutter='xs', style={'height': '700px', 'margin-bottom': '50px'}
    )


def create_right_panel():
    stack = [create_right_header()]

    for _ in range(5):
        stack.append(create_graph_comment_block())

    return dmc.Stack(stack)
