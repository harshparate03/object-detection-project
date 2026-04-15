import cv2
import tkinter as tk

def get_screen_size():
    root = tk.Tk()
    root.withdraw()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.destroy()
    return w, h

def run_centered_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        return

    win_name = "Webcam - Press Q to quit"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    screen_w, screen_h = get_screen_size()
    win_w, win_h = 640, 480

    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    cv2.moveWindow(win_name, x, y)
    cv2.resizeWindow(win_name, win_w, win_h)

    print(f"Screen: {screen_w}x{screen_h} | Window at ({x}, {y})")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break

        cv2.imshow(win_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_centered_webcam()
