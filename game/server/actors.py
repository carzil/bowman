from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 350
    axe_damage_mod = 50
    bow_damage_mod = 38
    spear_damage_mod = 44

class Damager(NetBowman):
    health = 200
    axe_damage_mod = 60
    bow_damage_mod = 70
    spear_damage_mod = 50

class Tank(NetBowman):
    health = 550
    axe_damage_mod = 70
    bow_damage_mod = 30
    spear_damage_mod = 36
