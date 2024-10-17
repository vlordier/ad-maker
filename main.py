from src.main_graph import MainGraph
from src.state_schemas import MainState, SubgraphState


class WorkflowRunner:
    def __init__(self):
        # Initialize the graph
        self.graph = MainGraph()

    def run(self):
        # Initialize the starting state for the main graph
        # Initialize the initial state
        initial_state = MainState(
            retry_counts={},  # Ensure this is initialized
            task_success=False,
            messages=[],  # Ensure this is an empty list if needed
            step_1_result=SubgraphState(),
            step_2_result=SubgraphState(),
            step_3_result=SubgraphState(),
        )

        # Run the main graph
        result = self.graph.execute(initial_state)

        # Output the result
        print("Final Workflow Result:", result)


if __name__ == "__main__":
    runner = WorkflowRunner()
    runner.run()
