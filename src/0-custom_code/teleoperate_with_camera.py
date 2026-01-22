from lerobot.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so101_follower import SO101FollowerConfig, SO101Follower
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig



teleop_config = SO101LeaderConfig(
    id="leader",
    port="/dev/ttyACM0"
)

robot_config = SO101FollowerConfig(
    id="follower",
    port="/dev/ttyACM1",
    cameras={
        "0": OpenCVCameraConfig(index_or_path=0, width=1280, height=720, fps=30, fourcc='MJPG'),
        "2": OpenCVCameraConfig(index_or_path=2, width=1280, height=720, fps=30, fourcc='MJPG')
    }
)



robot = SO101Follower(robot_config)
teleop_device = SO101Leader(teleop_config)
robot.connect()
teleop_device.connect()

while True:
    observation = robot.get_observation()
    action = teleop_device.get_action()
    robot.send_action(action)