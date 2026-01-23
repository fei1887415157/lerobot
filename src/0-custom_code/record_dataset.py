from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.datasets.utils import hw_to_dataset_features
from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig
from lerobot.teleoperators.so101_leader.so101_leader import SO101Leader
from lerobot.utils.control_utils import init_keyboard_listener
from lerobot.utils.utils import log_say
from lerobot.utils.visualization_utils import init_rerun
from lerobot.scripts.lerobot_record import record_loop
from lerobot.processor import make_default_processors
import os



TASK_DESCRIPTION = "test task"
NUM_EPISODES = 3
EPISODE_TIME_SEC = 5
RESET_TIME_SEC = 5
FPS = 30

teleop_config = SO101LeaderConfig(
    id="leader",
    port="/dev/ttyACM0",
)

robot_config = SO101FollowerConfig(
    id="follower",
    port="/dev/ttyACM1",
    cameras={
        "0": OpenCVCameraConfig(index_or_path=0, width=640, height=360, fps=FPS, fourcc='MJPG'),
        "2": OpenCVCameraConfig(index_or_path=2, width=640, height=360, fps=FPS, fourcc='MJPG')
    }
)



# Initialize the robot and teleoperator
robot = SO101Follower(robot_config)
teleop = SO101Leader(teleop_config)

# Configure the dataset features
action_features = hw_to_dataset_features(robot.action_features, "action")
obs_features = hw_to_dataset_features(robot.observation_features, "observation")
dataset_features = {**action_features, **obs_features}

repo_id = "fei1887415157/test_dataset"
local_dir = "/home/robobond/.cache/huggingface/lerobot/fei1887415157/test_dataset"

if os.path.exists(local_dir):
    # LOAD: This keeps existing episodes and appends new ones
    dataset = LeRobotDataset(repo_id)
    print("Existing dataset found. Appending new episodes.")
else:
    # CREATE: Only runs the very first time
    dataset = LeRobotDataset.create(
        repo_id=repo_id,
        fps=FPS,
        features=dataset_features,
        robot_type=robot.name,
        use_videos=True
    )
    print("Created a brand new dataset.")

# Initialize the keyboard listener and rerun visualization
_, events = init_keyboard_listener()
init_rerun(session_name="recording")

# Connect the robot and teleoperator
robot.connect()
teleop.connect()

# Create the required processors
teleop_action_processor, robot_action_processor, robot_observation_processor = make_default_processors()

episode_idx = 0
while episode_idx < NUM_EPISODES and not events["stop_recording"]:
    log_say(f"Recording episode {episode_idx + 1} of {NUM_EPISODES}")

    record_loop(
        robot=robot,
        events=events,
        fps=FPS,
        teleop_action_processor=teleop_action_processor,
        robot_action_processor=robot_action_processor,
        robot_observation_processor=robot_observation_processor,
        teleop=teleop,
        dataset=dataset,
        control_time_s=EPISODE_TIME_SEC,
        single_task=TASK_DESCRIPTION,
        display_data=True,
    )

    # Reset the environment if not stopping or re-recording
    if not events["stop_recording"] and (episode_idx < NUM_EPISODES - 1 or events["rerecord_episode"]):
        log_say("Reset the environment")
        record_loop(
            robot=robot,
            events=events,
            fps=FPS,
            teleop_action_processor=teleop_action_processor,
            robot_action_processor=robot_action_processor,
            robot_observation_processor=robot_observation_processor,
            teleop=teleop,
            control_time_s=RESET_TIME_SEC,
            single_task=TASK_DESCRIPTION,
            display_data=True,
        )

    if events["rerecord_episode"]:
        log_say("Re-recording episode")
        events["rerecord_episode"] = False
        events["exit_early"] = False
        dataset.clear_episode_buffer()
        continue

    dataset.save_episode()
    episode_idx += 1



# Clean up
log_say("Stop recording")
robot.disconnect()
teleop.disconnect()
dataset.push_to_hub()