import logging

from langgraph.graph import END

from src.state_schemas import MainState


def supervisor(state: MainState, step_name: str):
    logging.info(f"Supervisor - Checking state for {step_name}: {state}")

    # Retry if the task failed
    if not state.task_success:
        logging.info(f"Supervisor - {step_name} failed. Retrying...")
        return state  # Return the current state for retry

    # If completed, move to the next step or end
    if step_name == "step_3":
        logging.info("All steps completed successfully.")
        return END

    logging.info(f"Supervisor - {step_name} succeeded. Proceeding to the next step.")
    return state  # Return the current state to continue
