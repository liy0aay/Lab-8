import cv2
import numpy as np

def circle_detector():
    cap = cv2.VideoCapture(0) # захват видео с камеры, 0 - первая доступная камера
    
    while True:
        ret, frame = cap.read() # захват одного кадра, ret-булево, frame-сам кадр
        if not ret:
            break

        height, width = frame.shape[:2] # размеры кадра
        xcenter, ycenter = width // 2, height // 2  # центр кадра

        # определяем границы центрального квадрата 200x200 пикселей
        square_size = 200
        half_square = square_size // 2
        square_x1, square_y1 = xcenter - half_square, ycenter - half_square # верхний левый угол
        square_x2, square_y2 = xcenter + half_square, ycenter + half_square # правый нижний угол

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        gray = cv2.GaussianBlur(gray, (9, 9), 0)

        # используем метод для поиска круга
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, 
                                   minDist=100, param1=80, param2=40,
                                   minRadius=30, maxRadius=250)

        if circles is not None:
            circles = np.uint16(np.around(circles)) # округляем до целых 
            x, y, r = circles[0, 0] # центр круга  и радиус

            # рисуем круг и его центр
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

            # проверяем, попал ли центр круга в центральный квадрат
            in_center = (square_x1 <= x <= square_x2) and (square_y1 <= y <= square_y2)

            #рисуем квадрат и статус
            color = (0, 0, 255) if in_center else (255, 0, 0)  # красный, если в центре
            cv2.rectangle(frame, (square_x1, square_y1), (square_x2, square_y2), color, 2)

            if in_center:
                cv2.putText(frame, "CIRCLE DETECTED", (100, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (140, 140, 13), 2)

            print(f"Координаты центра: ({x}, {y})")

        cv2.imshow('Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    circle_detector()