from game.server.exceptions import MoveInterrupt

class Spell():
    mana = 0

    def count_damage(self, player, opponent, r):
        pass

    def apply(self, player, opponent, r):
        pass

class FireBall(Spell):
    mana = 150
    
    def count_damage(self, player, opponent, r):
        if player.mana < self.mana:
            return False, 0
        return False, 210

class HealthBreak(Spell):
    mana = 520

    def count_damage(self, player, opponent, r):
        if player.mana < self.mana:
            return False, 0
        return False, opponent.health // 4

class Froze(Spell):
    def count_damage(self, player, opponent, r):
        return None, None

    def apply(self, player, opponent, r):
        return FrozeSpellResult()

class SpellResult():

    def check(self):
        pass

class FrozeSpellResult(SpellResult):
    moves = 1

    def check(self):
        if not self.moves:
            return False
        else:
            self.moves -= 1
            raise MoveInterrupt



