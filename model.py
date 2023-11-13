"""Contains entities used for the app.

"""


class Entity:
    """The Item represents one entity in the model"""
    pk = None
    key = ''
    keywords = ''
    def set_id(self, pk):
        self.pk = pk

    def get_id(self):
        return self.pk

    def from_dict(self, d: dict):
        self.pk = d.get('pk', '')
        self.key = d.get('key', '')
        self.keywords = d.get('keywords', '')

    def to_dict(self):
        return {'pk': self.pk,
                'key': self.key,
                'keywords': self.keywords}

    def extrakeys(self):
        return None


class Resource(Entity):
    """A simple resource entity, like a tool,a machine or a role.
    """

    def __init__(self):
        self.url = ''
        self.name = ''
        self.description = ''
        self.image = ''
        self.color = ''

    def to_dict(self):
        return super().to_dict()|{
                'url': self.url,
                'name': self.name,
                'description': self.description,
                'image': self.image,
                'color': self.color}

    def from_dict(self, d: dict):
        super().from_dict(d)
        self.name = d.get('name', '')
        self.description = d.get('description', '')
        self.image = d.get('image', '')
        self.color = d.get('color', '')


class Part(Resource):
    """Represents a basic part in the technology.
    """

    def __init__(self):
        super().__init__()
        self.bom = {}

    def to_dict(self):
        return super().to_dict()|{'bom': self.bom}

    def from_dict(self, d: dict):
        super().from_dict(d)
        self.bom = d.get('bom', {})


class Step(Resource):
    """Represents one build step in the manufacturing process, that results in outputs.

    The process itself uses the same tools and machines during all the subprocesses.
    """

    def __init__(self):
        super().__init__()
        self.acceptance = ''
        self.actions = {}
        self.inputparts = {}
        self.outputparts = {}
        self.tools = {}
        self.machines = {}
        self.roles = {}
        self.location = None
        self.start_after = {}
        self.start_after_start = {}
        self.prepare_hours = 0
        self.cooldown_hours = 0

    def from_dict(self, d: dict):
        super().from_dict(d)
        self.inputparts = d.get('inputparts', {})
        self.outputparts = d.get('outputparts', {})
        self.tools = d.get('tools', {})
        self.machines = d.get('machines', {})
        self.roles = d.get('roles', {})
        self.location = d.get('location', None)
        self.actions = d.get('actions', {})
        self.acceptance = d.get('acceptance', '')
        self.start_after = d.get('start_after', {})
        self.start_after_start = d.get('start_after_start', {})
        self.prepare_hours = d.get('prepare_time', 0)
        self.cooldown_hours = d.get('cooldown_time',0)

    def to_dict(self):
        return super().to_dict()|{
                'inputparts': self.inputparts,
                'outputparts': self.outputparts,
                'tools': self.tools,
                'machines': self.machines,
                'roles': self.roles,
                'actions': self.actions,
                'location': self.location,
                'acceptance': self.acceptance,
                'start_after': self.start_after,
                'start_after_start': self.start_after_start,
                'prepare_hours': self.prepare_hours,
                'cooldown_hours': self.cooldown_hours}

    def get_relations(self, key):
        response = {}
        if key in self.inputparts:
            response['inputparts'] = True
        if key in self.outputparts:
            response['outputparts'] = True
        if key in self.actions:
            response['actions'] = True
        if key in self.tools:
            response['tools'] = True
        if key in self.machines:
            response['machines'] = True
        if key in self.roles:
            response['roles'] = True
        if key in self.start_after:
            response['start_after'] = True
        if key in self.start_after_start:
            response['start_after_start'] = True
        if key == self.location:
            response['location'] = True
        return response

    def has_relation_to(self, key):
        return (key in self.inputparts or
                key in self.outputparts or
                key in self.tools or
                key in self.actions or
                key in self.roles or
                key in self.machines or
                key == self.location
                or key in self.start_after
                or key in self.start_after_start)

    def extrakeys(self):
        if self.key is not None:
            return {'key': self.key}
        return None

    def add_inputpart(self, partkey, amount):
        if partkey in self.inputparts:
            self.inputparts[partkey] += amount
        else:
            self.inputparts[partkey] = amount

    def remove_inputpart(self, partkey):
        if partkey in self.inputparts:
            del self.inputparts[partkey]

    def add_outputpart(self, partkey, amount):
        if partkey in self.outputparts:
            self.outputparts[partkey] += amount
        else:
            self.outputparts[partkey] = amount

    def remove_outputpart(self, partkey):
        if partkey in self.outputparts:
            del self.outputparts[partkey]

    def add_tool(self, partkey, amount):
        if partkey in self.tools:
            self.inputparts[partkey] += amount
        else:
            self.inputparts[partkey] = amount

    def remove_tool(self, partkey):
        if partkey in self.tools:
            del self.tools[partkey]

    def add_action(self, key, amount):
        if key in self.actions:
            self.inputparts[key] += amount
        else:
            self.inputparts[key] = amount

    def remove_action(self, key):
        if key in self.actions:
            del self.actions[key]

    def add_machine(self, partkey, amount):
        if partkey in self.machines:
            self.inputparts[partkey] += amount
        else:
            self.inputparts[partkey] = amount

    def remove_machine(self, partkey):
        if partkey in self.machines:
            del self.machines[partkey]

    def add_role(self, partkey, amount):
        if partkey in self.roles:
            self.roles[partkey] += amount
        else:
            self.roles[partkey] = amount

    def remove_role(self, partkey):
        if partkey in self.roles:
            del self.roles[partkey]

    def add_start_after(self, stepkey, amount):
        self.start_after[stepkey] = amount

    def remove_start_after(self, stepkey):
        if stepkey in self.start_after:
            del self.start_after[stepkey]

    def add_start_after_start(self, stepkey, amount):
        self.start_after_start[stepkey] = amount

    def remove_start_after_start(self, stepkey):
        if stepkey in self.start_after_start:
            del self.start_after_start[stepkey]

    def set_location(self, locationkey):
        self.location = locationkey

    def set_prepare_hours(self, prepare_hours: float):
        self.prepare_hours = prepare_hours

    def set_cooldown_hours(self, cooldown_hours: float):
        self.cooldown_hours = cooldown_hours
