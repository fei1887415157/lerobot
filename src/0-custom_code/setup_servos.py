x = input("Set up leader (L) or follower (F) ?")



if x == "L":
    from lerobot.teleoperators.so101_leader import SO101Leader, SO101LeaderConfig
    config = SO101LeaderConfig(
        port="/dev/ttyACM0",
        id="leader",
    )
    leader = SO101Leader(config)
    leader.setup_motors()



elif x == "F":
    from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
    config = SO101FollowerConfig(
        port="/dev/ttyACM0",
        id="follower",
    )
    follower = SO101Follower(config)
    follower.setup_motors()



else:
    print("Error. Enter L or F")
    exit(1)