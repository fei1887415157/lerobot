import cv2
import threading
import time


class MultithreadCam:
    # Accept specific parameters during initialization
    def __init__(self, src=-1, width=0, height=0, fps=0):
        self.cap = cv2.VideoCapture(src)

        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        self.ret, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            return self
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True  # Ends thread when main program exits
        self.thread.start()
        return self

    def update(self):
        while self.started:
            ret, frame = self.cap.read()
            with self.read_lock:
                self.ret = ret
                if ret:
                    self.frame = frame
            # Micro-sleep to prevent background threads from spiking CPU overhead
            time.sleep(0.001)

    def read(self):
        with self.read_lock:
            frame_copy = self.frame.copy() if self.ret else None
            return self.ret, frame_copy

    def stop(self):
        self.started = False
        if self.thread.is_alive():
            self.thread.join()
        self.cap.release()


# --- Execution ---
if __name__ == '__main__':
    # Initialize Camera 1: 4K @ 60 FPS (Device Index 0)
    cam1 = MultithreadCam(src=0, width=1280, height=720, fps=15).start()

    # Initialize Camera 2: 4K @ 30 FPS (Device Index 2 - adjust if needed)
    cam2 = MultithreadCam(src=2, width=1280, height=720, fps=15).start()

    # --- WINDOW CONFIGURATIONS ---
    win_cam1 = 'Cam 1: 4K 30FPS'
    win_cam2 = 'Cam 2: 4K 30FPS'

    cv2.namedWindow(win_cam1, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_cam1, 960, 720)  # Scale down display mapping to fit your desktop

    cv2.namedWindow(win_cam2, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_cam2, 960, 720)

    # Individual loop timing tracking variables
    prev_time1 = time.time()
    prev_time2 = time.time()

    print("Streaming dual 4K setups... Press 'q' to quit.")

    while True:
        # 1. Process and Render Camera 1
        ret1, frame1 = cam1.read()
        if ret1:
            curr_time1 = time.time()
            fps1 = 1 / (curr_time1 - prev_time1) if (curr_time1 - prev_time1) > 0 else 0
            prev_time1 = curr_time1

            cv2.putText(frame1, f"Display FPS: {int(fps1)}", (40, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            cv2.imshow(win_cam1, frame1)

        # 2. Process and Render Camera 2
        ret2, frame2 = cam2.read()
        if ret2:
            curr_time2 = time.time()
            fps2 = 1 / (curr_time2 - prev_time2) if (curr_time2 - prev_time2) > 0 else 0
            prev_time2 = curr_time2

            cv2.putText(frame2, f"Display FPS: {int(fps2)}", (40, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4, cv2.LINE_AA)
            cv2.imshow(win_cam2, frame2)

        # Break loop globally
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean shut down of both streams
    cam1.stop()
    cam2.stop()
    cv2.destroyAllWindows()