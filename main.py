from Classes.Game import Person, Colours
from Classes.magic import Spell
from Classes.inventory import Item
import random

# this is a list (array) of objects
'''magic = [{"name": "Fire", "cost": 10, "dmg": 120},
         {"name": "Thunder", "cost": 10, "dmg": 100},
         {"name": "Blizzard", "cost": 10, "dmg": 50}]'''

# list of spells
fire = Spell("Fire", 12, 120, "Cast")
thunder = Spell("Thunder", 15, 150, "Cast")
blizzard = Spell("Blizzard", 10, 80, "Cast")
meteor = Spell("Meteor", 20, 200, "Cast")
quake = Spell("Quake", 14, 100, "Cast")
light_cure = Spell("Light Cure", 10, 120, "Divine")
minor_cure = Spell("Minor Cure", 15, 240, "Divine")

# list of items
potion = Item("Potion", "potion", "heals 50 HP", 50)
high_potion = Item("High Potion", "potion", "heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restore HP/MP", 9999)
high_elixer = Item("Mega_elixer", "elixer", "Fully restores HP/MP of all party", 9999)
grenade = Item("Grenade", "attack", "deals 500 damage", 500)

all_spells = [fire, thunder, blizzard, meteor, quake, light_cure, minor_cure]
enemy_spells = [fire, quake, light_cure]
all_items = [{"Item": potion, "Quantity": 15},
             {"Item": high_potion, "Quantity": 5},
             {"Item": super_potion, "Quantity": 5},
             {"Item": elixer, "Quantity": 5},
             {"Item": high_elixer, "Quantity": 2},
             {"Item": grenade, "Quantity": 5}]

player1 = Person("Valos:", 3260, 165, 132, 34, all_spells, all_items)
player2 = Person("Nick :", 4160, 165, 188, 34, all_spells, all_items)
player3 = Person("Robot:", 3089, 165, 174, 34, all_spells, all_items)
enemy1 = Person("Magus:", 10900, 165, 800, 25, enemy_spells, [])
enemy2 = Person("Imp1", 1250, 130, 560, 325, enemy_spells, [])
enemy3 = Person("Imp2", 1250, 130, 560, 325, enemy_spells, [])

enemies = [enemy1, enemy2, enemy3]
players = [player1, player2, player3]

running = True

print(Colours.FAIL + Colours.BOLD + "An enemy attacks!!" + Colours.ENDC)

while running:
    print("================================")
    print(Colours.BOLD + "Name                   HP                                  MP" + Colours.ENDC)
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player_choice = 9999
        if player.get_hp() > 0:
            chosen_enemy = player.choose_target(enemies)
            player.choose_action()
            player_choice = int(input("\n" + player.name + "Choose action:"))

        if player_choice == 0:
            continue

        if player_choice == 1:
            player_dmg = player.generate_damage()
            enemies[chosen_enemy].take_damage(player_dmg)
            print("\n", player.name, "hit " + enemies[chosen_enemy].name + " with", player_dmg,
                  "The Enemy HP is now has:", enemies[chosen_enemy]
                  .get_hp(), "\n")

        elif player_choice == 2:
            player.choose_magic()
            magic_choice = int(input("\nMagic choice:")) - 1

            if magic_choice == -1:
                continue

            # The spell variable here holds an object inside it at the index stipulated in the magic choice
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_dmg()

            current_player_mp = player.get_mp()

            if spell.cost > current_player_mp:
                print(Colours.FAIL + "\n", player.name, "does not have enough magic points\n" + Colours.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "Divine":
                player.heal(magic_dmg)
                print(Colours.OKGREEN, player.name, "has healed", str(magic_dmg), "points of damage" + Colours.ENDC,
                      "\n")
            elif spell.type == "Cast":
                enemies[chosen_enemy].take_damage(magic_dmg)
                print(Colours.OKBLUE, player.name, "hit " + enemies[chosen_enemy].name + " with", spell.name, "for",
                      str(magic_dmg),
                      "points of damage" + Colours.ENDC, "\n")

        elif player_choice == 3:
            player.choose_item()
            item_choice = int(input("Choose item to use")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["Item"]
            player.items[item_choice]["Quantity"] -= 1
            quant = player.items[item_choice]["Quantity"]
            if quant <= 0:
                print(Colours.FAIL + "\n", player.name, "has run out of " + item.name + Colours.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                print(Colours.OKGREEN + "\n", player.name, "has healed for " + str(item.prop) + "HP" + Colours.ENDC)

            elif item.type == "elixer":

                if item.name == "Mega_elixer":
                    for i in players:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                    else:
                        player.hp = player.max_hp
                        player.mp = player.max_mp

                print(Colours.OKGREEN + "\n Your HP amd MP are now at max" + Colours.ENDC)

            elif item.type == "attack":
                enemies[chosen_enemy].take_damage(item.prop)
                print(Colours.FAIL + "\n", player.name, "deals" + str(item.prop) + "points of damage to "
                      + enemies[chosen_enemy].name)

    for enemy in enemies:
        if enemy.get_hp() > 0:
            enemy_choice = random.randrange(0, 2)
            target = random.randrange(0, 3)
            if enemy_choice == 0:
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)
                print(Colours.FAIL + enemy.name + " hit", players[target].name, "with", str(enemy_dmg),
                      "points of damage" + Colours.ENDC)

            elif enemy_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                enemy.reduce_mp(spell.cost)

                if spell.type == "Divine":
                    enemy.heal(magic_dmg)
                    print(Colours.OKGREEN, enemy.name, "has healed", str(magic_dmg), "points of damage" + Colours.ENDC,
                          "\n")
                elif spell.type == "Cast":
                    players[target].take_damage(magic_dmg)
                    print(Colours.OKBLUE, enemy.name, "hit " + players[target].name + " with", spell.name, "for",
                          str(magic_dmg),
                          "points of damage" + Colours.ENDC, "\n")

    enemy_defeated = 0
    player_defeated = 0
    for enemy in enemies:
        if enemy.get_hp() <= 0:
            print(Colours.OKGREEN + enemy.name + " is dead" + Colours.ENDC)
            enemy_defeated += 1
            del enemy

        if enemy_defeated == len(enemies):
            print(Colours.OKGREEN + Colours.BOLD + "All enemies are dead! You have won" + Colours.ENDC)
            running = False

    for player in players:
        if player.get_hp() <= 0:
            print(Colours.FAIL + player.name + " is dead" + Colours.ENDC)
            player_defeated += 1

        if player_defeated == len(players):
            print(Colours.FAIL + Colours.BOLD + "All players are dead! You have won" + Colours.ENDC)
            running = False
