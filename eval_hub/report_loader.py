from typing import Dict, List
import json
from pathlib import Path


from report_data_classes import (
    Block, ReportData,
    PlotBlock,
    Comment,
    BlockType,
    TextBlock
)


def create_comments(comments_json: dict) -> List[Comment]:
    """
    Given a dictionary of comments, create comment objects of each
    :param comments_json:
    :return:
    """
    return [
        Comment(id='0', user=user, comment_text=comment)
        for user, comment in comments_json.items()
    ]


def load_plot_block(fig_path: Path) -> PlotBlock:
    with open(f'{fig_path}/comments.json', 'r') as f:
        comments = json.load(f)
        comments = create_comments(comments)

    with open(f'{fig_path}/metadata.json', 'r') as f:
        metadata = json.load(f)

    with open(f'{fig_path}/fig.json', 'r') as f:
        fig_data = f.read()

    return PlotBlock(id=metadata['id'],
                     title=metadata['title'],
                     description=metadata['description'],
                     graph_data=fig_data,
                     graph_parameters=metadata['parameters'],
                     comments=comments,
                     type=BlockType.PLOT)


def load_text_block(block_path: Path):
    with open(f'{block_path}/metadata.json', 'r') as f:
        metadata = json.load(f)

    return TextBlock(id=metadata['id'],
                     title=metadata['title'],
                     text=metadata['text'],
                     type=BlockType.TEXT)


def load_blocks(report_path: Path):
    figs_path = report_path / 'figs'
    texts_path = report_path / 'texts'
    plot_blocks = [
        load_plot_block(fig_path)
        for fig_path in figs_path.iterdir()
        if fig_path.is_dir()
    ]
    text_blocks = [
        load_text_block(text_path)
        for text_path in texts_path.iterdir()
        if text_path.is_dir()
    ]

    return plot_blocks, text_blocks


def create_report_structure(blocks: List[Block], report_structure: List[str]):
    """
    Given a list of blocks, create a list of blocks in the order specified by the report structure.
    The blocks are loaded ahead of time to reduce IO operations.
    :param blocks:
    :param report_structure:
    :return:
    """
    final_structure = []
    for block_id in report_structure:
        block = next((block for block in blocks if block.id == block_id), None)
        if block is not None:
            final_structure.append(block)
        else:
            raise ValueError(f'Block with id {block_id} not found in the list of blocks')
    return final_structure


def load_report(report_path: str) -> ReportData:
    report_path = Path(report_path)
    with open(f'{report_path}/metadata.json', 'r') as f:
        metadata = json.load(f)

    plot_blocks, text_blocks = load_blocks(report_path)
    blocks = create_report_structure(plot_blocks + text_blocks, metadata['structure'])

    return ReportData(id=metadata['id'],
                      title=metadata['title'],
                      description=metadata['description'],
                      blocks=blocks)


if __name__ == '__main__':
   import plotly.express as px
   df = px.data.iris()
   fig = px.scatter(df, x="sepal_width", y="sepal_length")
   fig.write_json('/Users/amihaio/Documents/work/eval-hub/dummy_data/report1/fig1.json')

   fig = px.line(range(10), range(10))
   fig.write_json('/Users/amihaio/Documents/work/eval-hub/dummy_data/report1/fig2.json')

   fig = px.bar(range(10), range(10))
   fig.write_json('/Users/amihaio/Documents/work/eval-hub/dummy_data/report2/fig1.json')

   fig = px.scatter(range(20), range(20))
   fig.write_json('/Users/amihaio/Documents/work/eval-hub/dummy_data/report2/fig2.json')
