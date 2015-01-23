import os
import sys

import settings

package_dir = os.path.join(os.getcwd(), 'clustack/packages')

sys.path.insert(0, package_dir)

settings.package_dir = os.path.join(os.getcwd(), 'clustack/packages')

