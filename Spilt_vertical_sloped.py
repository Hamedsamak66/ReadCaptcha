import cv2
from matplotlib import pyplot as plt

image = cv2.imread('129_2_2.png', 0)
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
counter = 1

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    number = binary_image[y:y+h, x:x+w]
    cv2.imwrite(f'number_{counter}.png', number)
    counter += 1

    # Instead of cv2.imshow, use matplotlib
    plt.imshow(number, cmap='gray')
    plt.title(f'Number {counter}')
    plt.show()
