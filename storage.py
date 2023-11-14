"""
Handles overall in-memory data.

"""
import os
from cache import Cache
from config import Config
import json
from model import Resource, Step, Part


class Storage:
    """Stores data in memory and handles loading and saving.

    """

    def __init__(self, mfgdocsapp):
        self.cache_actions = Cache('actions')
        self.cache_roles = Cache('roles')
        self.cache_tools = Cache('tools')
        self.cache_steps = Cache('buildsteps')
        self.cache_parts = Cache('parts')
        self.cache_locations = Cache('locations')
        self.cache_machines = Cache('machines')
        self.cache_consumables = Cache('consumables')
        self.mfgdocsapp = mfgdocsapp
        self.load_resources()

    def load_resources(self):
        self.load_json(self.cache_roles, '/data/roles.json', Resource)
        self.load_json(self.cache_tools, '/data/tools.json', Resource)
        self.load_json(self.cache_actions, '/data/actions.json', Resource)
        self.load_json(self.cache_parts, '/data/parts.json', Part)
        self.load_json(self.cache_locations, '/data/locations.json', Resource)
        self.load_json(self.cache_machines, '/data/machines.json', Resource)
        self.load_json(self.cache_consumables, '/data/consumables.json', Resource)
        self.load_json(self.cache_steps, '/data/buildsteps.json', Step)

    def load_json(self, cache, filename, classname):
        f_name = Config.workdir+filename.replace('/', os.sep)
        try:
            with open(f_name, mode='rt', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                for key in json_data.keys():
                    item = classname()
                    item.from_dict(json_data[key])
                    cache.add(key, item, item.extrakeys())
        except OSError as e:
            self.mfgdocsapp.log(f'storage.load_json error: {e}')
