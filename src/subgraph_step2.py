# subgraph_step2.py
import logging

from langgraph.graph import StateGraph

from src.state_schemas import SubgraphState

logging.basicConfig(level=logging.INFO)


class Step2Subgraph:
    def __init__(self):
        self.graph = StateGraph(SubgraphState)
        self.build_subgraph()
        self.compiled_graph = self.graph.compile()

    def task_step(self, state: SubgraphState):
        logging.info(f"Step 2 - Current state: {state}")

        # Increment retry count
        state.retry_counts["step_2"] = state.retry_counts.get("step_2", 0) + 1

        # Example condition for task success (you can customize this logic)
        if state.retry_counts["step_2"] >= 3:
            state.task_success = True  # Mark as successful after 3 retries

        # Always ensure to return the updated state
        return {
            "retry_counts": state.retry_counts,
            "task_success": state.task_success,
            "messages": state.messages,
            "step_2_result": state,  # Make sure the result is part of the state
        }

    def retry_logic(self, state: SubgraphState):
        if not state.task_success and state.retry_counts.get("step_2", 0) < 3:
            return "task_step"
        return "next_step"

    def build_subgraph(self):
        self.graph.add_node("task_step", self.task_step)
        self.graph.add_node("retry_logic", self.retry_logic)
        self.graph.add_node("next_step", lambda state: state)

        self.graph.add_edge("task_step", "retry_logic")
        self.graph.add_edge("retry_logic", "next_step")

        self.graph.set_entry_point("task_step")

    def execute(self, state: SubgraphState):
        # Log current state
        logging.info(f"Executing step 2: {state}")

        # Perform task logic here
        state.retry_counts["step_2"] = state.retry_counts.get("step_2", 0) + 1
        if state.retry_counts["step_2"] >= 2:
            state.task_success = True

        # Always return the updated state
        return state


# Instantiate the subgraph for step 2
step_2_subgraph = Step2Subgraph()
