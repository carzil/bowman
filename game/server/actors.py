from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 700
    axe_damage_mod = int(choise[x for x in range(150, 180, 5)])
    bow_damage_mod = int(choise[x for x in range(70, 115, 5)])
    spear_damage_mod = int(choise[x for x in range(125, 150, 5)])

class Damager(NetBowman):
    health = 480
    axe_damage_mod = int(choise[x for x in range(180, 230, 5)])
    bow_damage_mod = int(choise[x for x in range(100, 135, 5)])
    spear_damage_mod = int(choise[x for x in range(140, 165, 5)])

class Tank(NetBowman):
    health = 1200
    axe_damage_mod = int(choise[x for x in range(200, 250, 5)])
    bow_damage_mod = int(choise[x for x in range(50, 80, 5)])
    spear_damage_mod = int(choise[x for x in range(80, 115, 5)])
