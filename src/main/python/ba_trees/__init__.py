from default import *

from ba_trees.main import startup_main
from ba_trees.main_init.pre_main import premain

try:
    from ba_trees.gui.gui import *
    from ba_trees.gui.RenderWidget import *
except ImportError:
    pass

from ba_trees.main_init.main_main import main
from ba_trees.main_init.post_main import postmain