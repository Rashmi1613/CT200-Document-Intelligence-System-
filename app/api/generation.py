from fastapi import APIRouter, HTTPException

from app.services.generation_service import GenerationService
from app.services.llm_service import LLMService

router = APIRouter(
    prefix="/generations",
    tags=["Generation"]
)

# Replace with your API key loading method
llm = LLMService(api_key="YOUR_GEMINI_API_KEY")


@router.post("/{selection_id}")
def generate(selection_id: int):

    service = GenerationService()

    data = service.build_context(selection_id)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Selection not found"
        )

    existing = service.find_existing_generation(
        selection_id,
        data["source_hash"]
    )

    if existing:

        return {

            "message": "Existing generation returned.",

            "generation_id": existing["id"],

            "status": existing["status"]

        }

    result = llm.generate(
        data["context"]
    )

    generation_id = service.save_generation(

        selection_id=selection_id,

        source_hash=data["source_hash"],

        prompt=result["prompt"],

        response=result["response"],

        model_name="gemini-2.5-flash",

        status=result["status"]

    )

    return {

        "generation_id": generation_id,

        "status": result["status"],

        "test_cases": result["parsed"]

    }