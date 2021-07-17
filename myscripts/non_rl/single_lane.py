from flow.controllers import IDMController
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.params import VehicleParams, InFlows, SumoCarFollowingParams, SumoLaneChangeParams
from flow.envs import TestEnv
from flow.core.params import TrafficLightParams
from myscripts.nets.single_lane import SingleLane
from myscripts.nets.single_lane import ADDITIONAL_NET_PARAMS
from flow.envs.ring.accel import ADDITIONAL_ENV_PARAMS
#from myscripts.envs.single_lane import SingleLaneEnv


vehicles = VehicleParams()
vehicles.add(
    veh_id="human",
    acceleration_controller=(IDMController, {}),
    car_following_params=SumoCarFollowingParams(min_gap=0.5),
    lane_change_params=SumoLaneChangeParams(
        model="SL2015",
        lc_sublane=2.0,
        ),
    )

inflow = InFlows()
inflow.add(
    veh_type="human",
    edge="before_tl",
    vehs_per_hour=1000,
    depart_lane="free",
    depart_speed=20
)


sim_params = SumoParams(sim_step=0.1, render=True, lateral_resolution=0.1)
env_params = EnvParams(horizon=2000, additional_params=ADDITIONAL_ENV_PARAMS.copy())
net_params = NetParams(inflows=inflow, additional_params=ADDITIONAL_NET_PARAMS.copy())

tl_logic =  TrafficLightParams(baseline = False)
phases = [{"duration": "31", "minDur": "8", "maxDur": "45", "state": "GrGr"},
          {"duration": "6", "minDur": "3", "maxDur": "6", "state": "yryr"},
          {"duration": "31", "minDur": "8", "maxDur": "45", "state": "rGrG"},
          {"duration": "6", "minDur": "3", "maxDur": "6", "state": "ryry"}]

offset = random.randint(0, 37)
tl_logic.add("t.l.", phases=phases, offset=offset)

flow_params = dict(
    exp_tag='single_lane',
    env_name=TestEnv,
    network=SingleLane,
    simulator='traci',
    sim=sim_params,
    env=env_params,
    net=net_params,
    veh=vehicles,
    initial=InitialConfig(),
    tls = tl_logic
)

