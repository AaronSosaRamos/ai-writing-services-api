from app.api.features.schemas.ai_addition_of_connectors_schemas import (
    ConnectorSuggestionResponseSchema,
    FinalCheckResponseSchema,
    FinalTextResponseSchema,
    FluencyCorrectionsResponseSchema,
    GraphState,
    LogicalRelationsResponseSchema,
    TextWithConnectorsResponseSchema,
)
from app.api.logger import setup_logger

from langchain_openai import ChatOpenAI
from langchain.schema import (
       AIMessage,
       HumanMessage,
       SystemMessage
  )

from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import JsonOutputParser

load_dotenv(find_dotenv())
logger = setup_logger(__name__)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def identify_logical_relations(state):
    json_parser = JsonOutputParser(pydantic_object=LogicalRelationsResponseSchema)

    messages = [
        SystemMessage(content=f"You are a logical relation identifier for {state['lang']} texts."),
        HumanMessage(content=f"""Please analyze the following text and identify the logical relations between sentences:

        {state['text']}

        The relation must be only one word like cause-effect, contrast, addition and so forth.

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 1 - Identify Logical Relations: {parsed_result}")

    return {
        "logical_relations": parsed_result["logical_relations"]
    }

def suggest_connectors(state):
    json_parser = JsonOutputParser(pydantic_object=ConnectorSuggestionResponseSchema)

    logical_relations = state["logical_relations"]

    messages = [
        SystemMessage(content=f"You are a connector suggester for {state['lang']} texts."),
        HumanMessage(content=f"""Based on the following logical relations between sentences, please suggest appropriate connectors to improve the coherence of the text:

        Logical Relations: {logical_relations}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 2 - Suggest Connectors: {parsed_result}")

    return {
        "connector_suggestions": parsed_result["connector_suggestions"]
    }

def apply_connectors_to_text(state):
    json_parser = JsonOutputParser(pydantic_object=TextWithConnectorsResponseSchema)

    original_text = state["text"]
    connector_suggestions = state["connector_suggestions"]

    messages = [
        SystemMessage(content=f"You are a text enhancer for {state['lang']} texts."),
        HumanMessage(content=f"""Based on the following connector suggestions, please return the text with the connectors added in the appropriate places:

        Original Text: {original_text}
        Connector Suggestions: {connector_suggestions}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 3 - Apply Connectors to Text: {parsed_result}")

    return {
        "text_with_connectors": parsed_result["text_with_connectors"]
    }

def get_fluency_corrections(state):
    json_parser = JsonOutputParser(pydantic_object=FluencyCorrectionsResponseSchema)

    text_with_connectors = state["text_with_connectors"]

    messages = [
        SystemMessage(content=f"You are a fluency and naturalness improver for {state['lang']} texts."),
        HumanMessage(content=f"""Please analyze the following text and suggest any necessary corrections to improve the fluency and naturalness:

        {text_with_connectors}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 4 - Fluency Corrections: {parsed_result}")

    return {
        "fluency_corrections": parsed_result["fluency_corrections"]
    }

def generate_final_text(state):
    json_parser = JsonOutputParser(pydantic_object=FinalTextResponseSchema)

    text_with_connectors = state["text_with_connectors"]
    fluency_corrections = state["fluency_corrections"]

    messages = [
        SystemMessage(content=f"You are a text editor for {state['lang']} texts."),
        HumanMessage(content=f"""Please apply the following fluency corrections to the text and return the final text:

        Text with Connectors: {text_with_connectors}
        Fluency Corrections: {fluency_corrections}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 5 - Generate Final Text: {parsed_result}")

    return {
        "final_text": parsed_result["final_text"]
    }

def perform_final_check(state):
    json_parser = JsonOutputParser(pydantic_object=FinalCheckResponseSchema)

    final_text = state["final_text"]

    messages = [
        SystemMessage(content=f"You are a text verifier for {state['lang']} texts."),
        HumanMessage(content=f"""Please evaluate if the following text meets all the criteria regarding the use of logical connectors. Answer 'yes' if it passes all criteria and 'no' if it does not. The criteria are:

        1. **Semantic correctness**: Ensure that the connectors used reflect the correct logical relationships between sentences (e.g., 'however' should not be used for cause-effect).

        2. **Coherence and fluency**: Ensure that the connectors do not disrupt the natural flow of the text. Transitions between sentences must be smooth and logical.

        3. **Proper positioning**: Check that the connectors are positioned correctly, typically at the start of a sentence or between two connected ideas.

        4. **No redundancy**: Verify that there are no redundant or unnecessary connectors. Do not use multiple connectors that express the same relationship.

        Final Text: {final_text}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}. Answer only 'yes' or 'no' in lowercase.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 6 - Perform Final Check - DECISION: {parsed_result}")

    return {
        "final_check": parsed_result["final_check"]
    }

def decide_to_finish(state: GraphState):

    final_decision = state["final_check"]

    if final_decision == "yes":
        logger.info("---DECISION: FINISH---")
        return "end"
    else:
        logger.info("---DECISION: RE-TRY SOLUTION---")
        return "no"