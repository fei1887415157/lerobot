import time
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

last_print_time = time.time()

while True:
    action = teleop_device.get_action()
    robot.send_action(action)

    if time.time() - last_print_time > 1.0:
        last_print_time = time.time()
        
        # Read raw values
        currents = robot.bus.sync_read('Present_Current')
        voltages = robot.bus.sync_read('Present_Voltage')
        temps = robot.bus.sync_read('Present_Temperature')

        # Convert to standard units for display (taking the first motor as an example or iterating)
        # Example for printing all motors:
        print(f"Current (A):  {[round(c * 0.0065, 2) for c in currents.values()]}")
        print(f"Voltage (V):  {[v * 0.1 for v in voltages.values()]}")
        print(f"Temp (°C):    {list(temps.values())}")
        print("-" * 20)