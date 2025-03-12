import cv2

def image_processing():
    img = cv2.imread('images/variant-3.jpeg')

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  
    cv2.imshow('Original (BGR)', img)
    cv2.imshow('HSV Image', hsv_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image_processing()