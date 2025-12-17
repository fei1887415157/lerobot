x = input("Calibrate leader (L) or follower (F) ?")



if x == "L":
    from lerobot.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader
    config = SO101LeaderConfig(
        port="/dev/ttyACM0",
        id="leader",
    )
    leader = SO101Leader(config)
    leader.connect(calibrate=False)
    leader.calibrate()
    leader.disconnect()



elif x == "F":
    from lerobot.robots.so101_follower import SO101FollowerConfig, SO101Follower
    config = SO101FollowerConfig(
        port="/dev/tty",
        id="follower",
    )
    follower = SO101Follower(config)
    follower.connect(calibrate=False)
    follower.calibrate()
    follower.disconnect()



else:
    print("Error. Enter L or F")
    exit(1)