from default import *

from .main_init.pre_main import premain

try:
    from .config import *
    from .gui import *
    from .workspace import *
except ImportError:
    pass

from .main_init.main_main import main
from .main_init.post_main import postmain