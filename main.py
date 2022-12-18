import os
import cv2 as cv
import matplotlib.pylab as plt
import numpy as np

def region_of_interest(img, v):
    mask = np.zeros_like(img)
    mask = cv.fillPoly(mask, v, (255, ))
    masked_img = cv.bitwise_and(img, mask)
    return masked_img


def main():
    path = f'{os.getcwd()}/data'

    for i in range(len(os.listdir(path))):
        
        # Lendo a imagem
        img = cv.imread(f'{path}/{i}.png', cv.IMREAD_GRAYSCALE)

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

        # ! Teste
        # l = np.array([
        #     [417, 373],
        #     [556, 224],
        #     [566, 220],
        #     [433, 373]
        # ], dtype=np.int32)

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
            lines = np.array([]),
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

                    if -0.4 <= line_angle <= 0.4:
                        continue

                    not_group_yet = True
                    for angle in line_groups.keys():
                        if angle - 0.5 <= line_angle <= angle + 0.5:
                            line_groups[angle].append([x1, y1, x2, y2])
                            not_group_yet = False
                            break
                        
                    if len(line_groups) == 0 or not_group_yet:
                        line_groups[line_angle] = [[x1, y1, x2, y2]]

            for k, line_groups_val in line_groups.items():
                first_point = [0, 0]
                second_point = [0, 0]
                for l in line_groups_val:
                    first_point[0] += l[0]
                    first_point[1] += l[1]
                    second_point[0] += l[2]
                    second_point[1] += l[3]
                
                first_point[0] = int(first_point[0] / len(line_groups_val))
                first_point[1] = int(first_point[1] / len(line_groups_val))
                second_point[0] = int(second_point[0] / len(line_groups_val))
                second_point[1] = int(second_point[1] / len(line_groups_val))

                line_image = cv.line(line_image, tuple(first_point), tuple(second_point),(255,0,0),5)

            # Colocando as linhas na imagem original
            lines_edges = cv.addWeighted(img, 0.8, line_image, 1, 1)

            plt.clf()
            plt.imshow(lines_edges)
            plt.pause(0.05)


if __name__ == '__main__':
    main()