from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import random
import string
from datetime import datetime
import plotly.graph_objects as go


GraphParameters = Dict[str, Any]
GraphData = str


@dataclass
class Comment:
    id: str
    comment_text: str
    user: str
    date: Optional[str] = None


@dataclass
class GraphBlock:
    id: str
    title: str
    description: str
    graph_data: GraphData
    graph_parameters: GraphParameters
    comments: List[Comment]


@dataclass
class ReportData:
    id: str
    title: str
    description: str
    graph_blocks: List[GraphBlock]


SOME_TEXT = "In the sprawling expanse of the universe, our tiny blue planet Earth is but a speck of dust. Yet, upon this minuscule orb, the dance of life unfolds in magnificent complexity. From the depths of the oceans to the peaks of the tallest mountains, life thrives in all its diversity. Each organism, from the tiniest bacterium to the mightiest whale, plays its part in the intricate web of existence."

LOTS_OF_TEXT = """
In the sprawling expanse of the universe, our tiny blue planet Earth is but a speck of dust. Yet, upon this minuscule orb, the dance of life unfolds in magnificent complexity. From the depths of the oceans to the peaks of the tallest mountains, life thrives in all its diversity. Each organism, from the tiniest bacterium to the mightiest whale, plays its part in the intricate web of existence.

Humanity, with its remarkable intelligence and boundless curiosity, has emerged as a dominant force on Earth. Through millennia of innovation and discovery, we have reshaped the world around us, harnessing the power of nature and bending it to our will. From the invention of the wheel to the exploration of outer space, our quest for knowledge and understanding knows no bounds.

Yet, for all our achievements, we stand at a crossroads. The same ingenuity that has propelled us to such great heights now threatens to be our undoing. Climate change, pollution, and dwindling resources loom large on the horizon, casting a shadow over the future of our planet. If we are to ensure the survival of our species and the myriad others with whom we share this world, we must act swiftly and decisively.
"""


def generate_dummy_comment():
    return Comment(
        id=''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        comment_text=SOME_TEXT,
        user='User' + str(random.randint(1, 10)),
        date=str(datetime.now())
    )

def generate_dummy_plot():
    fig = go.Figure(data=go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13]))
    return fig.to_json()

def generate_dummy_graph_block():
    return GraphBlock(
        id=''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        title='GraphBlock' + str(random.randint(1, 10)),
        description='Dummy description',
        graph_data=generate_dummy_plot(),
        graph_parameters={'param1': 'value1', 'param2': 'value2'},
        comments=[generate_dummy_comment() for _ in range(random.randint(0, 5))]
    )


def generate_dummy_report_data():
    return ReportData(
        id=''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        title='ReportData' + str(random.randint(1, 10)),
        description=LOTS_OF_TEXT,
        graph_blocks=[generate_dummy_graph_block() for _ in range(random.randint(1, 3))]
    )


# Generating dummy data
dummy_data = [generate_dummy_report_data() for _ in range(3)]
