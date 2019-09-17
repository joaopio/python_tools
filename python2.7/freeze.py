import pkg_resources
import pkgutil

import os
import sys

if __name__ == "__main__":

    for mod in pkgutil.iter_modules():
        module_name = mod[1]
        try:
            module_version = pkg_resources.get_distribution(module_name).version

            print "{0} - {1}".format(module_name, module_version)
        except:
            pass
