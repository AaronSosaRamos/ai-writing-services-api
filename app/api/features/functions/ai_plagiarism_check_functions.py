from app.api.features.schemas.ai_plagiarism_check_schemas import (
    FinalPlagiarismCheckResponseSchema,
    GraphState, 
    IsPlagiarismResponseSchema,
    PlagiarismCorrectionResponseSchema,
    PlagiarismSuspicionSuggestionResponseSchema,
    TextAnalysisResponseSchema
)
from app.api.logger import setup_logger
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import (
       AIMessage,
       HumanMessage,
       SystemMessage
  )
from langchain_core.output_parsers import JsonOutputParser

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def is_text_plagiarized(state):
    json_parser = JsonOutputParser(pydantic_object=IsPlagiarismResponseSchema)

    lang = state['lang']
    original_text = state['original_text']
    comparison_text = state['comparison_text']

    messages = [
        SystemMessage(content=f"You are a plagiarism detection expert for {lang} texts."),
        HumanMessage(content=f"""Please compare the following two texts and determine if the original text is likely plagiarized from the comparison text.
        Focus on similarities in phrasing, structure, and content. Based on your analysis, respond only with 'yes' if the original text is plagiarized, or 'no' if it is not. Answer in lowercase.

        Original Text:
        {original_text}

        Comparison Text:
        {comparison_text}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Plagiarism Check: {parsed_result}")

    return {
        "is_plagiarized": parsed_result["is_plagiarized"],
        "plagiarism_level": parsed_result["plagiarism_level"]
    }

def decide_to_continue(state: GraphState):

    is_plagiarized = state["is_plagiarized"]

    if is_plagiarized == "yes":
        logger.info("---DECISION: CONTINUE---")
        return "continue"
    else:
        logger.info("---DECISION: FINISH---")
        return "end"
    
def analyze_text_for_plagiarism(state):
    json_parser = JsonOutputParser(pydantic_object=TextAnalysisResponseSchema)

    lang = state['lang']
    original_text = state['original_text']
    comparison_text = state['comparison_text']

    messages = [
        SystemMessage(content=f"You are a plagiarism detection expert for {lang} texts."),
        HumanMessage(content=f"""Please analyze the following texts and determine the likelihood that each sentence in the original text is plagiarized from the comparison text.
        For each sentence, indicate the likelihood as a probability between 0 and 1, and flag any sentence that should be reviewed due to suspicious similarities.

        Original Text:
        {original_text}

        Comparison Text:
        {comparison_text}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Text Analysis for Plagiarism Detection: {parsed_result}")

    return {
        "text_analysis": parsed_result["text_analysis"]
    }

def generate_plagiarism_suspicion_suggestions(state):
    json_parser = JsonOutputParser(pydantic_object=PlagiarismSuspicionSuggestionResponseSchema)

    lang = state['lang']
    text_analysis = state['text_analysis']

    formatted_analysis = "\n".join(
        [f"Original Sentence: {analysis['sentence_original']}, Comparison Sentence: {analysis['sentence_comparison']}, Likelihood of Plagiarism: {analysis['likelihood_of_plagiarism']}"
        for analysis in text_analysis if analysis['flagged_for_review']]
    )

    messages = [
        SystemMessage(content=f"You are a plagiarism detection expert for {lang} texts."),
        HumanMessage(content=f"""Please review the following text analysis and provide suggestions for any sentences flagged as potentially plagiarized.
        For each flagged sentence, explain why it might be plagiarized and suggest any corrections if necessary.

        Text Analysis:
        {formatted_analysis}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Plagiarism Suspicion Suggestions: {parsed_result}")

    return {
        "plagiarism_suspicion_suggestions": parsed_result["plagiarism_suspicion_suggestions"]
    }

def apply_plagiarism_corrections(state):
    json_parser = JsonOutputParser(pydantic_object=PlagiarismCorrectionResponseSchema)

    lang = state['lang']
    plagiarism_suspicion_suggestions = state['plagiarism_suspicion_suggestions']

    formatted_suggestions = "\n".join(
        [f"Original Sentence: {suggestion['sentence_original']}, Suggestion: {suggestion['suggestion']}"
        for suggestion in plagiarism_suspicion_suggestions]
    )

    messages = [
        SystemMessage(content=f"You are a plagiarism correction expert for {lang} texts."),
        HumanMessage(content=f"""Based on the following plagiarism suspicion suggestions, please apply corrections to reduce suspicion that the text is plagiarized.
        For each flagged sentence, provide a corrected version and explain why the correction reduces the suspicion of plagiarism.

        Plagiarism Suspicion Suggestions:
        {formatted_suggestions}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Plagiarism Corrections: {parsed_result}")

    return {
        "plagiarism_corrections": parsed_result["plagiarism_corrections"]
    }

def final_plagiarism_check(state):
    json_parser = JsonOutputParser(pydantic_object=FinalPlagiarismCheckResponseSchema)

    lang = state['lang']
    plagiarism_corrections = state['plagiarism_corrections']

    formatted_corrections = "\n".join(
        [f"Original Sentence: {correction['original_sentence']}, Corrected Sentence: {correction['corrected_sentence']}"
        for correction in plagiarism_corrections]
    )

    messages = [
        SystemMessage(content=f"You are a plagiarism checker expert for {lang} texts."),
        HumanMessage(content=f"""Please review the following corrections made to the text that was previously flagged for plagiarism.
        Based on these corrections, determine if the text now passes the plagiarism check. Respond with 'yes' if the text is no longer suspected to be plagiarized, or 'no' if it still presents characteristics of plagiarism.
        Additionally, provide any review notes if necessary.

        Plagiarism Corrections:
        {formatted_corrections}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Final Plagiarism Check: {parsed_result}")

    return {
        "final_plagiarism_check": parsed_result["final_plagiarism_check"]
    }

def decide_to_finish(state: GraphState):

    final_check = state["final_plagiarism_check"]["final_check"]

    if final_check == "yes":
        logger.info("---DECISION: FINISH---")
        return "end"
    else:
        logger.info("---DECISION: RE-TRY SOLUTION---")
        return "no"