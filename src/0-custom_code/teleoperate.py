from lerobot.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so101_follower import SO101FollowerConfig, SO101Follower



# Plug in Leader first, Follower second.
teleop_config = SO101LeaderConfig(
    id="leader",
    port="/dev/ttyACM0",
)

robot_config = SO101FollowerConfig(
    id="follower",
    port="/dev/ttyACM1",
)



robot = SO101Follower(robot_config)
teleop_device = SO101Leader(teleop_config)
robot.connect()
teleop_device.connect()

while True:
    action = teleop_device.get_action()
    robot.send_action(action)