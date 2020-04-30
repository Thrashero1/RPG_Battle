import random


class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, attack, defense, magic, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.attack_low = attack - 10
        self.attack_high = attack + 10
        self.defense = defense
        self.magic = magic
        self.actions = ["Go Back to previous menu", "Attack", "Magic", "Items"]
        self.items = items

    def generate_damage(self):
        return random.randrange(self.attack_low, self.attack_high)

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, mp_cost):
        self.mp -= mp_cost

    def choose_action(self):
        i = 0
        print(Colours.BOLD + "\nChoose your actions " + self.name + Colours.ENDC)
        for item in self.actions:
            print("    ", str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(Colours.BOLD + Colours.UNDERLINE + "Available magic" + Colours.ENDC)
        for spell in self.magic:
            print("    ", str(i) + ":", spell.name, "cost:", str(spell.cost))
            i += 1

    def choose_item(self):
        i = 1
        print(Colours.OKBLUE + Colours.BOLD + "Available items" + Colours.ENDC)
        for item in self.items:
            print("    ", str(i), "name", item["Item"].name + ":", item["Item"].description, "quantity: " +
                  str(item["Quantity"]))
            i += 1

    def choose_target(self, enemy):
        i = 1
        print("\n" + Colours.FAIL + Colours.BOLD + "Choose target" + Colours.ENDC)
        for en in enemy:
            if en.get_hp() > 0:
                print(i, ":", en.name)
            i += 1
        choice = int(input("Choose your target: ")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        hp_ticks = ((self.hp / self.max_hp) * 100) / 2

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        full_hp = str(self.max_hp) + "/" + str(self.max_hp)
        hp_string = str(self.hp) + "/" + str(self.max_hp)
        add_space_hp = len(full_hp) - len(hp_string)
        hp_decreased = ""
        while add_space_hp > 0:
            hp_decreased += " "
            add_space_hp -= 1

        hp_string = hp_decreased + hp_string

        print(Colours.BOLD + self.name + "    " + hp_string + "   |" + Colours.FAIL + hp_bar + Colours.ENDC + "| ")

    def get_stats(self):
        hp_bar = ""
        hp_ticks = ((self.hp / self.max_hp) * 100) / 4

        mp_bar = ""
        mp_ticks = ((self.mp / self.max_mp) * 100) / 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        full_hp = str(self.max_hp) + "/" + str(self.max_hp)
        full_mp = str(self.max_mp) + "/" + str(self.max_mp)
        hp_string = str(self.hp) + "/" + str(self.max_hp)
        mp_string = str(self.mp) + "/" + str(self.max_mp)
        add_space_mp = len(full_mp) - len(mp_string)
        add_space_hp = len(full_hp) - len(hp_string)
        hp_decreased = ""
        mp_decreased = ""
        while add_space_hp > 0:
            hp_decreased += " "
            add_space_hp -= 1

        while add_space_mp > 0:
            mp_decreased += " "
            add_space_mp -= 1

        mp_string = mp_decreased + mp_string
        hp_string = hp_decreased + hp_string

        print(Colours.BOLD + self.name + "    " +
              hp_string + "   |" + Colours.OKGREEN + hp_bar +
              Colours.ENDC + "| " + Colours.BOLD + mp_string + "   |" + Colours.OKBLUE +
              mp_bar + Colours.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_dmg()

        if self.mp < 5:
            print("Not enough mp")
        elif spell.cost < self.mp:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg

