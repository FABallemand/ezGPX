
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

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "extensions"
        display_color : str, optional
            Display color, by default "Cyan"
        distance : float, optional
            Distance, by default None
        total_elapsed_time : float, optional
            Total elapsed time, by default None
        moving_time : float, optional
            Moving time, by default None
        stopped_time : float, optional
            Stopped time, by default None
        moving_speed : float, optional
            Moving speed, by default None
        max_speed : float, optional
            Maximum speed, by default None
        max_elevation : float, optional
            Maximum elevation, by default None
        min_elevation : float, optional
            Minimum elevation, by default None
        ascent : float, optional
            Ascent, by default None
        descent : float, optional
            Descent, by default None
        avg_ascent_rate : float, optional
            Average ascent rate, by default None
        max_ascent_rate : float, optional
            Maximum ascent rate, by default None
        avg_descent_rate : float, optional
            Average descent rate, by default None
        max_descent_rate : float, optional
            Maximum descent rate, by default None
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
