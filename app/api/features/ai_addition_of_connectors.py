from app.api.features.functions.ai_addition_of_connectors_functions import (
    apply_connectors_to_text,
    decide_to_finish,
    generate_final_text,
    get_fluency_corrections,
    identify_logical_relations,
    perform_final_check,
    suggest_connectors,
)
from app.api.features.schemas.ai_addition_of_connectors_schemas import GraphState
from app.api.logger import setup_logger
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

workflow = StateGraph(GraphState)

workflow.add_node("identify_logical_relations", identify_logical_relations)
workflow.add_node("suggest_connectors", suggest_connectors)
workflow.add_node("apply_connectors_to_text", apply_connectors_to_text)
workflow.add_node("get_fluency_corrections", get_fluency_corrections)
workflow.add_node("generate_final_text", generate_final_text)
workflow.add_node("perform_final_check", perform_final_check)

workflow.set_entry_point("identify_logical_relations")
workflow.add_edge('identify_logical_relations', "suggest_connectors")
workflow.add_edge('suggest_connectors', "apply_connectors_to_text")
workflow.add_edge('apply_connectors_to_text', "get_fluency_corrections")
workflow.add_edge('get_fluency_corrections', "generate_final_text")
workflow.add_edge('generate_final_text', "perform_final_check")

workflow.add_conditional_edges(
    "perform_final_check",
    decide_to_finish,
    {
        "end": END,
        "no": "generate_final_text",
    },
)

def compile_workflow():
    app = workflow.compile()
    return app