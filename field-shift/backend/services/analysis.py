from mock_data.crops import CROP_PROFILES
from mock_data.environment import climate_for, soil_for
from schemas.farm import AnalysisResponse, FarmInput, RotationResponse

DISCLAIMER = (
    "Architecture demonstration using illustrative rules and mock data. "
    "Scores are not scientifically validated forecasts or farming advice."
)


def _crop_scores(farm: FarmInput, soil: dict) -> list[dict]:
    water_per_dunam = farm.available_water_m3 / farm.area_dunams
    previous = farm.previous_crop.strip().lower()
    scores = []

    for key, crop in CROP_PROFILES.items():
        score = 72
        reasons = []

        if water_per_dunam >= crop["water_need_m3_per_dunam"]:
            score += 14
            reasons.append("demo water allocation meets the sample threshold")
        else:
            score -= min(28, int((crop["water_need_m3_per_dunam"] - water_per_dunam) * 1.2))
            reasons.append("sample water need may exceed the entered allocation")

        low_ph, high_ph = crop["preferred_ph"]
        if low_ph <= soil["ph"] <= high_ph:
            score += 8
            reasons.append("mock soil pH is within the preferred range")

        if key == previous:
            score -= 25
            reasons.append("penalized to avoid repeating the previous crop")
        elif crop["family"].lower() == "legume" and previous in {"wheat", "barley"}:
            score += 6
            reasons.append("a legume follows the previous cereal")

        scores.append(
            {
                "crop": crop["name"],
                "score": max(0, min(100, score)),
                "reason": "; ".join(reasons).capitalize() + ".",
                "water_need_m3_per_dunam": crop["water_need_m3_per_dunam"],
            }
        )

    return sorted(scores, key=lambda item: item["score"], reverse=True)[:3]


def analyze_farm(farm: FarmInput) -> AnalysisResponse:
    climate = climate_for(farm.latitude)
    soil = soil_for(farm.longitude)
    water_per_dunam = farm.available_water_m3 / farm.area_dunams
    crops = _crop_scores(farm, soil)

    water_level = "high" if water_per_dunam < 32 else "medium" if water_per_dunam < 45 else "low"
    heat_level = "medium" if climate["average_temperature_c"] > 24 else "low"

    return AnalysisResponse(
        data_label="Demo / Mock Data",
        disclaimer=DISCLAIMER,
        request_summary=farm,
        climate=climate,
        soil=soil,
        suggested_crops=crops,
        risks=[
            {
                "type": "Water pressure",
                "level": water_level,
                "note": f"Based on {water_per_dunam:.1f} m³ available per dunam.",
            },
            {
                "type": "Heat exposure",
                "level": heat_level,
                "note": "Inferred from the mock annual temperature profile.",
            },
            {
                "type": "Rotation fatigue",
                "level": "medium" if farm.previous_crop.lower() in {"wheat", "barley"} else "low",
                "note": "A simple crop-family repeat check; no field history is stored.",
            },
        ],
    )


def suggest_rotation(farm: FarmInput) -> RotationResponse:
    previous = farm.previous_crop.strip().lower()
    if previous in {"wheat", "barley"}:
        crops = ["Chickpea", "Sunflower", "Barley"]
    elif previous in {"tomato", "potato", "pepper"}:
        crops = ["Barley", "Chickpea", "Sunflower"]
    else:
        crops = ["Chickpea", "Barley", "Tomato"]

    explanations = [
        f"Switches away from the previous {farm.previous_crop} crop and introduces a legume.",
        "Changes crop family and uses a deeper-rooted sample crop.",
        "Returns to a market crop after two contrasting seasons.",
    ]
    periods = ["Winter 2026", "Summer 2027", "Winter 2027"]

    return RotationResponse(
        data_label="Demo / Mock Data",
        disclaimer=DISCLAIMER,
        plan_name="Balanced three-season demo",
        seasons=[
            {"season": index + 1, "period": periods[index], "crop": crop, "explanation": explanations[index]}
            for index, crop in enumerate(crops)
        ],
    )

