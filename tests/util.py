# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

import os.path
import numpy as np

def unique_model_name():
    return str(np.random.randint(1_000_000_000_000_000))

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")