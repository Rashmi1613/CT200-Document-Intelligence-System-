from fastapi import APIRouter, HTTPException

from app.services.version_service import VersionService

router = APIRouter(
    prefix="/documents",
    tags=["Browse"]
)



@router.get("/{document_id}/sections")
def get_top_level_sections(
    document_id: int,
    version: str = "latest"
):
    version_service = VersionService()

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


@router.get("/nodes/{logical_node_id}")
def get_node(
    logical_node_id: int,
    document_id: int,
    version: str = "latest"
):

    version_service = VersionService()

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

    node = version_service.get_node(
        version_id,
        logical_node_id
    )

    if node is None:
        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    children = version_service.get_children(
        version_id,
        logical_node_id
    )

    return {
        "logical_node_id": node["logical_node_id"],
        "parent_id": node["parent_id"],
        "title": node["title"],
        "type": node["type"],
        "level": node["level"],
        "content": node["content"],
        "content_hash": node["content_hash"],
        "children": [
            {
                "logical_node_id": child["logical_node_id"],
                "title": child["title"],
                "type": child["type"],
                "level": child["level"]
            }
            for child in children
        ]
    }
    
@router.get("/{document_id}/search")
def search_document(
    document_id: int,
    q: str,
    version: str = "latest"
):

    version_service = VersionService()

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

    results = version_service.search_sections(
        version_id,
        q
    )

    return [
        {
            "logical_node_id": row["logical_node_id"],
            "title": row["title"],
            "type": row["type"],
            "level": row["level"],
            "content": row["content"]
        }
        for row in results
    ]
@router.get("/{document_id}/compare")
def compare_versions(
    document_id: int,
    logical_node_id: int,
    from_version: int,
    to_version: int
     ):

    version_service = VersionService()

    from_version_id = version_service.get_version_id(
        document_id,
        from_version
    )

    to_version_id = version_service.get_version_id(
        document_id,
        to_version
    )

    if from_version_id is None or to_version_id is None:
        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    old_node = version_service.get_node_by_version(
        from_version_id,
        logical_node_id
    )

    new_node = version_service.get_node_by_version(
        to_version_id,
        logical_node_id
    )

    if old_node is None or new_node is None:
        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    changed = (
        old_node["content_hash"] !=
        new_node["content_hash"]
    )

    return {
        "logical_node_id": logical_node_id,
        "changed": changed,
        "old_hash": old_node["content_hash"],
        "new_hash": new_node["content_hash"],
        "old_content": old_node["content"],
        "new_content": new_node["content"]
    }