from math import pi, radians, floor, log, tan


def web_mercator_projection(latitude: float, longitude: float, zoom_level: int = 1) -> tuple[int, int]:
    """
    https://en.wikipedia.org/wiki/Web_Mercator_projection

    Args:
        latitude (float): _description_
        longitude (float): _description_
        zoom_level (int, optional): Zoom level. Defaults to 1.

    Returns:
        _type_: _description_
    """

    # WARNING -> Poles: see link above

    # Convert latitude and longitude to radians
    latitude, longitude = radians(latitude), radians(longitude)

    # Compute coordinates
    const = (2**zoom_level)/(2 * pi)
    x = const * (longitude + pi)
    y = const * (pi - log(tan(pi/4 + latitude/2)))

    return floor(x), floor(y)
