from fastapi import APIRouter

from mock_data.crops import CROP_PROFILES

router = APIRouter(tags=["crops"])


@router.get("/crops")
def list_crops() -> dict:
    return {
        "data_label": "Demo / Mock Data",
        "disclaimer": "Sample crop requirements for architecture demonstration only.",
        "crops": list(CROP_PROFILES.values()),
    }

