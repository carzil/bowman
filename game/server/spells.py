class Spell():
    mana = 0

    def count_damage(self, player, opponent, r):
        pass

class FireBall(Spell):
    mana = 150
    
    def count_damage(self, player, opponent, r):
        return False, 210

class HealthBreak(Spell):
    mana = 520

    def count_damage(self, player, opponent, r):
        return False, opponent.health // 4
