from fastapi import APIRouter

from schemas.farm import FarmInput, RotationResponse
from services.analysis import suggest_rotation

router = APIRouter(tags=["rotation"])


@router.post("/rotation/suggest", response_model=RotationResponse)
def rotation(payload: FarmInput) -> RotationResponse:
    return suggest_rotation(payload)

