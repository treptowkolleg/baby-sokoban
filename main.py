from time import sleep

import sokoban
import serial
from serial.tools import list_ports

# Spiel auswählen
game = 0

# Ergebnisse für 20x20-Spielbrett
seed_list = [
"s0123456",         #  0 RRRRRRUUUUUULLLDLU
"s0596553",         #  1 DDDDDDDDRRRRRRRRRRDRUUU
"s0596553a",        #  2 RRDLLLLLLLLLLLLLDLUUUU
"s0596553b",        #  3 RRRRRRRRRRRRRRRRDDDDDLLLLLLULDDDD
"s0596553c",        #  4 LLDDDRRRRRRRDRUUUUUUUU
"s0596553d",        #  5 Dieses Spiel kann leider nicht gewonnen werden
"s0596553e",        #  6 URRDLLLLULD
"s0596553f",        #  7 RRRRRRRRDDDRRRRRRRRRURDDDDDDDDDDDDD
"s0596553g",        #  8 LLLLLLLLLLLLLLLLLDDDDDDDDDDDLUUUUUUUUUUUUUU
"s0596553h",        #  9 LLLLLLLLLLLUUUUUURRRRRRDRUUUUUUUU
"s0596553q",        # 10 Dieses Spiel kann leider nicht gewonnen werden
]

# Serial-Instanz
serial = serial.Serial()

# Ports prüfen und erstbesten zuweisen
ports = enumerate(list_ports.comports())
port = ""
for n, (p, descriptor, hid) in ports:
    print(p, descriptor, hid)
    serial.port = port
    serial.baudrate = 115200
    serial.timeout = 1
    break

# prüfen, ob Port vorhanden
if serial.port:
    # Port öffnen und ggf. Daten senden.
    serial.open()
    if serial.is_open:
        message = "0" # 0,1,2,3 → links, oben, rechts, unten
        message_barry = bytearray.fromhex(message)
        serial.write(message_barry)
        serial.flush()

# World instantiieren
s = sokoban.World(seed_list[game])

# Konstanten zur relativen Bestimmung
LEFT = ABOVE = -1
RIGHT = BELOW = 1
HIT = 0

# Polymorphie ausnutzen, daher spezialisierte Unterklassen.
class Target(sokoban.Cell):
    def __init__(self, x=None, y=None):
        super().__init__(x, y)

# cast Cell als Target-Instanz
s.target = Target(s.target.x, s.target.y)

def is_winnable():
    """
    Überprüft, ob das aktuelle Spiel gewonnen werden kann.
    :return: False, wenn Spiel nicht gewonnen werden kann, ansonsten True
    """
    pos = calculate_rel_pos(s.target, s.box)

    # Ziel [Richtung] von Box, Box jedoch am anderen Rand:
    if  pos[0] == LEFT and s.box.x == s.w - 1 or \
        pos[0] == RIGHT and s.box.x == 0 or \
        pos[1] == ABOVE and s.box.y == s.h - 1 or \
        pos[1] == BELOW and s.box.y == 0:
        return False

    # Ziel ganz oben oder ganz unten:
    if s.target.y in (0, s.h - 1):
        # Box links bzw. rechts, Ziel jeweils nicht
        if  s.box.x == 0 and s.target.x != 0 or \
            s.box.x == s.w - 1 and s.target.x != s.w - 1 :
            return False

    return True


def calculate_rel_pos(b: sokoban.Cell, a: sokoban.Cell):
    """
    Berechnet die relative Position einer Zelle A in Bezug zur Zelle B.
    :param b: Zelle, deren Position ermittelt werden soll
    :param a: Zielzelle
    :return: list[px, py] (siehe Positionskonstanten)
    """
    dx = a.x - b.x
    dy = a.y - b.y

    output = []

    if dx < HIT: output.append(LEFT)
    elif dx > HIT: output.append(RIGHT)
    else: output.append(LEFT if b.x == 0 else RIGHT)

    if dy < HIT: output.append(ABOVE)
    elif dy > HIT: output.append(BELOW)
    else: output.append(ABOVE if b.y == 0 else BELOW)

    return output


def step_out():
    """
    Spieler versetzen, falls in einer Linie mit Box. Erforderlich für Vektorlauf.
    :return: None
    """
    if s.box.x - s.me.x == HIT:
        if s.box.x > 0: s.left()
        else: s.right()
    if s.box.y - s.me.y == HIT:
        if s.box.y > 0: s.up()
        else: s.down()


def run_vector(b: sokoban.Cell, a: sokoban.Cell, px: int=HIT, py: int=HIT):
    """
    Bewegt Spieler entlang des Vektors b->a.
    :param b: Startzelle
    :param a: Zielzelle
    :param px: relative x-Position
    :param py: relative y-Position
    :return: None
    """
    tx = dx = a.x - b.x
    ty = dy = a.y - b.y

    while dx != px:
        match dx:
            case dx if dx < px:
                s.left()
                dx += 1
            case dx if dx > px:
                s.right()
                dx -= 1
            case _: break

    if s.has_target(s.box): return

    if isinstance(a, Target):
        if ty < py: s.down()
        if ty > py: s.up()
        if tx < px: s.left()
        if tx > px: s.right()

        if dy != HIT:
            if s.box.x - s.me.x < HIT: s.left()
            if s.box.x - s.me.x > HIT: s.right()

    while dy != py:
        match dy:
            case dy if dy < py:
                s.up()
                dy += 1
            case dy if dy > py:
                s.down()
                dy -= 1
            case _: break


# Spiel beginnen

# Gewinnchancen überprüfen
if not is_winnable():
    print("Dieses Spiel kann leider nicht gewonnen werden.", end="")
    sleep(3)
    exit(0)

# relative Position der Box zum Ziel ermitteln
target_pos = calculate_rel_pos(s.box, s.target)

# kurz warten
sleep(1)

# Spieler ggf. versetzen
step_out()

# Game-Loop
while not s.winning():
    run_vector(s.me, s.box, target_pos[0])
    run_vector(s.box, s.target)
