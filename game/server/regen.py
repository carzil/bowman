class Regen():
    name = "regen"

    def __init__(self, regen_mod=10):
        self.regen_mod = regen_mod

    def regen(self):
        return self.regen_mod
