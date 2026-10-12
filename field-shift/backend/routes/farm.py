from fastapi import APIRouter

from schemas.farm import AnalysisResponse, FarmInput
from services.analysis import analyze_farm

router = APIRouter(tags=["farm analysis"])


@router.post("/farm/analyze", response_model=AnalysisResponse)
def analyze(payload: FarmInput) -> AnalysisResponse:
    return analyze_farm(payload)

