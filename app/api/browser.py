from fastapi import APIRouter, HTTPException

from app.services.version_service import VersionService

router = APIRouter(
    prefix="/documents",
    tags=["Browse"]
)

version_service = VersionService()


@router.get("/{document_id}/sections")
def get_top_level_sections(
    document_id: int,
    version: str = "latest"
):

    if version == "latest":
        version_id = version_service.get_latest_version_id(document_id)
    else:
        version_id = version_service.get_version_id(
            document_id,
            int(version)
        )

    if version_id is None:
        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    sections = version_service.get_top_level_sections(version_id)

    return [
        {
            "logical_node_id": row["logical_node_id"],
            "title": row["title"],
            "type": row["type"],
            "level": row["level"]
        }
        for row in sections
    ]