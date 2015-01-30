
import os

from utils import sys_command

import settings

PYTHON_TEMPLATE = """from clustack.builder import Builder

class {}Builder(Builder):
    def __init__(self):
        self.url = '{}'
        self.name = '{}'
        self._version = '{}'

"""

YAML_TEMPLATE = """name: {}
url : {}
version : {}
"""

def generate_python_builder(name, url):
    version = "1.0.0"

    template_contents = PYTHON_TEMPLATE.format(
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

def generate_yaml_builder(name, url):
    version = "1.0.0"

    template_contents = YAML_TEMPLATE.format(
        name,
        url,
        version
    )

    # FIXME
    yaml_dir = os.path.join(os.getcwd(), 'yaml')

    filename = name.lower() + '.yaml'

    full_path_name = os.path.join(yaml_dir, filename)

    with open(full_path_name, 'w') as f:
        f.write(template_contents)

    sys_command(['vim', full_path_name])
