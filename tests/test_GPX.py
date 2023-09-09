import sys
import os
import pytest
import filecmp
from shutil import rmtree

import numpy as np
import matplotlib.pyplot as plt

file_folder = os.path.dirname(__file__)
parent_folder = os.path.realpath(os.path.dirname(file_folder)) # ie: ezGPX

os.chdir(file_folder)
sys.path.append(parent_folder + "/ezgpx")

from ezgpx import GPX

FILES_DIRECTORY = "test_files/files/"
REFERENCE_FILES_DIRECTORY = "test_files/reference_files/"

class TestGPX():

    #==== Init ===============================================================#

    def test_init(self):
        # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")

    #==== Parsing/Writing ====================================================#

    def test_parse(self):
        # Parse GPX files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"), check_schemas=True, extensions_schemas=False)
        invalid_gpx = GPX(os.path.join(FILES_DIRECTORY, "invalid_schema.gpx"), check_schemas=False, extensions_schemas=False)

    #==== Check Schemas ======================================================#

    def test_check_schemas(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"), check_schemas=True, extensions_schemas=False)
        invalid_gpx = GPX(os.path.join(FILES_DIRECTORY, "invalid_schema.gpx"), check_schemas=False, extensions_schemas=False)
        # Tests
        assert(gpx.check_schemas(extensions_schemas=False) == True)
        assert(invalid_gpx.check_schemas(extensions_schemas=False) == False)

    #==== Properties =========================================================#

    def test_file_name(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.file_name() == "strava_run_1.gpx")

    def test_name(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.name() == "Dérouillage habituel 💥")

    def test_set_name(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        new_name = "test"
        gpx.set_name(new_name)
        assert(gpx.name() == new_name)

    def test_nb_points(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.nb_points() == 939)

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
        assert(gpx.bounds() == (44.032965, 4.444134, 44.047778, 4.486607))

    def test_center(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.center() == (44.0403715, 4.465370500000001))

    def test_distance(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.distance() == 10922.788757238777)

    def test_ascent(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.ascent() == 225.29999999999995)

    def test_descent(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Test
        assert(gpx.descent() == 224.79999999999987)

    #==== Conversion and Saving ==============================================#

    def test_to_gpx(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        gpx.to_gpx("tmp/strava_run_1.gpx", check_schemas=False)
        # Test
        assert(filecmp.cmp("tmp/strava_run_1.gpx", os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1_test.gpx"), False))
        
    def test_to_kml(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        gpx.to_kml("tmp/strava_run_1_test.kml", styles=None, check_schemas=False)
        # Test
        assert(filecmp.cmp("tmp/strava_run_1_test.kml", os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1_test.kml"), False))

    def test_to_csv(self):
        # Parse GPX Files
        gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        gpx.to_csv("tmp/strava_run_1.csv", columns=["lat", "lon", "ele"])
        # Test
        assert(filecmp.cmp("tmp/strava_run_1.csv", os.path.join(REFERENCE_FILES_DIRECTORY, "strava_run_1_test.csv"), False))

    #==== Plots ==============================================================#

    def _test_matplotlib_plot_1(self):
        # Plot
        self.gpx.matplotlib_plot(start_stop_colors=None, color="#ffffff", title="Track", file_path="tmp/matplotlib_strava_run_1.png")
        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1.png")
        ref_img = plt.imread(os.path.join(REFERENCE_FILES_DIRECTORY, "matplotlib_strava_run_1.png"))
        # Compare images
        return np.array_equal(test_img, ref_img)
    
    def _test_matplotlib_plot_2(self):
        # Plot
        self.gpx.matplotlib_plot(start_stop_colors=("#00FF00", "#FF0000"), color="#ffffff", title="Track", file_path="tmp/matplotlib_strava_run_1_start_stop.png")
        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1_start_stop.png")
        ref_img = plt.imread(os.path.join(REFERENCE_FILES_DIRECTORY, "matplotlib_strava_run_1_start_stop.png"))

        # Compare images
        return np.array_equal(test_img, ref_img)
    
    def _test_matplotlib_plot_3(self):
        # Plot
        self.gpx.matplotlib_plot(start_stop_colors=None, color=True, title="Track", file_path="tmp/matplotlib_strava_run_1_elevation.png")
        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1_elevation.png")
        ref_img = plt.imread(os.path.join(REFERENCE_FILES_DIRECTORY, "matplotlib_strava_run_1_elevation.png"))
        # Compare images
        return np.array_equal(test_img, ref_img)
    
    def _test_matplotlib_plot_4(self):
        # Plot
        self.gpx.matplotlib_plot(start_stop_colors=("#00FF00", "#FF0000"), color=True, title="Track", file_path="tmp/matplotlib_strava_run_1_start_stop_elevation.png")
        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1_start_stop_elevation.png")
        ref_img = plt.imread(os.path.join(REFERENCE_FILES_DIRECTORY, "matplotlib_strava_run_1_start_stop_elevation.png"))
        # Compare images
        return np.array_equal(test_img, ref_img)

    @pytest.mark.skip(reason="not ready")
    def test_matplotlib_plot(self, remove_tmp: bool = True):
        """
        Test matplotlib_plot method.

        Args:
            remove_tmp (bool, optional): Remove temporary folder. Defaults to True.
        """
        # Parse GPX file
        self.gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Tests
        assert(self._test_matplotlib_plot_1())
        assert(self._test_matplotlib_plot_2())
        assert(self._test_matplotlib_plot_3())
        assert(self._test_matplotlib_plot_4())
        # self._test_matplotlib_plot_1()
        # self._test_matplotlib_plot_2()
        # self._test_matplotlib_plot_3()
        # self._test_matplotlib_plot_4()

    #==== Destroy ============================================================#

    def test_destroy(self, remove_tmp: bool = True):
        # Remove temporary folder
        if remove_tmp:
            rmtree("tmp", True)

    #==== Test ===============================================================#

    @pytest.mark.skip(reason="test") # https://docs.pytest.org/en/7.3.x/how-to/skipping.html
    def test_test(self, remove_tmp: bool = True):
         # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")
        # Parse GPX file
        self.gpx = GPX(os.path.join(FILES_DIRECTORY, "strava_run_1.gpx"))
        # Remove temporary folder
        if remove_tmp:
            rmtree("tmp")