from typing import Dict, List
import json
from pathlib import Path

from plotly.io import read_json


from report_data_classes import (
    ReportData,
    GraphBlock,
    Comment,
    GraphParameters,
    GraphData
)

def create_comments(comments_json: dict) -> Dict[str, List[Comment]]:
   """
   Given a dictionary of comments, create comment objects of each
   :param comments_json:
   :return:
   """
   comment_dict = {}
   for fig_name, comments in comments_json.items():
       comments_lst = []
       for user, comment in comments.items():
           comments_lst.append(Comment(id='0',
                                       user=user,
                                       comment_text=comment)
                               )
       comment_dict[fig_name] = comments_lst

   return comment_dict


def load_graph_block(fig_path: Path) -> GraphBlock:
    with open(f'{fig_path}/comments.json', 'r') as f:
        comments = json.load(f)
        comments = create_comments(comments)



    return GraphBlock(id='0',
                      title=fig_path.name,
                      description='This is a description',
                      graph_data=GraphData(fig=read_json(f'{fig_path}/fig.json')),
                      graph_parameters=GraphParameters(),
                      comments=comments)


def load_report(report_path: str) -> ReportData:
    graph_blocks = []
    for fig_path in Path(report_path).iterdir():
        if not fig_path.is_dir():
            continue
        graph_blocks.append(load_graph_block(fig_path))

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
