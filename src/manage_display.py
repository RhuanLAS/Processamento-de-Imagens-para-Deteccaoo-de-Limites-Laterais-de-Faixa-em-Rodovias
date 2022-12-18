import os
import cv2 as cv
import matplotlib.pylab as plt

from .street_lines import StreetLines


class ManageDisplay:
    """
    ManageDisplay provides a workflow to display an image.
    """

    def __init__(self, data_path: str) -> None:
        """
        Constructor for ManageDisplay class.
        Stores data_path and creates street_lines_obj
        """

        self._data_path = data_path
        self._street_lines_obj = StreetLines(
            data_path = data_path
        )

    def workflow(self) -> None:
        """
        Project workflow
        """

        for i in range(len(os.listdir(self._data_path))):

            # Reading an image
            img = cv.imread(f'{self._data_path}/{i}.png')

            # Filtering the image to display
            self._img_display = self._street_lines_obj.process_new_img(
                img = img
            )

            self._show_img()

    def _show_img(self) -> None:
        """
        Verifies if img_display got some problem (None) otherwise show the image
        """
        
        if self._img_display is not None:
            plt.clf()
            plt.imshow(self._img_display)
            plt.pause(0.05)