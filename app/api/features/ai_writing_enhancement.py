from app.api.features.functions.ai_writing_enhancement_functions import (
    advanced_grammar_correction,
    clarity_readability_enhancement,
    normalize_text,
    stylistic_enhancement,
)
from app.api.logger import setup_logger
from app.api.features.schemas.ai_writing_enhancement_schemas import GraphState
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

workflow = StateGraph(GraphState)

workflow.add_node("normalize_text", normalize_text)
workflow.add_node("advanced_grammar_correction", advanced_grammar_correction)
workflow.add_node("clarity_readability_enhancement", clarity_readability_enhancement)
workflow.add_node("stylistic_enhancement", stylistic_enhancement)

workflow.set_entry_point("normalize_text")
workflow.add_edge('normalize_text', "advanced_grammar_correction")
workflow.add_edge('advanced_grammar_correction', "clarity_readability_enhancement")
workflow.add_edge('clarity_readability_enhancement', "stylistic_enhancement")
workflow.add_edge('stylistic_enhancement', END)

def compile_workflow():
    app = workflow.compile()
    return app