import os
import cv2 as cv
import numpy as np
import matplotlib.pylab as plt


def region_of_interest(img, v):
    mask = np.zeros_like(img)
    mask = cv.fillPoly(mask, v, (255, ))
    masked_img = cv.bitwise_and(img, mask)
    return masked_img


def main():
    path = f'{os.getcwd()}/data'
    old_angles = []

    for i in range(len(os.listdir(path))):
        
        # Lendo a imagem
        img = cv.imread(f'{path}/{i}.png')

        # Obtendo height e width da imagem
        height, width = img.shape[:2]

        # Definindo ROI
        region_of_interest_vertices = [
            (200, height),
            (width/2, height/1.9),
            (width/1.5, height)
        ]

        # Aplicando Gaussian Blur (Para tirar ruídos indesejados e garantir que o algoritmo Canny não detecte nada além de bordas)
        blur_img = cv.GaussianBlur(
            src = img,
            ksize = (5, 5),
            sigmaX = 0
        )

        # Algoritmo para detecção de bordas
        edges_img = cv.Canny(
            image = blur_img,
            threshold1 = 50,
            threshold2 = 200
        )

        # Gera uma imagem apenas com os valores na ROI
        cropped_img = region_of_interest(
            edges_img, 
            np.array([region_of_interest_vertices], np.int32)
        )

        # Obtendo as linhas usando Algoritmo de Hough
        lines = cv.HoughLinesP(
            image = cropped_img,
            rho = 4,
            theta = np.pi/180,
            threshold = 100,
            minLineLength = 50,
            maxLineGap = 10
        )
    
        # Criando uma matriz de Zeros com o mesmo tamanho da imagem original
        line_image = np.zeros_like(img)

        if lines is not None:
            
            line_groups = {}

            for line in lines:
                for x1,y1,x2,y2 in line:
                    line_angle = (y2 - y1)/(x2 - x1)
                    
                    if len(old_angles) <= 1:
                        if -0.4 <= line_angle <= 0.4:
                            continue
                    else:
                        good_angle = False
                        for oa in old_angles:
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

            old_angles.clear()
            for _, line_groups_val in line_groups.items():
                sum = [0 for _ in range(4)]
                for l in line_groups_val:
                    for index_l in range(len(l)):
                        sum[index_l] += l[index_l]

                for index_sum in range(len(sum)):
                    sum[index_sum] = int(sum[index_sum] / len(line_groups_val))

                old_angles.append((sum[3] - sum[1]) / (sum[2] - sum[0]))

                line_image = cv.line(line_image, (sum[0], sum[1]), (sum[2], sum[3]), (0,255,0, 1), 5)

            # Colocando as linhas na imagem original
            lines_edges = cv.addWeighted(img, 0.5, line_image, 4, 4)

            plt.clf()
            plt.imshow(lines_edges)
            plt.pause(0.05)


if __name__ == '__main__':
    main()