from typing import Dict, List
import json
from pathlib import Path


from report_data_classes import (
    ReportData,
    GraphBlock,
    Comment
)


def create_comments(comments_json: dict) -> List[Comment]:
    """
       Given a dictionary of comments, create comment objects of each
       :param comments_json:
       :return:
       """
    comment_objs = []
    for user, comment in comments_json.items():
        comment_objs.append(Comment(id='0',
                                    user=user,
                                    comment_text=comment)
                            )
    return comment_objs


def load_fig_block(fig_path: Path) -> GraphBlock:
    with open(f'{fig_path}/comments.json', 'r') as f:
        comments = json.load(f)
        comments = create_comments(comments)

    with open(f'{fig_path}/metadata.json', 'r') as f:
        metadata = json.load(f)

    with open(f'{fig_path}/fig.json', 'r') as f:
        fig_data = f.read()

    return GraphBlock(id=metadata['id'],
                      title=metadata['title'],
                      description=metadata['description'],
                      graph_data=fig_data,
                      graph_parameters=metadata['parameters'],
                      comments=comments)


def load_report(report_path: str) -> ReportData:
    report_path = Path(report_path)
    figs_path = report_path / 'figs'
    graph_blocks = []
    for fig_path in figs_path.iterdir():
        if not fig_path.is_dir():
            continue
        graph_blocks.append(load_fig_block(fig_path))

    with open(f'{report_path}/metadata.json', 'r') as f:
        metadata = json.load(f)

    return ReportData(id='0',
                      title=metadata['title'],
                      description=metadata['description'],
                      graph_blocks=graph_blocks)


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
