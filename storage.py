"""
Handles overall in-memory data.

"""
import os
from cache import Cache
from config import Config
import json
from model import Step, Part, Role, Tool, Action, Location, Machine, Consumable, Company


class Storage:
    """Stores data in memory and handles loading and saving.

    """

    def __init__(self, mfgdocsapp):
        self.cache_actions = Cache('actions')
        self.cache_roles = Cache('roles')
        self.cache_tools = Cache('tools')
        self.cache_steps = Cache('steps')
        self.cache_parts = Cache('parts')
        self.cache_locations = Cache('locations')
        self.cache_companies = Cache('companies')
        self.cache_machines = Cache('machines')
        self.cache_consumables = Cache('consumables')
        self.mfgdocsapp = mfgdocsapp
        self.load_resources()

    def cache_by_resource_type(self, resource_type):
        cache_map = {
            'actions': self.cache_actions,
            'roles': self.cache_roles,
            'tools': self.cache_tools,
            'steps': self.cache_steps,
            'parts': self.cache_parts,
            'companies': self.cache_companies,
            'locations': self.cache_locations,
            'machines': self.cache_machines,
            'consumables': self.cache_consumables,
        }
        if resource_type in cache_map:
            return cache_map[resource_type]
        return None

    def get_resource_by_type_and_key(self, res_type: str, key: str):
        print(f'storage.get_resource_by_type_and_key({res_type}, {key})')

        cache_map = {
            'actions': self.cache_actions,
            'roles': self.cache_roles,
            'tools': self.cache_tools,
            'steps': self.cache_steps,
            'parts': self.cache_parts,
            'companies': self.cache_companies,
            'locations': self.cache_locations,
            'machines': self.cache_machines,
            'consumables': self.cache_consumables,
        }
        if res_type == 'parts':
            key, stepkey = Part.extract_stepkey(key)
        if res_type in cache_map:
            return cache_map[res_type].get_by_unique_key('key', key)

        print(f'storage.get_resource_by_type_and_key({res_type}, {key}) unknown type {res_type}')
        return None

    def load_resources(self):
        self.load_json(self.cache_roles, '/data/roles.json', Role)
        self.load_json(self.cache_tools, '/data/tools.json', Tool)
        self.load_json(self.cache_actions, '/data/actions.json', Action)
        self.load_json(self.cache_parts, '/data/parts.json', Part)
        self.load_json(self.cache_locations, '/data/locations.json', Location)
        self.load_json(self.cache_machines, '/data/machines.json', Machine)
        self.load_json(self.cache_consumables, '/data/consumables.json', Consumable)
        self.load_json(self.cache_companies, '/data/companies.json', Company)
        self.load_json(self.cache_steps, '/data/steps.json', Step)

    def save_resources(self):
        self.save_json(self.cache_roles.data, '/data/roles.json')
        self.save_json(self.cache_tools.data, '/data/tools.json')
        self.save_json(self.cache_actions.data, '/data/actions.json')
        self.save_json(self.cache_parts.data, '/data/parts.json')
        self.save_json(self.cache_locations.data, '/data/locations.json')
        self.save_json(self.cache_machines.data, '/data/machines.json')
        self.save_json(self.cache_consumables.data, '/data/consumables.json')
        self.save_json(self.cache_companies.data, '/data/companies.json')
        self.save_json(self.cache_steps.data, '/data/steps.json')

    def load_json(self, cache, filename, classname, no_clear_before_load=False):
        if not no_clear_before_load:
            cache.clear()
        f_name = Config.workdir + filename.replace('/', os.sep)
        try:
            with open(f_name, mode='rt', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                for key in json_data.keys():
                    item = classname()
                    item.from_dict(json_data[key])
                    extrakeys = item.extrakeys()
                    cache.add(key, item, extrakeys)
        except OSError as e:
            self.mfgdocsapp.log(f'storage.load_json error: {e}')

    def save_json(self, data: dict, filename: str):
        f_name = Config.workdir + filename.replace('/', os.sep)
        fulldict = {}
        for k, v in data.items():
            fulldict[k] = v.to_dict()
        try:
            with open(f_name, mode='wt', encoding='utf-8') as json_file:
                json.dump(fulldict, json_file, indent=4, sort_keys=True)
        except OSError as e:
            self.mfgdocsapp.log(f'storage.save_json error: {e}')
