from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.franka.tasks import FollowTarget
from omni.isaac.motion_generation.lula import RmpFlow
from omni.isaac.motion_generation import ArticulationMotionPolicy
from omni.isaac.core import World

from omni.isaac.core.utils.extensions import get_extension_path_from_name
import os

my_world = World(stage_units_in_meters=1.0)

# 添加一个FollowTarget的任务，这个任务继承自omni.isaac.core.tasks.FollowTarget，重写了set_robot函数，返回一个Franka类
my_task = FollowTarget(name="follow_target_task")
my_world.add_task(my_task)

my_world.reset()
task_params = my_world.get_task("follow_target_task").get_params()
franka_name = task_params["robot_name"]["value"]
target_name = task_params["target_name"]["value"]
my_franka = my_world.scene.get_object(franka_name)

# RMPflow config files for supported robots are stored in the motion_generation extension under "/motion_policy_configs"
mg_extension_path = get_extension_path_from_name("omni.isaac.motion_generation")
rmp_config_dir = os.path.join(mg_extension_path, "motion_policy_configs")

#Initialize an RmpFlow object
rmpflow = RmpFlow(
    robot_description_path = rmp_config_dir + "/franka/rmpflow/robot_descriptor.yaml",
    urdf_path = rmp_config_dir + "/franka/lula_franka_gen.urdf",
    rmpflow_config_path = rmp_config_dir + "/franka/rmpflow/franka_rmpflow_common.yaml",
    end_effector_frame_name = "right_gripper",
    evaluations_per_frame = 5
)
#Use the ArticulationMotionPolicy wrapper object to connect rmpflow to the Franka robot articulation.
physics_dt = 1/60.
articulation_rmpflow = ArticulationMotionPolicy(my_franka,rmpflow,physics_dt)

articulation_controller = my_franka.get_articulation_controller()
while simulation_app.is_running():
    my_world.step(render=True)
    if my_world.is_playing():
        if my_world.current_time_step_index == 0:
            my_world.reset()
        observations = my_world.get_observations()

        #Set rmpflow target to be the current position of the target cube.
        rmpflow.set_end_effector_target(
            target_position=observations[target_name]["position"],
            target_orientation=observations[target_name]["orientation"],
        )

        actions = articulation_rmpflow.get_next_articulation_action()
        articulation_controller.apply_action(actions)

simulation_app.close()