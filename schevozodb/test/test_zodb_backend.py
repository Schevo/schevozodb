"""Run tests against zodb backend."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

import sys
from schevo.lib import optimize

from schevo.test.library import storage_classes


locals().update(storage_classes(class_label='zodb-1',
                                backend_name='zodb',
                                format=1,
                                ))
locals().update(storage_classes(class_label='zodb-2',
                                backend_name='zodb',
                                format=2,
                                ))


optimize.bind_all(sys.modules[__name__])  # Last line of module.
