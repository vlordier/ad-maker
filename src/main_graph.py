import logging

from langgraph.graph import END, START, StateGraph

from src.state_schemas import MainState
from src.subgraph_step1 import step_1_subgraph
from src.subgraph_step2 import step_2_subgraph
from src.subgraph_step3 import step_3_subgraph
from src.supervisor import supervisor

logging.basicConfig(level=logging.INFO)


class MainGraph:
    def __init__(self):
        self.graph = StateGraph(MainState)
        self.build_graph()

    def build_graph(self):
        # Define the node for step 1
        self.graph.add_node("step_1", step_1_subgraph.execute)
        self.graph.add_edge(START, "step_1")

        # Supervisor after step 1
        self.graph.add_node("supervisor_1", lambda state: supervisor(state, "step_1"))
        self.graph.add_edge("step_1", "supervisor_1")

        # Define the node for step 2
        self.graph.add_node("step_2", step_2_subgraph.execute)
        self.graph.add_edge("supervisor_1", "step_2")

        # Supervisor after step 2
        self.graph.add_node("supervisor_2", lambda state: supervisor(state, "step_2"))
        self.graph.add_edge("step_2", "supervisor_2")

        # Define the node for step 3
        self.graph.add_node("step_3", step_3_subgraph.execute)
        self.graph.add_edge("supervisor_2", "step_3")

        # Supervisor after step 3
        self.graph.add_node("supervisor_3", lambda state: supervisor(state, "step_3"))
        self.graph.add_edge("step_3", "supervisor_3")

        # End the graph after all steps
        self.graph.add_edge("supervisor_3", END)

        # Set entry and finish points
        self.graph.set_entry_point("step_1")
        self.graph.set_finish_point("supervisor_3")

        self.compiled_graph = self.graph.compile()

    def execute(self, initial_state: MainState):
        logging.info(f"Initial state: {initial_state}")

        current_state = initial_state.copy()  # Start with the initial state
        previous_state = None  # Initialize previous_state as None

        # Use a loop to handle state changes and backtracking
        while True:
            # Run the compiled graph with the current state
            result = self.compiled_graph.invoke(current_state)

            # If the result state differs from the previous state, handle backtracking
            if previous_state and previous_state != result:
                logging.info(
                    f"State changed! Backtracking to previous state: {previous_state}"
                )
                current_state = previous_state.copy()
            else:
                previous_state = result.copy()  # Update the previous state

            if result == END:
                logging.info("Execution finished successfully.")
                break

        return result


# Instantiate the main graph
main_graph = MainGraph()
