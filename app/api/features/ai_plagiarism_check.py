from app.api.features.functions.ai_plagiarism_check_functions import (
    analyze_text_for_plagiarism,
    apply_plagiarism_corrections,
    decide_to_continue,
    final_plagiarism_check,
    generate_plagiarism_suspicion_suggestions, 
    is_text_plagiarized,
    decide_to_finish
)
from app.api.features.schemas.ai_plagiarism_check_schemas import GraphState
from app.api.logger import setup_logger
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

workflow = StateGraph(GraphState)

workflow.add_node("is_text_plagiarized", is_text_plagiarized)
workflow.add_node("analyze_text_for_plagiarism", analyze_text_for_plagiarism)

workflow.add_node("generate_plagiarism_suspicion_suggestions", generate_plagiarism_suspicion_suggestions)
workflow.add_node("apply_plagiarism_corrections", apply_plagiarism_corrections)
workflow.add_node("final_plagiarism_check_node", final_plagiarism_check)

workflow.set_entry_point("is_text_plagiarized")
workflow.add_conditional_edges(
    "is_text_plagiarized",
    decide_to_continue,
    {
        "continue": "analyze_text_for_plagiarism",
        "end": END,
    },
)
workflow.add_edge('analyze_text_for_plagiarism', "generate_plagiarism_suspicion_suggestions")
workflow.add_edge('generate_plagiarism_suspicion_suggestions', "apply_plagiarism_corrections")
workflow.add_edge('apply_plagiarism_corrections', "final_plagiarism_check_node")

workflow.add_conditional_edges(
    "final_plagiarism_check_node",
    decide_to_finish,
    {
        "end": END,
        "no": "apply_plagiarism_corrections",
    },
)
def compile_workflow():
    app = workflow.compile()
    return app