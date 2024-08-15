from os import environ

from metadrive.envs import MetaDriveEnv, SafeMetaDriveEnv, MultiAgentRoundaboutEnv, \
    MultiAgentIntersectionEnv, MultiAgentParkingLotEnv, MultiAgentTollgateEnv, \
    MultiAgentBottleneckEnv, MultiAgentMetaDrive, ScenarioEnv
from metadrive.utils.registry import get_metadrive_class
import os

MetaDrive_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
