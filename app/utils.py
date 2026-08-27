def get_aqi_category(aqi):
    """
    OpenWeather AQI scale:

    1 = Good
    2 = Fair
    3 = Moderate
    4 = Poor
    5 = Very Poor
    """

    if aqi < 1.5:
        return "Good"

    elif aqi < 2.5:
        return "Fair"

    elif aqi < 3.5:
        return "Moderate"

    elif aqi < 4.5:
        return "Poor"

    else:
        return "Very Poor"


def get_health_advisory(category):

    advisories = {

        "Good":
            "Air quality is good. Outdoor activities are generally safe.",

        "Fair":
            "Air quality is acceptable for most people.",

        "Moderate":
            "Sensitive individuals should consider reducing prolonged outdoor exposure.",

        "Poor":
            "Consider limiting prolonged outdoor activities.",

        "Very Poor":
            "Avoid prolonged outdoor exposure and take appropriate precautions."
    }

    return advisories.get(
        category,
        "No health advisory available."
    )