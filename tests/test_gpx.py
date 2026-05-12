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

FILE_DIR = os.path.realpath(os.path.dirname(__file__))
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import GPX, Latitude, Longitude, Wpt  # pylint: disable=wrong-import-position

REAL_FILES_DIR = os.path.join(FILE_DIR, "files/real/")
REFERENCE_FILES_DIR = os.path.join(FILE_DIR, "files/reference/")
SYNTHETIC_FILES_DIR = os.path.join(FILE_DIR, "files/synthetic/")
TMP_DIR = os.path.join(FILE_DIR, "tmp")


class TestGPX:

    def test_init(self):
        # Create temporary folder
        rmtree(TMP_DIR, True)
        os.makedirs(TMP_DIR)

    ###############################################################################
    #### Parsing ##################################################################
    ###############################################################################

    @pytest.mark.parametrize(
        "file",
        [
            pytest.param("bounds.gpx", id="bounds"),
            pytest.param("copyright.gpx", id="copyright"),
            pytest.param("email.gpx", id="email"),
            pytest.param("gpx.gpx", id="gpx"),
            pytest.param("link.gpx", id="link"),
            pytest.param("metadata.gpx", id="metadata"),
            pytest.param("person.gpx", id="person"),
            pytest.param("rte.gpx", id="rte"),
            pytest.param("trk.gpx", id="trk"),
            pytest.param("trkseg.gpx", id="trkseg"),
            pytest.param("wpt.gpx", id="wpt"),
        ],
    )
    def test_parsing_mandatory(self, benchmark, file):
        benchmark(
            GPX,
            os.path.join(SYNTHETIC_FILES_DIR, "mandatory", file),
            xml_schema=False,
            xml_extensions_schemas=False,
        )

    @pytest.mark.parametrize(
        "file",
        [
            pytest.param("bounds.gpx", id="bounds"),
            pytest.param("copyright.gpx", id="copyright"),
            pytest.param("email.gpx", id="email"),
            # pytest.param("gpx.gpx", id="gpx"),  # TODO
            pytest.param("link.gpx", id="link"),
            pytest.param("metadata.gpx", id="metadata"),
            pytest.param("person.gpx", id="person"),
            pytest.param("rte.gpx", id="rte"),
            pytest.param("trk.gpx", id="trk"),
            pytest.param("trkseg.gpx", id="trkseg"),
            pytest.param("wpt.gpx", id="wpt"),
        ],
    )
    def test_parsing_all(self, benchmark, file):
        benchmark(
            GPX,
            os.path.join(SYNTHETIC_FILES_DIR, "all", file),
            xml_schema=False,
            xml_extensions_schemas=False,
        )

    ###############################################################################
    #### Schemas ##################################################################
    ###############################################################################

    @pytest.mark.parametrize(
        "file,expected",
        [
            pytest.param("gpx.gpx", True),
            # pytest.param("invalid_schema.gpx", False),  # TODO
        ],
    )
    def test_check_schemas(self, benchmark, file, expected):
        gpx = GPX(
            os.path.join(SYNTHETIC_FILES_DIR, "all", file),
            xml_schema=False,
            xml_extensions_schemas=False,
        )
        result = benchmark(gpx.check_xml_schema)
        assert result is expected

    ###############################################################################
    #### Metadata #################################################################
    ###############################################################################

    # def test_file_name(self, benchmark):
    #     gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
    #     result = benchmark(gpx.name)
    #     assert result == "test-name"

    # def test_set_file_name(self, benchmark):
    #     gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
    #     benchmark(gpx.set_name, "new-test-name")
    #     assert gpx.name() == "new-test-name"

    ###############################################################################
    #### Points ###################################################################
    ###############################################################################

    def test_trkpt_count(self, benchmark):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        result = benchmark(gpx.trkpt_count)
        assert result == 4

    def test_trkpt_bounds(self, benchmark):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        result = benchmark(gpx.trkpt_bounds)
        assert result == (Latitude(0), Longitude(0), Latitude(1), Longitude(1))

    def test_trkpt_center(self, benchmark):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        result = benchmark(gpx.trkpt_center)
        assert result == (Latitude(0.5), Longitude(0.5))

    def test_trkpt_extreme(self, benchmark):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        min_lat, min_lon, max_lat, max_lon = benchmark(gpx.trkpt_extreme)
        assert min_lat.lat == Latitude(0)
        assert min_lon.lon == Longitude(0)
        assert max_lat.lat == Latitude(1)
        assert max_lon.lon == Longitude(1)

    ###############################################################################
    #### Distance and Elevation ###################################################
    ###############################################################################

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

    ###############################################################################
    #### Time #####################################################################
    ###############################################################################

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

    ###############################################################################
    #### Speed and Pace ###########################################################
    ###############################################################################

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

    ###############################################################################
    #### Data Removal #############################################################
    ###############################################################################

    # TODO

    ###############################################################################
    #### Error Correction #########################################################
    ###############################################################################

    # TODO

    ###############################################################################
    #### Simplification ###########################################################
    ###############################################################################

    # TODO

    ###############################################################################
    #### Merge ####################################################################
    ###############################################################################

    # TODO

    ###############################################################################
    #### Exports ##################################################################
    ###############################################################################

    @pytest.mark.parametrize(
        "values, as_series, expected",
        [
            pytest.param(
                None, False, {"lat": [0.0, 1.0, 0.0, 1.0], "lon": [0.0, 1.0, 0.0, 1.0]}
            ),
            pytest.param(
                ["lat", "lon", "ele"],
                False,
                {
                    "lat": [0.0, 1.0, 0.0, 1.0],
                    "lon": [0.0, 1.0, 0.0, 1.0],
                    "ele": [0.0, 1.0, 0.0, 1.0],
                },
            ),
            # TODO as_series?
            # TODO all attributes?
        ],
    )
    def test_to_dict(self, benchmark, values, as_series, expected):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        d = benchmark(gpx.to_dict, values, as_series)
        assert d == expected

    @pytest.mark.parametrize(
        "values, expected",
        [
            pytest.param(
                None,
                [
                    {"lat": 0.0, "lon": 0.0},
                    {"lat": 1.0, "lon": 1.0},
                    {"lat": 0.0, "lon": 0.0},
                    {"lat": 1.0, "lon": 1.0},
                ],
            ),
            pytest.param(
                ["lat", "lon", "ele"],
                [
                    {"lat": 0.0, "lon": 0.0, "ele": 0.0},
                    {"lat": 1.0, "lon": 1.0, "ele": 1.0},
                    {"lat": 0.0, "lon": 0.0, "ele": 0.0},
                    {"lat": 1.0, "lon": 1.0, "ele": 1.0},
                ],
            ),
            # TODO all attributes?
        ],
    )
    def test_to_dicts(self, benchmark, values, expected):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        d = benchmark(gpx.to_dicts, values)
        assert d == expected

    # def test_to_dict_df(self)  # TODO?

    @pytest.mark.parametrize(
        "values, reference_file",
        [
            pytest.param(None, "gpx_mandatory.csv"),
            pytest.param(Wpt._fields, "gpx_all.csv"),
        ],
    )
    def test_to_pandas(self, benchmark, values, reference_file):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        df = benchmark(gpx.to_pandas, values)
        reference_df = pd.read_csv(
            os.path.join(REFERENCE_FILES_DIR, reference_file)
        ).replace({float("nan"): None})
        assert reference_df.equals(df)

    @pytest.mark.parametrize(
        "values, reference_file",
        [
            pytest.param(None, "gpx_mandatory.csv"),
            pytest.param(Wpt._fields, "gpx_all.csv"),
        ],
    )
    def test_to_polars(self, benchmark, values, reference_file):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        df = benchmark(gpx.to_polars, values)
        reference_df = pl.read_csv(
            os.path.join(REFERENCE_FILES_DIR, reference_file)
        ).fill_nan(None)
        assert reference_df.equals(df)

    def test_to_gpx(self, benchmark):  # TODO more examples
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        benchmark(gpx.to_gpx, os.path.join(TMP_DIR, "gpx.gpx"))
        assert filecmp.cmp(
            os.path.join(TMP_DIR, "gpx.gpx"),
            os.path.join(REFERENCE_FILES_DIR, "gpx_all.gpx"),
            False,
        )

    # def test_to_kml(self, benchmark):  # TODO
    #     gpx = GPX(os.path.join(REAL_FILES_DIR, "strava_run_1.gpx"))
    #     benchmark(gpx.to_kml, "tmp/strava_run_1_test.kml", styles=None)
    #     assert filecmp.cmp(
    #         "tmp/strava_run_1_test.kml",
    #         os.path.join(REFERENCE_FILES_DIR, "strava_run_1.kml"),
    #         False,
    #     )

    @pytest.mark.parametrize(
        "values, reference_file",
        [
            pytest.param(None, "gpx_mandatory.csv"),
            pytest.param(Wpt._fields, "gpx_all.csv"),
        ],
    )
    def test_to_csv(self, benchmark, values, reference_file):
        gpx = GPX(os.path.join(SYNTHETIC_FILES_DIR, "all", "gpx.gpx"))
        benchmark(
            gpx.to_csv,
            os.path.join(TMP_DIR, reference_file),
            values,
        )
        assert filecmp.cmp(
            os.path.join(TMP_DIR, reference_file),
            os.path.join(REFERENCE_FILES_DIR, reference_file),
            False,
        )

    # ==== Plots ===============================================================

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

    # ==== Destroy =============================================================

    def test_destroy(self, remove_tmp: bool = False):
        # Remove temporary folder
        if remove_tmp:
            rmtree(TMP_DIR, True)

    # ==== Test ================================================================

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
