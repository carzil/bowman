class Spell():
    mana = 0

    def count_damage(self, player, opponent, r):
        pass

class FireBall(Spell):
    mana = 140
    
    def count_damage(self, player, opponent, r):
        if player.mana < self.mana:
            return False, 0
        return False, 240

class HealthBreak(Spell):
    mana = 200

    def count_damage(self, player, opponent, r):
        if player.mana < self.mana:
            return False, 0
        return False, opponent.health // 5
