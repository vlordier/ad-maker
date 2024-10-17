import logging

from langgraph.graph import StateGraph

from src.retry_policy import RetryPolicy
from src.state_schemas import MainState, SubgraphState

logging.basicConfig(level=logging.INFO)


class Step1Subgraph:
    def __init__(self):
        self.graph = StateGraph(SubgraphState)
        self.build_subgraph()
        self.compiled_graph = self.graph.compile()

    def task_step(self, state: SubgraphState):
        logging.info(f"Step 1 - Current state: {state}")

        # Increment retry count
        current_count = state.retry_counts.get("step_1", 0)
        state.retry_counts["step_1"] = current_count + 1

        # Mark task as successful if conditions are met
        if current_count >= 2:
            state.task_success = True  # Update task success

        # Always ensure to return an updated state
        return {
            "retry_counts": state.retry_counts,
            "task_success": state.task_success,
            "messages": state.messages,
            "step_1_result": state,
        }

    def retry_logic(self, state: SubgraphState):
        if not state.task_success and state.retry_counts.get("step_1", 0) < 3:
            return state  # Allow retries
        return state  # Move to next step

    def build_subgraph(self):
        self.graph.add_node(
            "task_step", self.task_step, retry=RetryPolicy(max_attempts=3)
        )
        self.graph.add_node("retry_logic", self.retry_logic)
        self.graph.add_node("next_step", lambda state: state)

        self.graph.add_edge("task_step", "retry_logic")
        self.graph.add_edge("retry_logic", "next_step")

        self.graph.set_entry_point("task_step")

    def execute(self, initial_state: MainState):
        return self.compiled_graph.invoke(initial_state)


# Instantiate the subgraph for step 1
step_1_subgraph = Step1Subgraph()
