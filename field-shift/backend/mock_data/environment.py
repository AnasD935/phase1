def climate_for(latitude: float) -> dict:
    """Return a deterministic demo climate band based only on latitude."""
    absolute_latitude = abs(latitude)
    if absolute_latitude < 23.5:
        return {
            "annual_rainfall_mm": 610,
            "average_temperature_c": 25.4,
            "growing_season": "October–May",
            "source": "Demo climate profile (future: NASA POWER)",
        }
    if absolute_latitude < 38:
        return {
            "annual_rainfall_mm": 420,
            "average_temperature_c": 20.8,
            "growing_season": "November–June",
            "source": "Demo climate profile (future: NASA POWER)",
        }
    return {
        "annual_rainfall_mm": 690,
        "average_temperature_c": 13.6,
        "growing_season": "April–September",
        "source": "Demo climate profile (future: NASA POWER)",
    }


def soil_for(longitude: float) -> dict:
    """Return a deterministic demo soil profile based only on longitude."""
    index = int(abs(longitude)) % 3
    profiles = [
        {"texture": "Clay loam", "ph": 7.4, "organic_matter_percent": 2.1},
        {"texture": "Sandy loam", "ph": 6.8, "organic_matter_percent": 1.6},
        {"texture": "Silt loam", "ph": 7.1, "organic_matter_percent": 2.7},
    ]
    return {**profiles[index], "source": "Demo soil profile (future: SoilGrids)"}

