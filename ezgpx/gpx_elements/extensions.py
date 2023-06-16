
class Extensions():
    """
    Track extensions.
    """

    def __init__(
            self,
            display_color: str = "Cyan",
            distance: float = None,
            total_elapsed_time: float = None,
            moving_time: float = None,
            stopped_time: float = None,
            moving_speed: float = None,
            max_speed: float = None,
            max_elevation: float = None,
            min_elevation: float = None,
            ascent: float = None,
            descent: float = None,
            avg_ascent_rate: float = None,
            max_ascent_rate: float = None,
            avg_descent_rate: float = None,
            max_descent_rate: float = None) -> None:
        self.display_color: str = display_color
        self.distance: float = distance
        self.total_elapsed_time: float = total_elapsed_time # int?
        self.moving_time: float = moving_time # int?
        self.stopped_time: float = stopped_time
        self.moving_speed: float = moving_speed
        self.max_speed: float = max_speed
        self.max_elevation: float = max_elevation
        self.min_elevation: float = min_elevation
        self.ascent: float = ascent
        self.descent: float = descent
        self.avg_ascent_rate: float = avg_ascent_rate
        self.max_ascent_rate: float = max_ascent_rate
        self.avg_descent_rate: float = avg_descent_rate
        self.max_descent_rate: float = max_descent_rate
