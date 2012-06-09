class Spell():
    mana = 0

    def count_damage(self, player, opponent, r):
        pass

class FireBall(Spell):
    mana = 600

    def count_damage(self, player, opponent, r):
        if player.mana < self.mana:
            return False, 200
        return True, 0
