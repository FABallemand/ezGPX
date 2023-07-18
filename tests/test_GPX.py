import sys
import os
import pytest
from shutil import rmtree

import numpy as np
import matplotlib.pyplot as plt

file_folder = os.path.dirname(__file__)
parent_folder = os.path.realpath(os.path.dirname(file_folder)) # ie: ezGPX

os.chdir(file_folder)
sys.path.append(parent_folder + "/ezgpx")

from ezgpx import GPX

class TestGPX():

    def _test_matplotlib_plot_1(self):
        # Plot
        self.test_gpx.matplotlib_plot(start_stop_colors=None, elevation_color=False, title="Track", file_path="tmp/matplotlib_strava_run_1.png")

        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1.png")
        ref_img = plt.imread("../tests/test_files/reference_files/matplotlib_strava_run_1.png")

        # Compare images
        return np.array_equal(test_img, ref_img)
    
    def _test_matplotlib_plot_2(self):
        # Plot
        self.test_gpx.matplotlib_plot(start_stop_colors=("#00FF00", "#FF0000"), elevation_color=False, title="Track", file_path="tmp/matplotlib_strava_run_1_start_stop.png")

        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1_start_stop.png")
        ref_img = plt.imread("../tests/test_files/reference_files/matplotlib_strava_run_1_start_stop.png")

        # Compare images
        return np.array_equal(test_img, ref_img)
    
    def _test_matplotlib_plot_3(self):
        # Plot
        self.test_gpx.matplotlib_plot(start_stop_colors=None, elevation_color=True, title="Track", file_path="tmp/matplotlib_strava_run_1_elevation.png")

        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1_elevation.png")
        ref_img = plt.imread("../tests/test_files/reference_files/matplotlib_strava_run_1_elevation.png")

        # Compare images
        return np.array_equal(test_img, ref_img)
    
    def _test_matplotlib_plot_4(self):
        # Plot
        self.test_gpx.matplotlib_plot(start_stop_colors=("#00FF00", "#FF0000"), elevation_color=True, title="Track", file_path="tmp/matplotlib_strava_run_1_start_stop_elevation.png")

        # Load images
        test_img = plt.imread("tmp/matplotlib_strava_run_1_start_stop_elevation.png")
        ref_img = plt.imread("../tests/test_files/reference_files/matplotlib_strava_run_1_start_stop_elevation.png")

        # Compare images
        return np.array_equal(test_img, ref_img)

    def test_matplotlib_plot(self, remove_tmp: bool = True):
        """
        Test matplotlib_plot method.

        Args:
            remove_tmp (bool, optional): Remove temporary folder. Defaults to True.
        """
        self.test_gpx = GPX("../tests/test_files/files/strava_run_1.gpx")

        # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")

        # Tests
        assert(self._test_matplotlib_plot_1())
        assert(self._test_matplotlib_plot_2())
        assert(self._test_matplotlib_plot_3())
        assert(self._test_matplotlib_plot_4())

        # Remove temporary folder
        if remove_tmp:
            rmtree("tmp")

    @pytest.mark.skip(reason="test") # https://docs.pytest.org/en/7.3.x/how-to/skipping.html
    def test_test(self):
        print("Testing...")