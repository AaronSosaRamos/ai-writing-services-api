from app.api.features.ai_spelling_checker import compile_chain
from app.api.features.ai_writing_enhancement import compile_workflow
from app.api.features.ai_addition_of_connectors import compile_workflow as complie_workflow_connectors
from app.api.features.ai_textual_tone_shifts import compile_workflow as complie_workflow_tone_shift
from app.api.features.ai_plagiarism_check import compile_workflow as complie_workflow_plagiarism_check
from app.api.features.schemas.ai_addition_of_connectors_schemas import AIAdditionOfConnectorsInputSchema
from app.api.features.schemas.ai_plagiarism_check_schemas import AIPlagiarismCheckInputSchema
from app.api.features.schemas.ai_textual_tone_shifts_schemas import AITextualToneShiftInputSchema
from app.api.features.schemas.ai_writing_enhancement_schemas import AIWritingEnhancementInputSchema
from app.api.features.schemas.schemas import RequestSchema, SpellingCheckerRequestArgs
from fastapi import APIRouter, Depends
from app.api.logger import setup_logger
from app.api.auth.auth import key_check

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/check-spelling")
async def submit_tool( data: RequestSchema, _ = Depends(key_check)):
    logger.info(f"Loading request args...")
    args = SpellingCheckerRequestArgs(spelling_checker_schema=data)
    logger.info(f"Args. loaded successfully")

    chain = compile_chain()

    logger.info("Generating the spelling checking analysis")
    results = chain.invoke(args.validate_and_return())
    logger.info("The spelling checking analysis has been successfully generated")

    return results

@router.post("/writing-enhancement")
async def submit_tool( data: AIWritingEnhancementInputSchema, _ = Depends(key_check)):
    logger.info(f"Args. loaded successfully: {data}")

    writing_enhancement_workflow = compile_workflow()

    logger.info("Developing the Writing Enhancement")

    result = writing_enhancement_workflow.invoke(
        {
            "text": data.text,
            "lang": data.lang
        }
    )    

    logger.info("The writing enhancement has been successfully done")

    return result

@router.post("/addition-of-connectors")
async def submit_tool( data: AIAdditionOfConnectorsInputSchema, _ = Depends(key_check)):
    logger.info(f"Args. loaded successfully: {data}")

    addition_of_connectors_workflow = complie_workflow_connectors()

    logger.info("Developing the Addition of Connectors")

    result = addition_of_connectors_workflow.invoke(
        {
            "text": data.text,
            "lang": data.lang
        }
    )    

    logger.info("The addition of connectors has been successfully done")

    return result

@router.post("/textual-tone-shifts")
async def submit_tool( data: AITextualToneShiftInputSchema, _ = Depends(key_check)):
    logger.info(f"Args. loaded successfully: {data}")

    textual_tone_shifts_workflow = complie_workflow_tone_shift()

    logger.info("Developing the Textual Tone Shift")

    result = textual_tone_shifts_workflow.invoke(
        {
            "text": data.text,
            "lang": data.lang,
            "target_tone": data.target_tone
        }
    )    

    logger.info("The textual tone shifting has been successfully done")

    return result

@router.post("/plagiarism-check")
async def submit_tool( data: AIPlagiarismCheckInputSchema, _ = Depends(key_check)):
    logger.info(f"Args. loaded successfully: {data}")

    plagiarism_check_workflow = complie_workflow_plagiarism_check()

    logger.info("Developing the Plagiarism Check")

    result = plagiarism_check_workflow.invoke(
        {
            "original_text": data.original_text,
            "comparison_text": data.comparison_text,
            "lang": data.lang
        }
    )    

    logger.info("The plagiarism check has been successfully done")

    return result