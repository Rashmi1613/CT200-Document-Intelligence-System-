from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.selection_service import SelectionService

router = APIRouter(
    prefix="/selections",
    tags=["Selections"]
)


class SelectionRequest(BaseModel):

    name: str

    document_id: int

    version: int

    logical_node_ids: list[int]


@router.post("/")
def create_selection(request: SelectionRequest):

    service = SelectionService()

    version_id = service.get_document_version_id(
        request.document_id,
        request.version
    )

    if version_id is None:

        raise HTTPException(
            status_code=404,
            detail="Document version not found"
        )

    selection_id = service.create_selection(
        request.name,
        version_id,
        request.logical_node_ids
    )

    return {
        "selection_id": selection_id,
        "name": request.name
    }


@router.get("/{selection_id}")
def get_selection(selection_id: int):

    service = SelectionService()

    selection = service.get_selection(selection_id)

    if selection is None:

        raise HTTPException(
            status_code=404,
            detail="Selection not found"
        )

    node_ids = service.get_node_ids(selection_id)

    nodes = service.get_nodes(
        selection["document_version_id"],
        node_ids
    )

    return {

        "selection_id": selection["id"],

        "name": selection["name"],

        "version": selection["version_number"],

        "nodes": nodes
    }