import cv2
import time

cam1_id, w1, h1 = 0, 640, 360

def setup_camera(idx, w, h):
    cap = cv2.VideoCapture(idx)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    return cap

cap1 = setup_camera(cam1_id, w1, h1)

prev_time = time.time()
frame_count = 0
display_fps = 0

while True:
    ret1, frame1 = cap1.read()

    if not ret1:
        break

    # Performance Tracking
    frame_count += 1
    elapsed = time.time() - prev_time
    if elapsed >= 0.5:
        display_fps = frame_count / elapsed
        frame_count, prev_time = 0, time.time()

    # Overlay FPS on frame
    cv2.putText(frame1, f"FPS: {display_fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Camera 1", frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cv2.destroyAllWindows()