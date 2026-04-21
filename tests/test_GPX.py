# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the GPX class.
"""

import datetime
import filecmp
import os
import sys
from shutil import rmtree

import pandas as pd
import polars as pl
import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import GPX  # pylint: disable=wrong-import-position

REAL_FILES_DIR = "files/real/"
REFERENCE_FILES_DIR = "files/reference/"
SYNTHETIC_FILES_DIR = "files/synthetic/"
TMP_DIR = os.path.join(FILE_DIR, "tmp")


class TestGPX:
    # ==== Init ===============================================================#

    def test_init(self):
        # Create temporary folder
        rmtree(TMP_DIR, True)
        os.makedirs(TMP_DIR)

    # ==== Parsing ============================================================#

    @pytest.mark.parametrize(
        "file",
        [
            pytest.param("gpx.gpx", id="gpx"),
            pytest.param("metadata.gpx", id="metadata"),
            pytest.param("rte.gpx", id="rte"),
            pytest.param("trk.gpx", id="trk"),
            pytest.param("wpt.gpx", id="wpt"),
        ],
    )
    def test_parsing(self, benchmark, file):
        gpx = benchmark(
            GPX,
            os.path.join(SYNTHETIC_FILES_DIR, file),
            xml_schema=False,
            xml_extensions_schemas=False,
        )

    # ==== Check Schemas ======================================================#

    @pytest.mark.parametrize(
        "file,expected",
        [
            pytest.param("strava_run_1.gpx", True),
            pytest.param("invalid_schema.gpx", False),
        ],
    )
    def test_check_schemas(self, benchmark, file, expected):
        gpx = GPX(
            os.path.join(REAL_FILES_DIR, file),
            xml_schema=False,
            xml_extensions_schemas=False,
        )
        result = benchmark(gpx.check_xml_schema)
        assert result is expected

    # ==== Properties =========================================================#

    def test_name(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.name)
        assert result == "Dérouillage habituel 💥"

    def test_set_name(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        benchmark(gpx.set_name, "test")
        assert gpx.name() == "test"

    def test_nb_points(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.nb_points)
        assert result == 939

    @pytest.mark.parametrize(
        "trkpt_index,expected",
        [
            pytest.param(0, "WayPoint[trkpt](44.043332, 4.453089)", id="first_point"),
            pytest.param(-1, "WayPoint[trkpt](44.043391, 4.453165)", id="last_point"),
            pytest.param(42, "WayPoint[trkpt](44.046162, 4.449441)", id="random_point"),
        ],
    )
    def test_get_trkpt(self, benchmark, trkpt_index, expected):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.get_trkpt, 0, 0, trkpt_index)
        assert str(result) == expected

    def test_bounds(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.bounds)
        assert result == (44.032965, 4.444134, 44.047778, 4.486607)

    def test_center(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.center)
        assert result == (44.0403715, 4.465370500000001)

    def test_distance(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.distance)
        assert result == 10922.788757238777

    def test_ascent(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.ascent)
        assert result == 225.29999999999995

    def test_descent(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.descent)
        assert result == 224.79999999999987

    def test_max_descent_rate(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.max_descent_rate)
        assert result == -38.54138626353898

    def test_max_ascent_rate(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.max_ascent_rate)
        assert result == 51.2919872933083

    def test_min_elevation(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.min_elevation)
        assert result == 98.5

    def test_max_elevation(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.max_elevation)
        assert result == 235.6

    def test_start_time(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.start_time)
        assert result == datetime.datetime(
            2023,
            5,
            22,
            8,
            4,
            58,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200), "CEST"),
        )

    def test_stop_time(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.stop_time)
        assert result == datetime.datetime(
            2023,
            5,
            22,
            9,
            6,
            25,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200), "CEST"),
        )

    def test_total_elapsed_time(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.total_elapsed_time)
        assert result == datetime.timedelta(seconds=3687)

    def test_stopped_time(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.stopped_time)
        assert result == datetime.timedelta(seconds=104)

    def test_moving_time(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.moving_time)
        assert result == gpx.moving_time()

    @pytest.mark.parametrize(
        "moving,expected",
        [
            pytest.param(False, 10.66505004775145),
            pytest.param(True, 10.974613320139435),
        ],
    )
    def test_avg_speed(self, benchmark, moving, expected):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.avg_speed, moving)
        assert result == expected

    def test_min_speed(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.min_speed)
        assert result == 0.0

    def test_max_speed(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.max_speed)
        assert result == 19.69510525631602

    @pytest.mark.parametrize(
        "moving,expected",
        [
            pytest.param(False, 5.625852643105975),
            pytest.param(True, 5.467163010645161),
        ],
    )
    def test_avg_pace(self, benchmark, moving, expected):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.avg_pace, moving)
        assert result == expected

    def test_min_pace(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.min_pace)
        assert result == 0.0

    def test_max_pace(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.max_pace)
        assert result == 1041.2956304834424

    def test_min_ascent_speed(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.min_ascent_speed)
        assert result == -3359.9999999999794

    def test_max_ascent_speed(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        result = benchmark(gpx.max_ascent_speed)
        assert result == 2159.9999999999797

    # ==== Modifications ======================================================#

    # ==== Conversion and Saving ==============================================#

    def test_to_pandas(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        df = benchmark(gpx.to_pandas, values=["lat", "lon", "ele", "time"])
        reference_df = pd.read_csv(
            os.path.join(REFERENCE_FILES_DIR, "strava_run_1.csv")
        )
        assert reference_df.equals(df)

    def test_to_polars(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        df = benchmark(gpx.to_polars, values=["lat", "lon", "ele", "time"])
        reference_df = pl.read_csv(
            os.path.join(REFERENCE_FILES_DIR, "strava_run_1.csv")
        )
        assert reference_df.equals(df)

    def test_to_gpx(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        benchmark(gpx.to_gpx, "tmp/strava_run_1_test.gpx")
        assert filecmp.cmp(
            "tmp/strava_run_1_test.gpx",
            os.path.join(REFERENCE_FILES_DIR, "strava_run_1.gpx"),
            False,
        )

    def test_to_kml(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        benchmark(gpx.to_kml, "tmp/strava_run_1_test.kml", styles=None)
        assert filecmp.cmp(
            "tmp/strava_run_1_test.kml",
            os.path.join(REFERENCE_FILES_DIR, "strava_run_1.kml"),
            False,
        )

    def test_to_csv(self, benchmark):
        gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        benchmark(
            gpx.to_csv,
            "tmp/strava_run_1_test.csv",
            values=["lat", "lon", "ele", "time"],
        )
        assert filecmp.cmp(
            "tmp/strava_run_1_test.csv",
            os.path.join(REFERENCE_FILES_DIR, "strava_run_1.csv"),
            False,
        )

    # ==== Plots ==============================================================#

    # def _test_matplotlib_plot_1(self):
    #     # Plot
    #     self.gpx.matplotlib_plot(
    #         start_stop_colors=None, color="#ffffff", title="Track",
    #         file_path="tmp/matplotlib_strava_run_1.png")
    #     # Load images
    #     test_img = plt.imread("tmp/matplotlib_strava_run_1.png")
    #     ref_img = plt.imread(
    #         os.path.join(REFERENCE_FILES_DIR,
    #                      "matplotlib_strava_run_1.png"))
    #     # Compare images
    #     return np.array_equal(test_img, ref_img)

    # def _test_matplotlib_plot_2(self):
    #     # Plot
    #     self.gpx.matplotlib_plot(
    #         start_stop_colors=("#00FF00", "#FF0000"), color="#ffffff",
    #         title="Track", file_path="tmp/matplotlib_strava_run_1_start_stop.png")
    #     # Load images
    #     test_img = plt.imread("tmp/matplotlib_strava_run_1_start_stop.png")
    #     ref_img = plt.imread(
    #         os.path.join(REFERENCE_FILES_DIR,
    #                      "matplotlib_strava_run_1_start_stop.png"))

    #     # Compare images
    #     return np.array_equal(test_img, ref_img)

    # def _test_matplotlib_plot_3(self):
    #     # Plot
    #     self.gpx.matplotlib_plot(
    #         start_stop_colors=None, color=True, title="Track",
    #         file_path="tmp/matplotlib_strava_run_1_elevation.png")
    #     # Load images
    #     test_img = plt.imread("tmp/matplotlib_strava_run_1_elevation.png")
    #     ref_img = plt.imread(
    #         os.path.join(REFERENCE_FILES_DIR,
    #                      "matplotlib_strava_run_1_elevation.png"))
    #     # Compare images
    #     return np.array_equal(test_img, ref_img)

    # def _test_matplotlib_plot_4(self):
    #     # Plot
    #     self.gpx.matplotlib_plot(
    #         start_stop_colors=("#00FF00", "#FF0000"), color=True, title="Track",
    #         file_path="tmp/matplotlib_strava_run_1_start_stop_elevation.png")
    #     # Load images
    #     test_img = plt.imread("tmp/matplotlib_strava_run_1_start_stop_elevation.png")
    #     ref_img = plt.imread(
    #         os.path.join(REFERENCE_FILES_DIR,
    #                      "matplotlib_strava_run_1_start_stop_elevation.png"))
    #     # Compare images
    #     return np.array_equal(test_img, ref_img)

    # @pytest.mark.skip(reason="not ready")
    # def test_matplotlib_plot(self):
    #     # Parse GPX file
    #     self.gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
    #     # Tests
    #     assert self._test_matplotlib_plot_1()
    #     assert self._test_matplotlib_plot_2()
    #     assert self._test_matplotlib_plot_3()
    #     assert self._test_matplotlib_plot_4()
    #     # self._test_matplotlib_plot_1()
    #     # self._test_matplotlib_plot_2()
    #     # self._test_matplotlib_plot_3()
    #     # self._test_matplotlib_plot_4()

    # def _test_folium_plot_1(self):
    #     # Plot
    #     self.gpx.folium_plot(tiles="openStreetMap",
    #                          color="#110000",
    #                          start_stop_colors=None,
    #                          waypoints_color=None,
    #                          minimap=False,
    #                          coord_popup=False,
    #                          title=None,
    #                          zoom=12,
    #                          file_path="tmp/folium_strava_run_1.html",
    #                          open=False)
    #     # Compare files
    #     return filecmp.cmp("tmp/folium_strava_run_1.html",
    #                        os.path.join(REFERENCE_FILES_DIR,
    #                                     "folium_strava_run_1.html"), False)

    # @pytest.mark.skip(reason="not ready")
    # def test_folium_plot(self):
    #     self.test_init() # For developping purpose only (using: pytest test_GPX.py::TestGPX::test_folium_plot)
    #     # Parse GPX file
    #     self.gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
    #     # Tests
    #     assert self._test_folium_plot_1()
    #     # assert self._test_folium_plot_2())
    #     # assert self._test_folium_plot_3())
    #     # assert self._test_folium_plot_4())
    #     # self._test_folium_plot_1()
    #     # self._test_folium_plot_2()
    #     # self._test_folium_plot_3()
    #     # self._test_folium_plot_4()

    # ==== Destroy ============================================================#

    def test_destroy(self, remove_tmp: bool = True):
        # Remove temporary folder
        if remove_tmp:
            rmtree(TMP_DIR, True)

    # ==== Test ===============================================================#

    @pytest.mark.skip(
        reason="test"
    )  # https://docs.pytest.org/en/7.3.x/how-to/skipping.html
    def test_test(self, remove_tmp: bool = True):
        # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")
        # Parse GPX file
        self.gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
        # Remove temporary folder
        if remove_tmp:
            rmtree("tmp")
