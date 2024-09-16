from app.api.features.schemas.ai_writing_enhancement_schemas import (
     AdvancedGrammarCorrectionSchema,
     ClarityReadabilityTextCorrectionSchema, 
     NormalizeTextCorrectionSchema,
     StylisticTextCorrectionSchema
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

def normalize_text(state):
    json_parser = JsonOutputParser(pydantic_object=NormalizeTextCorrectionSchema)

    messages = [
        SystemMessage(content=f"You are a text normalizer for {state['lang']} texts."),
        HumanMessage(content=f"""Please correct the following text for basic grammar and punctuation errors:

        {state['text']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Normalize text result: {parsed_result}")

    return {
        "normalized_text": parsed_result["corrected_normalize_text"],
        "normalize_corrections": parsed_result["normalize_corrections"]
    }

def advanced_grammar_correction(state):
    json_parser = JsonOutputParser(pydantic_object=AdvancedGrammarCorrectionSchema)

    messages = [
        SystemMessage(content=f"You are an advanced grammar and syntax corrector for {state['lang']} texts."),
        HumanMessage(content=f"""Please review the following text for advanced grammar, sentence structure, and syntactical errors:

        {state['normalized_text']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Advanced Grammar Correction result: {parsed_result}")

    return {
        "advanced_grammar_text": parsed_result["corrected_advanced_grammar_text"],
        "advanced_grammar_corrections": parsed_result["advanced_grammar_corrections"]
    }

def clarity_readability_enhancement(state):
    json_parser = JsonOutputParser(pydantic_object=ClarityReadabilityTextCorrectionSchema)

    messages = [
        SystemMessage(content=f"You are a clarity and readability enhancer for {state['lang']} texts."),
        HumanMessage(content=f"""Please improve the following text to make it clearer and easier to understand:

        {state['advanced_grammar_text']}

        Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"Clarity and Readability Enhancement result: {parsed_result}")

    return {
        "clarity_readability_text": parsed_result["corrected_clarity_readability_text"],
        "clarity_readability_corrections": parsed_result["clarity_readability_corrections"]
    }

def stylistic_enhancement(state):
  json_parser = JsonOutputParser(pydantic_object=StylisticTextCorrectionSchema)

  messages = [
    SystemMessage(content=f"You are a stylistic enhancer for {state['lang']} texts."),
    HumanMessage(content=f"""Please improve the professional and formal fluency, tone, and consistency of the following paragraph:

    {state['clarity_readability_text']}

    Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.
    """)
  ]

  result = llm.invoke(messages)

  parsed_result = json_parser.parse(result.content)

  logger.info(f"Stylistic Enhancement result: {parsed_result}")

  return {
      "corrected_style_text": parsed_result["corrected_style_text"],
      "stylistic_corrections": parsed_result["stylistic_corrections"],
  }