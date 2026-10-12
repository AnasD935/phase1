from typing import Literal

from pydantic import BaseModel, Field


class FarmInput(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    area_dunams: float = Field(gt=0, le=100_000)
    available_water_m3: float = Field(ge=0, le=100_000_000)
    previous_crop: str = Field(min_length=2, max_length=50)


class ClimateData(BaseModel):
    annual_rainfall_mm: int
    average_temperature_c: float
    growing_season: str
    source: str


class SoilData(BaseModel):
    texture: str
    ph: float
    organic_matter_percent: float
    source: str


class Risk(BaseModel):
    type: str
    level: Literal["low", "medium", "high"]
    note: str


class CropSuggestion(BaseModel):
    crop: str
    score: int = Field(ge=0, le=100)
    reason: str
    water_need_m3_per_dunam: int


class AnalysisResponse(BaseModel):
    data_label: str
    disclaimer: str
    request_summary: FarmInput
    climate: ClimateData
    soil: SoilData
    suggested_crops: list[CropSuggestion]
    risks: list[Risk]


class RotationSeason(BaseModel):
    season: int
    period: str
    crop: str
    explanation: str


class RotationResponse(BaseModel):
    data_label: str
    disclaimer: str
    plan_name: str
    seasons: list[RotationSeason]

