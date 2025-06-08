import filecmp
import os
import sys
from shutil import rmtree

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

file_folder = os.path.dirname(__file__)
parent_folder = os.path.realpath(os.path.dirname(file_folder))  # ie: ezGPX

os.chdir(file_folder)
sys.path.append(parent_folder + "/ezgpx")

from ezgpx import GPX

FILES_DIRECTORY = "test_files/files/"
REFERENCE_FILES_DIRECTORY = "test_files/reference_files/"


class TestGPX:

    # ==== Init ===============================================================#

    def test_init(self):
        # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")

    # ==== Parsing/Writing ====================================================#

    def test_parse(self):
        # Parse GPX files
        gpx = GPX(
            os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"),
            xml_schema=True,
            xml_extensions_schemas=False,
        )
        invalid_gpx = GPX(
            os.path.join(FILES_DIRECTORY, "invalid_schema.gpx"),
            xml_schema=False,
            xml_extensions_schemas=False,
        )

    # ==== Check Schemas ======================================================#

    def test_check_schemas(self):
        # Parse GPX Files
        gpx = GPX(
            os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"),
            xml_schema=False,
            xml_extensions_schemas=False,
        )
        invalid_gpx = GPX(
            os.path.join(FILES_DIRECTORY, "invalid_schema.gpx"),
            xml_schema=False,
            xml_extensions_schemas=False,
        )
        # Tests
        assert gpx.check_xml_schema() is True
        assert invalid_gpx.check_xml_schema() is False

    # ==== Properties =========================================================#

    def test_file_name(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.file_name == "strava_run_1.gpx"

    def test_name(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.name() == "Dérouillage habituel 💥"

    def test_set_name(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        new_name = "test"
        gpx.set_name(new_name)
        assert gpx.name() == new_name

    def test_nb_points(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.nb_points() == 939

    @pytest.mark.skip(reason="nothing to test")
    def test_first_point(self):
        pass

    @pytest.mark.skip(reason="nothing to test")
    def test_last_point(self):
        pass

    def test_bounds(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.bounds() == (44.032965, 4.444134, 44.047778, 4.486607)

    def test_center(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.center() == (44.0403715, 4.465370500000001)

    def test_distance(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.distance() == 10922.788757238777

    def test_ascent(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.ascent() == 225.29999999999995

    def test_descent(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.descent() == 224.79999999999987

    @pytest.mark.skip(reason="nothing to test")
    def test_compute_points_ascent_rate(self):
        pass

    def test_min_ascent_rate(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.min_ascent_rate() == -38.54138626353898

    def test_max_ascent_rate(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.max_ascent_rate() == 51.2919872933083

    def test_min_elevation(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.min_elevation() == 98.5

    def test_max_elevation(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.max_elevation() == 235.6

    @pytest.mark.skip(reason="time related test")
    def test_start_time(self):
        pass

    @pytest.mark.skip(reason="time related test")
    def test_stop_time(self):
        pass

    @pytest.mark.skip(reason="time related test")
    def test_total_elapsed_time(self):
        pass

    @pytest.mark.skip(reason="time related test")
    def test_stopped_time(self):
        pass

    @pytest.mark.skip(reason="time related test")
    def test_moving_time(self):
        pass

    def test_avg_speed(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.avg_speed() == 10.66505004775145

    def test_avg_moving_speed(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.avg_moving_speed() == 10.974613320139435

    @pytest.mark.skip(reason="nothing to test")
    def test_compute_points_speed(self):
        pass

    def test_min_speed(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.min_speed() == 0.0

    def test_max_speed(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.max_speed() == 19.69510525631602

    def test_avg_pace(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.avg_pace() == 5.625852643105975

    def test_avg_moving_pace(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.avg_moving_pace() == 5.467163010645161

    @pytest.mark.skip(reason="nothing to test")
    def test_compute_points_pace(self):
        pass

    def test_min_pace(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.min_pace() == 3.046442210851278

    def test_max_pace(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.max_pace() == 1041.2956304834424

    @pytest.mark.skip(reason="nothing to test")
    def test_compute_points_ascent_speed(self):
        pass

    def test_min_ascent_speed(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.min_ascent_speed() == -3.3599999999999794

    def test_max_ascent_speed(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert gpx.max_ascent_speed() == 2.1599999999999797

    # ==== Modifications ======================================================#

    # ==== Conversion and Saving ==============================================#

    def test_to_pandas(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        df = gpx.to_pandas(values=["lat", "lon", "ele", "time"])
        reference_df = pd.read_csv(
            os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1.csv")
        )
        # Test
        assert reference_df.equals(df)

    def test_to_gpx(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        gpx.to_gpx("tmp/strava_run_1_test.gpx", xml_schema=False)
        # Test
        assert filecmp.cmp(
            "tmp/strava_run_1_test.gpx",
            os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1.gpx"),
            False,
        )

    def test_to_kml(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        gpx.to_kml("tmp/strava_run_1_test.kml", styles=None, xml_schema=False)
        # Test
        assert filecmp.cmp(
            "tmp/strava_run_1_test.kml",
            os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1.kml"),
            False,
        )

    def test_to_csv(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        gpx.to_csv("tmp/strava_run_1_test.csv", values=["lat", "lon", "ele", "time"])
        # Test
        assert filecmp.cmp(
            "tmp/strava_run_1_test.csv",
            os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1.csv"),
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
    #         os.path.join(REFERENCE_FILES_DIRECTORY,
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
    #         os.path.join(REFERENCE_FILES_DIRECTORY,
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
    #         os.path.join(REFERENCE_FILES_DIRECTORY,
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
    #         os.path.join(REFERENCE_FILES_DIRECTORY,
    #                      "matplotlib_strava_run_1_start_stop_elevation.png"))
    #     # Compare images
    #     return np.array_equal(test_img, ref_img)

    # @pytest.mark.skip(reason="not ready")
    # def test_matplotlib_plot(self):
    #     # Parse GPX file
    #     self.gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
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
    #                          way_points_color=None,
    #                          minimap=False,
    #                          coord_popup=False,
    #                          title=None,
    #                          zoom=12,
    #                          file_path="tmp/folium_strava_run_1.html",
    #                          open=False)
    #     # Compare files
    #     return filecmp.cmp("tmp/folium_strava_run_1.html",
    #                        os.path.join(REFERENCE_FILES_DIRECTORY,
    #                                     "folium_strava_run_1.html"), False)

    # @pytest.mark.skip(reason="not ready")
    # def test_folium_plot(self):
    #     self.test_init() # For developping purpose only (using: pytest test_GPX.py::TestGPX::test_folium_plot)
    #     # Parse GPX file
    #     self.gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
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
            rmtree("tmp", True)

    # ==== Test ===============================================================#

    @pytest.mark.skip(
        reason="test"
    )  # https://docs.pytest.org/en/7.3.x/how-to/skipping.html
    def test_test(self, remove_tmp: bool = True):
        # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")
        # Parse GPX file
        self.gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Remove temporary folder
        if remove_tmp:
            rmtree("tmp")
