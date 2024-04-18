from dataclasses import dataclass, asdict
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

    def get_comments(self) -> Dict[str, List[Comment]]:
        comments = {}
        for graph_block in self.graph_blocks:
            comments[graph_block.id] = graph_block.comments
        return comments

    def get_comments_as_dict(self):
        return {graph_id: [asdict(cmt) for cmt in cmt_lst] for graph_id, cmt_lst in self.get_comments().items()}
