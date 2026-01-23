import cv2
import time

# The Other Camera
# camera_index = 0
# width = 1280
# height = 720
# fps_target = 30
# fourcc_code = 'MJPG'

# Logi C270
camera_index = 2
width = 853
height = 480
fps_target = 30
fourcc_code = 'MJPG'

cap = cv2.VideoCapture(camera_index)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, fps_target)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc_code))

actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
window_title = f"Camera {camera_index} - {actual_w}x{actual_h}"

# Variables for smoothed FPS
prev_time = time.time()
display_fps = 0
frame_count = 0
update_interval = 0.5  # Seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate time elapsed
    current_time = time.time()
    elapsed = current_time - prev_time
    frame_count += 1

    # Update the display value only every 0.5s
    if elapsed >= update_interval:
        display_fps = frame_count / elapsed
        frame_count = 0
        prev_time = current_time

    # Display FPS in green
    cv2.putText(frame, f"FPS: {display_fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(window_title, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()