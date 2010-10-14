"""
    model.py
    Eastwind config models
"""

import json

class EastwindAction:
    """ Class for eastwind atomic actions """

    def __init__(self, arg_hash):
        """
            Initialize a single action with a dict(hash), for example:
            action = EastwindAction({'install': 'vim'})
        """
        self.type = arg_hash.keys()[0]
        self.arg = arg_hash[self.type]

    def to_dict(self):
        """ Convert to dict format """
        return {self.type: self.arg}

class EastwindSet:
    """ A set of eastwind actions"""

    def __init__(self, filename=''):
        """ Init and load from json if filename provided """
        self.name = ''
        self.actions = []
        self.filename = filename

        if filename != '':
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.name = data['name']
                for action in data['actions']:
                    self.actions.append(EastwindAction(action))

    @classmethod
    def touch(self, filename, name=''):
        with open(filename, "w") as f:
            json.dump({'name': name, 'actions': []}, f, sort_keys=True, indent=4)

    def to_dict(self):
        """ Convert to dict format """
        return {'name': self.name,
                'actions': [act.to_dict() for act in self.actions]}

    def dump(self, filename=''):
        """ Dump to json file """
        if filename == '':
            filename = self.filename
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, sort_keys=True, indent=4)

