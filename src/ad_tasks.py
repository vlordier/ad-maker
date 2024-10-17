from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging
from state_schemas import MainState
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)

# Function to call LLM for better suggestions on a failed input
def llm_suggest_fallback(field: str, current_value: str):
    """LLM fallback to suggest a valid value."""
    prompt_template = PromptTemplate(
        input_variables=["field", "current_value"],
        template="Suggest a valid {field} given the invalid value: {current_value}."
    )
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = LLMChain(prompt=prompt_template, llm=llm)
    
    response = chain.invoke({"field": field, "current_value": current_value})
    suggestion = response
    logging.info(f"LLM suggested {field}: {suggestion}")
    return suggestion

# Step 1: Collecting and Validating Ad Information
def ask_for_ad_info(state: MainState):
    try:
        # Collect ad information
        state.ad_duration = int(input("Enter Ad Duration (0-60s): "))
        state.ad_channel = input("Enter Ad Channel (Facebook, Instagram, TikTok): ")
        state.ad_theme = input("Enter Ad Theme (~50-word description): ")

        # Validate the state using Pydantic
        state = MainState(**state.dict())

    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        # Use LLM-based suggestion for each error
        for error in e.errors():
            field = error['loc'][0]
            current_value = getattr(state, field)
            suggestion = llm_suggest_fallback(field, current_value)

            # Validate LLM suggestion
            try:
                setattr(state, field, suggestion)
                state = MainState(**state.dict())  # Re-validate the state
            except ValidationError:
                logging.error(f"LLM suggestion for {field} was also invalid: {suggestion}")
                # Fallback to human input
                logging.info(f"Asking for human input for {field}.")
                if field == "ad_duration":
                    state.ad_duration = int(input("Enter valid Ad Duration (0-60s): "))
                elif field == "ad_channel":
                    state.ad_channel = input("Enter valid Ad Channel (Facebook, Instagram, TikTok): ")
                elif field == "ad_theme":
                    state.ad_theme = input("Enter valid Ad Theme (~50-word description): ")

        state.retry_counts['ask_for_ad_info'] = state.retry_counts.get('ask_for_ad_info', 0) + 1
        state.task_success = False
        return state

    state.task_success = True
    return state

# Step 2: Generate Ad Concept with LLM Prompting
def generate_ad_concept(state: MainState):
    logging.info("Generating Ad Concept via LLM.")

    # Use LLMChain with a prompt template for generating the ad concept
    prompt_template = PromptTemplate(
        input_variables=["ad_theme"],
        template="Generate an Ad Concept based on the theme: {ad_theme}."
    )
    llm = ChatOpenAI(model_name="gpt-4")
    chain = LLMChain(prompt=prompt_template, llm=llm)
    
    state.ad_concept = chain.invoke({"ad_theme": state.ad_theme})
    logging.info(f"Generated Ad Concept: {state.ad_concept}")
    return state

# Step 3: Validate the Ad Concept with the User
def validate_ad_concept(state: MainState):
    logging.info(f"Presenting Ad Concept: {state.ad_concept}")

    user_input = input("Do you approve this Ad Concept? (yes/no): ")

    if user_input.lower() == "yes":
        state.task_success = True
    elif user_input.lower() == "no":
        state.task_success = False
        state.retry_counts['generate_ad_concept'] = state.retry_counts.get('generate_ad_concept', 0) + 1
        logging.info("User rejected Ad Concept. Retrying...")
        return generate_ad_concept(state)
    else:
        logging.error("Invalid input. Please enter 'yes' or 'no'.")
        state.task_success = False
        return state

    return state

# Step 4: Generate and Validate Storyboard
def generate_storyboard(state: MainState):
    logging.info("Generating Storyboard based on Ad Duration.")

    # LLM prompt for storyboard generation
    prompt_template = PromptTemplate(
        input_variables=["ad_concept", "ad_duration"],
        template="""
        Generate a storyboard based on the following Ad Concept:
        {ad_concept}

        Ad Duration: {ad_duration} seconds.
        Generate the storyboard in multiple scenes with a coherent flow.
        """
    )
    
    llm = ChatOpenAI(model_name="gpt-4")
    chain = LLMChain(prompt=prompt_template, llm=llm)
    
    response = chain.invoke({
        "ad_concept": state.ad_concept,
        "ad_duration": state.ad_duration
    })
    
    state.storyboard = response.split("\n")
    logging.info(f"Generated Storyboard: {state.storyboard}")
    return state

# Validate Storyboard with User
def validate_storyboard(state: MainState):
    logging.info(f"Presenting Storyboard: {state.storyboard}")

    user_input = input("Do you approve this storyboard? (yes/no): ")

    if user_input.lower() == "yes":
        state.task_success = True
    elif user_input.lower() == "no":
        state.task_success = False
        state.retry_counts['generate_storyboard'] = state.retry_counts.get('generate_storyboard', 0) + 1
        logging.info("User rejected Storyboard. Retrying...")
        return generate_storyboard(state)
    else:
        logging.error("Invalid input. Please enter 'yes' or 'no'.")
        state.task_success = False
        return state

    return state
