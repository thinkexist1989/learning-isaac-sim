from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.types import ArticulationAction
from omni.isaac.core import World

import numpy as np
import os
import carb

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
asset_path = os.path.join(os.getcwd(), "siasun_gcr10/siasun_gcr10.usd")
add_reference_to_stage(usd_path=asset_path, prim_path="/World/Siasun_robot")
# articulation_controller =  ArticulationController()
siasun = world.scene.add(Robot(prim_path="/World/Siasun_robot", name="siasun_robot"))


world.reset()

siasun_articulation_controller = siasun.get_articulation_controller()


i = np.array([0, 0, 0, 0, 0, 0]);
while simulation_app.is_running():
    world.step(render=True)
    if world.is_playing():
        if world.current_time_step_index == 0:
            world.reset()
    siasun.apply_action(ArticulationAction(
        joint_positions=0.5 * np.sin(0.01*i), 
        joint_efforts=None, 
        joint_velocities=None))
    i = i + 1
    # siasun_articulation_controller.apply_action(ArticulationAction(joint_positions=1 * np.random.rand(2,), joint_efforts=None, joint_velocities=None))
    
    