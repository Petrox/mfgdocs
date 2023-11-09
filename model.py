"""Contains entities used for the app.

"""


class Entity:
    """The Item represents one entity in the model"""
    pk = None

    def set_id(self, pk):
        self.pk = pk

    def get_id(self):
        return self.pk

    def from_dict(self, d: dict):
        pass

    def to_dict(self):
        return {'id': self.pk}


class Resource(Entity):
    """A simple resource entity, like a tool,a machine or a role.
    """
    identifier = ''
    url = ''
    name = ''
    description = ''
    image = ''

    def to_dict(self):
        return {'pk': self.pk,
                'identifier': self.identifier,
                'url': self.url,
                'name': self.name,
                'description': self.description,
                'image': self.image}

    def from_dict(self, d: dict):
        self.pk = d['pk']
        self.identifier = d['identifier']
        self.name = d['name']
        self.description = d['description']
        self.image = d['image']


class BuildStep(Entity):
    """Represents one build step in the manufacturing process, that results in outputs.

    The process itself uses the same tools and machines during all the subprocesses.
    """
    inputparts = {}
    outputparts = {}
    tools = {}
    machines = {}
    roles = {}
    location = None
    start_after = {}
    start_after_start = {}
    substeps = {}
    title = ''
    text = ''
    prepare_hours = 0
    cooldown_hours = 0

    def from_dict(self, d: dict):
        self.pk = d['pk']
        self.inputparts = d['inputparts']
        self.outputparts = d['outputparts']
        self.tools = d['tools']
        self.machines = d['machines']
        self.roles = d['roles']
        self.title = d['title']
        self.text = d['text']
        self.location = d['location']
        self.start_after = d['start_after']
        self.start_after_start = d['start_after_start']
        self.prepare_hours = d['prepare_time']
        self.cooldown_hours = d['cooldown_time']

    def to_dict(self):
        return {'pk': self.pk,
                'inputparts': self.inputparts,
                'outputparts': self.outputparts,
                'tools': self.tools,
                'machines': self.machines,
                'roles': self.roles,
                'location': self.location,
                'text': self.text,
                'title': self.title,
                'start_after': self.start_after,
                'start_after_start': self.start_after_start,
                'prepare_hours': self.prepare_hours,
                'cooldown_hours': self.cooldown_hours}

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
