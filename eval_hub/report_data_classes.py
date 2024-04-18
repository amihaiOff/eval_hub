from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


GraphParameters = Dict[str, Any]
GraphData = str


class BlockType:
    TEXT = "text"
    PLOT = "plot"


@dataclass
class Block:
    id: str
    type: BlockType


@dataclass
class Comment:
    id: str
    comment_text: str
    user: str
    date: Optional[str] = None


@dataclass
class PlotBlock(Block):
    title: str
    description: str
    graph_data: GraphData
    graph_parameters: GraphParameters
    comments: List[Comment]


@dataclass
class TextBlock(Block):
    text: str
    title: Optional[str] = ""


@dataclass
class ReportData:
    id: str
    title: str
    description: str
    blocks: List[Block]

    def get_comments(self) -> Dict[str, List[Comment]]:
        comments = {}
        for block in self.blocks:
            if isinstance(block, PlotBlock):
                comments[block.id] = block.comments
        return comments

    def get_comments_as_dict(self):
        return {graph_id: [asdict(cmt) for cmt in cmt_lst] for graph_id, cmt_lst in self.get_comments().items()}

    def get_first_plot_block(self):
        for block in self.blocks:
            if block.type == BlockType.PLOT:
                return block
        return None
