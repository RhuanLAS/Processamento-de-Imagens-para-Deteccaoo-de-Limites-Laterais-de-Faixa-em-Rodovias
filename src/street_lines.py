import cv2 as cv
import numpy as np


class StreetLines:
    """
    StreetLines agroup steps to look for street lines in an image
    """
    
    def __init__(self, data_path: str) -> None:
        self._old_angles = []
        self._data_path = data_path
    
    def process_new_img(self, img):
        """
        All process to get an image with street lines filled.
        """
        
        h, w = img.shape[:2]

        blur_img = self._blurring_img(img)
        edges_img = self._look_for_edges(blur_img)
        cropped_img = self._crop_img(edges_img, h, w)
        self._lines = self._look_for_lines(cropped_img)
        lines_edges = self._filtering_lines(img)
        return lines_edges

    def _blurring_img(self, img):
        """
        Since edge detection is susceptible to noise in the image
        first step is to remove the noise in the image with a 5x5 
        Gaussian filter
        """

        return cv.GaussianBlur(
            src = img,
            ksize = (5, 5),
            sigmaX = 0
        )

    def _look_for_edges(self, blur_img):
        """
        Looks for edges using Canny Algorithm in the blur_img.
        Canny Edge Detection is a popular edge detection algorithm.
        """

        return cv.Canny(
            image = blur_img,
            threshold1 = 50,
            threshold2 = 200
        )

    def _crop_img(self, edges_img, h, w):
        """
        Defines an image with only edges inside ROI.
        """

        region_of_interest_vertices = [(200, h), (w/2, h/1.9), (w/1.5, h)]

        mask = np.zeros_like(edges_img)
        mask = cv.fillPoly(mask, np.array([region_of_interest_vertices], np.int32), (255, ))
        masked_img = cv.bitwise_and(edges_img, mask)
        return masked_img

    def _look_for_lines(self, cropped_img):
        """
        Looks for lines using Hough Lines Algorithm.
        The Hough Line Transform is a transform used to detect straight lines.
        """
        return cv.HoughLinesP(
            image = cropped_img,
            rho = 4,
            theta = np.pi/180,
            threshold = 100,
            minLineLength = 50,
            maxLineGap = 10
        )

    def _filtering_lines(self, img):
        """
        Gets previous angles and interpolate lines that satisfies those angles.
        """
        
        line_image = np.zeros_like(img)

        if self._lines is not None:
            
            line_groups = {}

            for line in self._lines:
                for x1,y1,x2,y2 in line:
                    line_angle = (y2 - y1)/(x2 - x1)
                    
                    if len(self._old_angles) <= 1:
                        if -0.4 <= line_angle <= 0.4:
                            continue
                    else:
                        good_angle = False
                        for oa in self._old_angles:
                            if oa - 0.2 <= line_angle <= oa + 0.2:
                                good_angle = True
                                break
                        if not good_angle:
                            continue

                    not_group_yet = True
                    for angle in line_groups.keys():
                        if angle - 0.5 <= line_angle <= angle + 0.5:
                            line_groups[angle].append([x1, y1, x2, y2])
                            not_group_yet = False
                            break
                        
                    if len(line_groups) == 0 or not_group_yet:
                        line_groups[line_angle] = [[x1, y1, x2, y2]]

            self._old_angles.clear()
            for _, line_groups_val in line_groups.items():
                sum = [0 for _ in range(4)]
                for l in line_groups_val:
                    for index_l in range(len(l)):
                        sum[index_l] += l[index_l]

                for index_sum in range(len(sum)):
                    sum[index_sum] = int(sum[index_sum] / len(line_groups_val))

                self._old_angles.append((sum[3] - sum[1]) / (sum[2] - sum[0]))

                line_image = cv.line(line_image, (sum[0], sum[1]), (sum[2], sum[3]), (0,255,0, 1), 5)

            lines_edges = cv.addWeighted(img, 0.5, line_image, 4, 4)

            return lines_edges
        else:
            return None