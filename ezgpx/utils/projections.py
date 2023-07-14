from math import pi, radians, floor, log, cos, sin, tan
from ..utils import EARTH_RADIUS


def web_mercator_projection(latitude: float, longitude: float, zoom_level: int = 1) -> tuple[int, int]:
    """
    https://en.wikipedia.org/wiki/Web_Mercator_projection

    Args:
        latitude (float): Point latitude.
        longitude (float): Point longitude.
        zoom_level (int, optional): Zoom level. Defaults to 1.

    Returns:
        tuple[int, int]: Point coordinates in the web-mercator projection.
    """

    # WARNING -> Poles: see link above

    # Convert latitude and longitude to radians
    latitude, longitude = radians(latitude), radians(longitude)

    # Compute coordinates
    const = (2**zoom_level)/(2 * pi)
    x = const * (longitude + pi)
    y = const * (pi - log(tan(pi/4 + latitude/2)))

    # return floor(x), floor(y)
    return x, y  # ???


def lambert_conformal_conic_projection(latitude: float, longitude: float, ref_latitude: float, ref_longitude: float, standard_parallel_1: float, standard_parallel_2: float) -> tuple[float, float]:
    """
    https://en.wikipedia.org/wiki/Lambert_conformal_conic_projection

    Args:
        latitude (float): Point latitude.
        longitude (float): Point longitude.
        ref_latitude (float): Reference point latitude.
        ref_longitude (float): Reference point longitude.
        standard_parallel_1 (float): First standard parallel.
        standard_parallel_2 (float): Second standard parallel.

    Returns:
        tuple[float, float]: Point coordinates in the Lambert conformal conic projection.
    """
    latitude = radians(latitude)
    longitude = radians(longitude)
    ref_latitude = radians(ref_latitude)
    ref_longitude = radians(ref_longitude)
    standard_parallel_1 = radians(standard_parallel_1)
    standard_parallel_2 = radians(standard_parallel_2)

    if standard_parallel_1 != standard_parallel_2:
        n = log(cos(standard_parallel_1) * (1/cos(standard_parallel_2))) / log(tan(0.75 *
                                                                                   pi + 0.5*standard_parallel_2) * (1/tan(0.75*pi + 0.5*standard_parallel_1)))
    else:
        n = sin(standard_parallel_1)

    F = cos(standard_parallel_1) * \
        (tan(0.75*pi + 0.5*standard_parallel_1))**n / n
    rho = EARTH_RADIUS*F*(1/tan(0.75*pi + 0.5*latitude))**n
    rho_0 = EARTH_RADIUS*F*(1/tan(0.75*pi + 0.5*ref_latitude))**n

    x = rho*sin(n*(longitude - ref_longitude))
    y = rho_0 - rho*cos(n*(longitude - ref_longitude))
    
    print(f"n={n}")
    print(f"F={F}")
    print(f"rho={rho}")
    print(f"rho_0={rho_0}")
    print(f"x,y={x},{y}")

    return x, y
