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