
class Extensions():
    """
    extensionsType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "extensions",
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
        """
        Initialize Extensions instance.

        Args:
            tag (str, optional): XML tag. Defaults to "extensions".
            display_color (str, optional): Display color. Defaults to "Cyan".
            distance (float, optional): Distance. Defaults to None.
            total_elapsed_time (float, optional): Total elapsed time. Defaults to None.
            moving_time (float, optional): Moving time. Defaults to None.
            stopped_time (float, optional): Stopped time. Defaults to None.
            moving_speed (float, optional): Moving speed. Defaults to None.
            max_speed (float, optional): Maximum speed. Defaults to None.
            max_elevation (float, optional): Maximum elevation. Defaults to None.
            min_elevation (float, optional): Minimum elevation. Defaults to None.
            ascent (float, optional): Ascent. Defaults to None.
            descent (float, optional): Descent. Defaults to None.
            avg_ascent_rate (float, optional): Average ascent rate. Defaults to None.
            max_ascent_rate (float, optional): Maximum ascent rate. Defaults to None.
            avg_descent_rate (float, optional): Average descent rate. Defaults to None.
            max_descent_rate (float, optional): Maximum descent rate. Defaults to None.
        """
        self.tag: str = tag
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
