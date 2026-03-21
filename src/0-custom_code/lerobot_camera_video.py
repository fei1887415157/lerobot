import cv2
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.cameras.opencv.camera_opencv import OpenCVCamera
from lerobot.cameras.configs import ColorMode, Cv2Rotation

# Construct an `OpenCVCameraConfig` with your desired FPS, resolution, color mode, and rotation.
config = OpenCVCameraConfig(
    index_or_path=2,
    fps=30,
    width=1280,
    height=720,
    color_mode=ColorMode.BGR, # Using BGR for cv2.imshow compatibility
    rotation=Cv2Rotation.NO_ROTATION,
    fourcc='MJPG'
)

# Instantiate and connect an `OpenCVCamera`, performing a warm-up read (default).
camera = OpenCVCamera(config)
camera.connect()

print("Starting live video view. Press 'q' to exit.")

# Read frames asynchronously in a loop via `async_read(timeout_ms)`
try:
    while True:
        frame = camera.async_read(timeout_ms=200)
        
        if frame is not None:
            # Display the frame using OpenCV
            cv2.imshow("Lerobot Camera Live View", frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Timeout reading frame...")
finally:
    camera.disconnect()
    cv2.destroyAllWindows()