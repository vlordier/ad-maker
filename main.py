# main.py
import logging
from main_graph import MainGraph
from state_schemas import MainState

logging.basicConfig(level=logging.INFO)

def run():
    # Initialize the MainGraph
    runner = MainGraph()

    # Initial empty state
    initial_state = MainState()

    # Execute the graph with the initial state
    logging.info("Starting the execution of the Ad Storyboard Design Flow.")
    result = runner.execute(initial_state)

    if result:
        logging.info(f"Execution finished with the following result: {result}")
    else:
        logging.error("Execution failed or incomplete.")

if __name__ == "__main__":
    run()
