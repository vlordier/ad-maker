# main_graph.py
import logging

from langgraph.graph import END, START, StateGraph

from src.ad_tasks import (
    ask_for_ad_info,
    generate_ad_concept,
    generate_storyboard,
    validate_ad_concept,
    validate_storyboard,
)
from src.state_schemas import MainState

logging.basicConfig(level=logging.INFO)


class MainGraph:
    def __init__(self):
        self.graph = StateGraph(MainState)
        self.build_graph()

    def create_supervisor(self, step_name: str, retry_node: str):
        """Supervisor function to handle user input validation and retries."""

        def supervisor_lambda(state: MainState, prev_state: MainState):
            logging.info(f"Supervisor - Checking state for {step_name}: {state}")

            # If the task was unsuccessful, trigger a retry or backtrack
            if not state.task_success:
                logging.info(
                    f"Supervisor - {step_name} failed. Retrying or backtracking..."
                )

                # Allow retry or backtracking based on user input
                user_input = (
                    input(
                        f"Do you want to retry {step_name} or backtrack? (retry/backtrack): "
                    )
                    .strip()
                    .lower()
                )

                if user_input == "retry":
                    logging.info(f"Retrying {step_name}...")
                    state.retry_counts[step_name] = (
                        state.retry_counts.get(step_name, 0) + 1
                    )
                    return retry_node
                elif user_input == "backtrack":
                    logging.info("Backtracking to previous state...")
                    return prev_state  # Return the previous node for backtracking
                else:
                    logging.error("Invalid input. Defaulting to retry.")
                    return retry_node  # Default to retry if input is invalid

            logging.info(f"Supervisor - {step_name} successful.")
            return state

        return supervisor_lambda

    def build_graph(self):
        # Step 1: Collect Ad Information
        self.graph.add_node("ask_for_ad_info", ask_for_ad_info)
        self.graph.add_edge(START, "ask_for_ad_info")

        # Supervisor after Step 1
        self.graph.add_node(
            "supervisor_1", self.create_supervisor("step_1", "ask_for_ad_info")
        )
        self.graph.add_edge("ask_for_ad_info", "supervisor_1")

        # Step 2: Generate Ad Concept
        self.graph.add_node("generate_ad_concept", generate_ad_concept)
        self.graph.add_edge("supervisor_1", "generate_ad_concept")

        # Supervisor after Step 2
        self.graph.add_node(
            "supervisor_2", self.create_supervisor("step_2", "generate_ad_concept")
        )
        self.graph.add_edge("generate_ad_concept", "supervisor_2")

        # Step 3: Validate Ad Concept
        self.graph.add_node("validate_ad_concept", validate_ad_concept)
        self.graph.add_edge("supervisor_2", "validate_ad_concept")

        # Supervisor after Step 3
        self.graph.add_node(
            "supervisor_3", self.create_supervisor("step_3", "validate_ad_concept")
        )
        self.graph.add_edge("validate_ad_concept", "supervisor_3")

        # Step 4: Generate Storyboard
        self.graph.add_node("generate_storyboard", generate_storyboard)
        self.graph.add_edge("supervisor_3", "generate_storyboard")

        # Supervisor after Step 4
        self.graph.add_node(
            "supervisor_4", self.create_supervisor("step_4", "generate_storyboard")
        )
        self.graph.add_edge("generate_storyboard", "supervisor_4")

        # Step 5: Validate Storyboard
        self.graph.add_node("validate_storyboard", validate_storyboard)
        self.graph.add_edge("supervisor_4", "validate_storyboard")

        # Final Supervisor after validating storyboard
        self.graph.add_node(
            "supervisor_final",
            self.create_supervisor("step_final", "validate_storyboard"),
        )
        self.graph.add_edge("validate_storyboard", "supervisor_final")

        # End point
        self.graph.add_edge("supervisor_final", END)

        # Compile the graph
        self.compiled_graph = self.graph.compile()

    def execute(self, initial_state: MainState):
        logging.info(f"Initial state: {initial_state}")

        current_state = initial_state.copy()  # Start with the initial state

        while True:
            result = self.compiled_graph.invoke(current_state)

            # Check for finished state
            if result == END:
                logging.info("Execution finished successfully.")
                break

            # If any state step failed, retry or backtrack
            if not result.task_success:
                logging.info(f"Retrying step. Current state: {result}")
                continue

        return result


# Example Runner
if __name__ == "__main__":
    runner = MainGraph()
    initial_state = MainState()  # Initial empty state
    runner.execute(initial_state)
