# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

class Restart(Exception):
    pass

class Exit(Exception):
    pass

class Retry(Exception):
    pass

class Kill(Exception):
    def __init__(self, p, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.player = p
