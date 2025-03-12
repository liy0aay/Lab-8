import cv2
import numpy as np

def circle_detector():
    cap = cv2.VideoCapture(0) # захват видео с камеры, 0 - первая доступная камера
    
    fly = cv2.imread("images/fly64.png", cv2.IMREAD_UNCHANGED)  # загрузка с альфа-каналом
    fly_h, fly_w = fly.shape[:2]  # размеры мухи

    while True:
        ret, frame = cap.read() # захват одного кадра, ret-булево, frame-сам кадр
        if not ret:
            break

        height, width = frame.shape[:2] # размеры кадра
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        gray = cv2.GaussianBlur(gray, (9, 9), 0)

        # используем метод для поиска круга
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, 
                                   minDist=100, param1=80, param2=40,
                                   minRadius=30, maxRadius=250)

        if circles is not None:
            circles = np.uint16(np.around(circles)) # округляем до целых 
            x, y, r = circles[0, 0] # центр круга  и радиус


            print(f"Координаты центра: ({x}, {y})")

            # располагаем муху точно по центру метки
            fly_x1 = x - fly_w // 2
            fly_y1 = y - fly_h // 2
            fly_x2 = fly_x1 + fly_w
            fly_y2 = fly_y1 + fly_h

            # проверяем границы, чтобы не выйти за край кадра
            if 0 <= fly_x1 < width and 0 <= fly_y1 < height and fly_x2 < width and fly_y2 < height:
                fly_region = frame[fly_y1:fly_y2, fly_x1:fly_x2]

                # работа с прозрачностью
                if fly.shape[2] == 4: # это размерность альфа-канала (у RGB их 3)
                    alpha = fly[:, :, 3] / 255.0
                    for c in range(3):
                        fly_region[:, :, c] = (1 - alpha) * fly_region[:, :, c] + alpha * fly[:, :, c]
                else:
                    frame[fly_y1:fly_y2, fly_x1:fly_x2] = fly
    
        cv2.imshow('Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    circle_detector()