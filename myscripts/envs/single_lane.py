from flow.envs import Env
from gym.spaces.box import Box
from gym.spaces import Tuple
import numpy as np

ADDITIONAL_ENV_PARAMS = {
    "max_accel" : 1,
    "max_decle" : 1,
}

class SingleLaneEnv(Env):
    def action_space(self):
        num_actions = self.initial_vehicles.num_rl_vehicles
        accel_ub = self.env_params.additional_params["max_accel"]
        accel_lb = - abs(self.env_params.additional_params["max_decel"])

        return Box(low=accel_lb,
                   high=accel_ub,
                   shape=(num_actions,))

    def observation_space(self):
        return Box(
            low=0,
            high=float("inf"),
            shape=(2*self.initial_vehicles.num_vehicles,),
        )

    def _apply_rl_actions(self, rl_actions):
        rl_ids = self.k.vehicle.get_rl_ids()
        self.k.vehicle.apply_acceleration(rl_ids, rl_actions)

    def get_state(self, **kwargs):
        ids = self.k.vehicle.get_ids()
        pos = [self.k.vehicle.get_x_by_id(veh_id) for veh_id in ids]
        vel = [self.k.vehicle.get_speed(veh_id) for veh_id in ids]

        return np.concatenate((pos, vel))

    def compute_reward(self, rl_actions, **kwargs):
        ids = self.k.vehicle.get_ids()

        speeds = self.k.vehicle.get_speed(ids)

        return np.mean(speeds)

    
