TEMPLATE = """from clustack.builder import Builder

class {}Builder(Builder):
    def __init__(self):
        self.url = '{}'
        self.name = '{}'
        self._version = '{}'

"""

import os

from utils import sys_command

import settings

def generate_builder(name, url):
    version = "1.0.0"

    template_contents = TEMPLATE.format(
        name,
        url,
        name,
        version
    )

    builder_dir = settings.package_dir

    filename = name.lower() + '.py'

    full_path_name = os.path.join(builder_dir, filename)

    with open(full_path_name, 'w') as f:
        f.write(template_contents)

    sys_command(['vim', full_path_name])
