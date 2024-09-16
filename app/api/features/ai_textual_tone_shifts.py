from app.api.features.functions.ai_textual_tone_shifts_functions import (
    analyze_text_tone,
    decide_to_finish,
    implement_tone_shifts,
    perform_final_tone_check,
    suggest_tone_shifts,
)
from app.api.features.schemas.ai_textual_tone_shifts_schemas import GraphState
from app.api.logger import setup_logger
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

workflow = StateGraph(GraphState)

workflow.add_node("analyze_text_tone", analyze_text_tone)
workflow.add_node("suggest_tone_shifts", suggest_tone_shifts)
workflow.add_node("implement_tone_shifts", implement_tone_shifts)
workflow.add_node("perform_final_tone_check", perform_final_tone_check)

workflow.set_entry_point("analyze_text_tone")
workflow.add_edge('analyze_text_tone', "suggest_tone_shifts")
workflow.add_edge('suggest_tone_shifts', "implement_tone_shifts")
workflow.add_edge('implement_tone_shifts', "perform_final_tone_check")

workflow.add_conditional_edges(
    "perform_final_tone_check",
    decide_to_finish,
    {
        "end": END,
        "no": "implement_tone_shifts",
    },
)

def compile_workflow():
    app = workflow.compile()
    return app