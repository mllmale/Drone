import numpy as np
import cv2
from matplotlib import pyplot as plt


def show_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


def get_color(obj_img, x, y):
    return obj_img.item(y, x, 2), obj_img.item(y, x, 1), obj_img.item(y, x, 0)


def set_color(obj_img, x, y, b, g, r):
    obj_img.itemset((y, x, 1), b)
    obj_img.itemset((y, x, 1), g)
    obj_img.itemset((y, x, 1), r)

    return obj_img


def main():
    obj_img = cv2.imread("img/20190129_111113.jpg")
    altura, largura, canal = obj_img.shape
    print(f'Dimensões da Imagem\natlura: {altura}\nLargura: {largura}\nCanal de cor: {canal}')

    for y in range(0, altura):
        for x in range(0, largura):
            azul, verde, vermelho = get_color(obj_img, x, y)
            obj_img = set_color(obj_img, x, y, verde, azul, vermelho)

    show_image(obj_img)


main()
