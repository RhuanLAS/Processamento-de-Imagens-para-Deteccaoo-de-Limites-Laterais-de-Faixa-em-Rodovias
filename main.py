import os
import cv2 as cv
import matplotlib.pylab as plt
import numpy as np
from filename_script import change_filename

def process_frame(image):
    height = image.shape[0]
    width = image.shape[1]

    region_of_interest_vertices = [
        (200, height),
        (width/2, height/1.9),
        (width/1.5, height)
    ]
    
    canny_image = cv.Canny(image, 170, 200)
    
    cropped_image = region_of_interest(canny_image, np.array([region_of_interest_vertices], np.int32))
    
    lines = cv.HoughLinesP(
        cropped_image,
        rho = 4,
        theta = np.pi/180,
        threshold = 200,
        lines = np.array([]),
        minLineLength = 40,
        maxLineGap = 25
    )

    return draw_the_lines(image, lines)
    
def main():
    path = f'{os.getcwd()}/data/'
    entries = change_filename(path)
    
    array_image = []
    
    for image in entries:
        array_image.append(process_frame(cv.imread(f'{path}{image}')))
    

    for img in array_image:
        plt.clf()
        plt.imshow(img)
        plt.pause(0.05)
        # plt.draw()

def draw_the_lines(img, lines):
    img = np.copy(img)
    blank = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv.line(blank, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)
    img = cv.addWeighted(img, 0.6, blank, 1, 0.0)
    return img

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    #channel_count = img.shape[2]
    match_mask_color = (255, ) #* channel_count
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv.bitwise_and(img, mask)
    return masked_image

    # img = cv.imread(f'{way}{entries[1]}')
    # edges = cv.Canny(img, 75, 100)

    # lines = cv.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # cv.imshow('edges', edges)
    # cv.imshow('image', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

if __name__ == '__main__':
    main()