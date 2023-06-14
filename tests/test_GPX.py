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

    def test_plot(self, remove_tmp: bool = True):
        # Create temporary folder
        rmtree("tmp", True)
        os.makedirs(os.path.dirname(__file__) + "/tmp")

        # Plot
        test_gpx = GPX("../test_files/files/strava_running_1.gpx")
        test_gpx.plot(start_stop=True, elevation_color=True, file_path="tmp/strava_running_1_start_stop_elevation.png")

        # Load images
        test_img = plt.imread("tmp/strava_running_1_start_stop_elevation.png")
        ref_img = plt.imread("../test_files/reference_files/strava_running_1_start_stop_elevation.png")

        res = np.array_equal(test_img, ref_img)

        # Create temporary folder
        if remove_tmp:
            rmtree("tmp")

        assert(res)

    @pytest.mark.skip(reason="test") # https://docs.pytest.org/en/7.3.x/how-to/skipping.html
    def test_test(self):
        print("Testing...")