from app.api.features.schemas.ai_addition_of_connectors_schemas import FinalCheckResponseSchema
from app.api.features.schemas.ai_textual_tone_shifts_schemas import (
    GraphState,
    ToneAnalysisResponseSchema,
    ToneShiftImplementationResponseSchema,
    ToneShiftSuggestionSchema,
)
from app.api.logger import setup_logger
from langchain_openai import ChatOpenAI
from langchain.schema import (
       AIMessage,
       HumanMessage,
       SystemMessage
  )
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logger = setup_logger(__name__)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def analyze_text_tone(state):
    json_parser = JsonOutputParser(pydantic_object=ToneAnalysisResponseSchema)

    target_tone = state['target_tone']

    messages = [
        SystemMessage(content=f"You are a tone analysis expert for {state['lang']} texts."),
        HumanMessage(content=f"""Please analyze the following text and identify the tone of each sentence.
        Indicate if the tone is formal, informal, persuasive, emotional, or neutral. Also, specify whether a tone shift is needed to achieve the target tone: {target_tone}.

        Text to analyze:
        {state['text']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 1 - Tone Analysis: {parsed_result}")

    return {
        "tone_analysis": parsed_result["tone_analysis"]
    }

def suggest_tone_shifts(state):
    json_parser = JsonOutputParser(pydantic_object=ToneShiftSuggestionSchema)

    messages = [
        SystemMessage(content=f"You are a tone shift suggester for {state['lang']} texts."),
        HumanMessage(content=f"""Based on the following tone analysis, please suggest specific changes to adjust the tone where necessary.
        The suggestions should include modifications to word choices, sentence structures, or overall style to achieve the desired tone.

        Tone Analysis:
        {state['tone_analysis']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 2 - Tone Shift Suggestions: {parsed_result}")

    return {
        "tone_shift_suggestions": parsed_result["tone_shift_suggestions"]
    }

def implement_tone_shifts(state):
    json_parser = JsonOutputParser(pydantic_object=ToneShiftImplementationResponseSchema)

    messages = [
        SystemMessage(content=f"You are a tone shift implementer for {state['lang']} texts."),
        HumanMessage(content=f"""Based on the following tone shift suggestions, please implement the suggested changes in the text.
        After implementing the changes, provide the final version of the text along with a review of whether the tone shift was successful or if further adjustments are needed.

        Tone Shift Suggestions:
        {state['tone_shift_suggestions']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    print(f"STEP 3 - Tone Shift Implementation: {parsed_result}")

    return {
        "tone_shift_implementation": parsed_result["tone_shift_implementation"],
        "final_text": parsed_result["final_text"],
        "final_review": parsed_result["final_review"],
        "review_notes": parsed_result["review_notes"]
    }

def perform_final_tone_check(state):
    json_parser = JsonOutputParser(pydantic_object=FinalCheckResponseSchema)

    messages = [
        SystemMessage(content=f"You are a final tone shift evaluator for {state['lang']} texts."),
        HumanMessage(content=f"""Please evaluate if the following text passes all the criteria for tone shifting.
        You must answer only 'yes' if the text meets the desired tone, and 'no' if it does not. Be precise in your judgment.

        Final Text to check:
        {state['final_text']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"STEP 4 - Final Tone Check: {parsed_result}")

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