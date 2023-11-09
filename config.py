"""Stores and serves all configuration options for the whole project.

This static class allows typed safe access to any configuration options globally.
"""
import os
from dotenv import load_dotenv


class Config:
    """Stores and serves all configuration options for the whole project.
    """

    instance: ""
    instance_color: ""
    instance_bgcolor: ""
    workdir: ""
    prefix_part: ""
    prefix_work: ""
    prefix_consumable: ""
    prefix_tool: ""
    prefix_machine: ""

    @staticmethod
    def init_config():
        load_dotenv()
        Config.instance = os.getenv("MFGDOCS_INSTANCE", "playground")
        Config.instance_color = os.getenv("MFGDOCS_INSTANCE_COLOR", "black")
        Config.instance_bgcolor = os.getenv("MFGDOCS_INSTANCE_BGCOLOR", "#f0f0f0")
        Config.workdir = os.getenv("MFGDOCS_WORKDIR", ".")
        Config.prefix_part = os.getenv("MFGDOCS_PREFIX_PART", "DS-001-")
        Config.prefix_work = os.getenv("MFGDOCS_PREFIX_WORK", "DS-WRK-")
        Config.prefix_machine = os.getenv("MFGDOCS_PREFIX_MACHINE", "DS-MAC-")
        Config.prefix_tool = os.getenv("MFGDOCS_PREFIX_TOOL", "DS-TOL-")
        Config.prefix_consumable = os.getenv("MFGDOCS_PREFIX_CONSUMABLE", "DS-CON-")
        Config.prefix_part = os.getenv("MFGDOCS_PREFIX_ROLE", "DS-ROL-")
        Config.prefix_work = os.getenv("MFGDOCS_PREFIX_LOCATION", "DS-LOC-")
        Config.inventree_url = os.getenv("INVENTREE_URL", "")


Config.init_config()
