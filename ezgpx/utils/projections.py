from math import pi, floor, log, tan


def deg_to_rad(latitude: float, longitude: float):
    return (latitude * pi)/180, (longitude*pi)/180


def web_mercator_projection(latitude: float, longitude: float, zoom_level: int = 1):
    """
    https://en.wikipedia.org/wiki/Web_Mercator_projection

    Args:
        latitude (_type_): _description_
        float (_type_): _description_
    """

    # WARNING -> Poles: see link above

    # Convert latitude and longitude to radians
    latitude, longitude = deg_to_rad(latitude, longitude)

    # Compute coordinates
    const = (2**zoom_level)/(2 * pi)
    x = const * (longitude + pi)
    y = const * (pi - log(tan(pi/4 + latitude/2)))

    return floor(x), floor(y)
