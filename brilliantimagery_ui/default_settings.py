import json
from pathlib import Path


class DefaultSettings:
    def __init__(self):
        self.path = Path('.') / 'default_settings.json'
        self.defaults = self.get_all()

    def get_all(self):
        with open(self.path, 'r') as f:
            try:
                return json.load(f)
            except:
                return {}

    def get(self, property_name: str, default=None):
        return self.defaults.get(property_name, default)

    def set(self, property_name: str, val: str):
        self.defaults[property_name] = val

        if self.defaults:
            with open(self.path, 'w') as f:
                j = json.dumps(self.defaults, indent=4)
                f.write(j)
