from typing import Annotated, Dict, Sequence

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class BaseState(BaseModel):
    retry_counts: Annotated[
        Dict[str, int], Field(default_factory=dict)
    ]  # Use a dictionary to track retry counts
    task_success: bool = Field(default=False)
    messages: Annotated[
        Sequence[BaseMessage], Field(default_factory=list)
    ]  # Default to an empty list


class SubgraphState(BaseState):
    pass


class MainState(BaseState):
    step_1_result: SubgraphState = Field(default_factory=SubgraphState)
    step_2_result: SubgraphState = Field(default_factory=SubgraphState)
    step_3_result: SubgraphState = Field(default_factory=SubgraphState)
