import sys
from freeorion_tools.charts_handler import charting_text
from traceback import print_exc
from shlex import split
import os

from common.option_tools import get_option_dict, HANDLERS
from common.listeners import register_pre_handler


def init_handlers(config_str, search_dir):
    handlers = split(get_option_dict()[HANDLERS])

    for handler in handlers:
        module = os.path.basename(handler)[:-3]

        # There is 3 way to specify path:
        # - absolute path to module
        # - single name, then module should be in same directory as config
        # - relative path, then use python as base path.
        if os.path.exists(handler):
            module_path = os.path.dirname(handler)
        elif not os.path.dirname(handler):
            module_path = os.path.dirname(config_str)
        else:
            module_path = os.path.join(search_dir, '..', os.path.dirname(handler))
        sys.path.insert(0, module_path)
        try:
            __import__(module)
        except Exception as e:
            for p in sys.path:
                print p
            print >> sys.stderr, "Fail to import handler %s with error %s" % (handler, e)
            print_exc()
            exit(1)
        register_pre_handler('generateOrders', charting_text)
