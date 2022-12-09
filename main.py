import os
import cv2 as cv
import matplotlib.pylab as plt
import numpy as np
from filename_script import change_filename

def main():
    way = f'{os.getcwd()}/data/'
    entries = change_filename(way)
    
    image = cv.imread(f'{way}{entries[4]}')
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]

    region_of_interest_vertices = [
        (200, height),
        (width/2, height/1.9),
        (width/1.5, height)
    ]
    
    canny_image = cv.Canny(image, 100, 200)
    
    cropped_image = region_of_interest(canny_image, np.array([region_of_interest_vertices], np.int32))
    
    lines = cv.HoughLinesP(
        cropped_image,
        rho = 6,
        theta = np.pi/60,
        threshold = 160,
        lines = np.array([]),
        minLineLength = 40,
        maxLineGap = 25
    )

    image_with_line = drow_the_lines(image, lines)

    plt.imshow(image_with_line)
    plt.show()

def drow_the_lines(img, lines):
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