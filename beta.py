from time import sleep

import sokoban

str_a = "s0123456"  # RRRRRRUUUUUULLLDLU
str_b = "s0596553"  # DDDDDDDDRRRRRRRRRRDRUUU
str_c = "s0596553a" # RRDLLLLLLLLLLLLLDLUUUU
str_d = "s0596553b" # RRRRRRRRRRRRRRRRDDDDDLLLLLLULDDDD
str_e = "s0596553c" # LLDDDRRRRRRRDRUUUUUUUU
str_f = "s0596553d" # nicht gewinnbar
str_g = "s0596553e" # URRDLLLLULD
str_h = "s0596553f" # RRRRRRRRDDDRRRRRRRRRURDDDDDDDDDDDDD
str_i = "s0596553g" # LLLLLLLLLLLLLLLLLDDDDDDDDDDDLUUUUUUUUUUUUUU
str_j = "s0596553h" # LLLLLLLLLLLUUUUUURRRRRRDRUUUUUUUU
str_k = "s0596553q" # nicht gewinnbar

# World instantiieren
s = sokoban.World(str_g,40,20)

# Konstanten zur relativen Bestimmung
LEFT = ABOVE = -1
RIGHT = BELOW = 1
HIT = 0

def is_winnable():
    """
    Überprüft, ob das aktuelle Spiel gewonnen werden kann.
    :return: False, wenn Spiel nicht gewonnen werden kann, ansonsten True
    """
    pos = calculate_rel_pos(s.target, s.box)

    # Noch nicht alle Zustände sind erfasst.
    if pos[1] == ABOVE and s.box.y == s.h - 1: return False
    if pos[1] == BELOW and s.box.y == 0: return False
    if pos[0] == LEFT and s.box.x == s.w - 1: return False
    if pos[0] == RIGHT and s.box.x == 0: return False
    if s.target.y == 0 and s.box.x == 0 and s.target.x != 0: return False
    return True


def calculate_rel_pos(a: sokoban.Cell, b: sokoban.Cell):
    """
    Berechnet die relative Position einer Zelle in Bezug auf die Zielzelle.
    :param a: Zielzelle
    :param b: Zelle, deren Position ermittelt werden soll
    :return: list[px, py] (siehe Positionskonstanten)
    """
    dx = a.x - b.x
    dy = a.y - b.y

    output = []

    match dx:
        case dx if dx < HIT: output.append(LEFT)
        case dx if dx > HIT: output.append(RIGHT)
        case _:
            if b.x == 0: output.append(LEFT)
            else: output.append(RIGHT)

    match dy:
        case dy if dy < HIT: output.append(ABOVE)
        case dy if dy > HIT: output.append(BELOW)
        case _:
            if b.y == 0: output.append(ABOVE)
            else: output.append(BELOW)

    return output


def step_out():
    if s.box.x - s.me.x == HIT:
        if s.box.x > 0: s.left()
        else: s.right()
    if s.box.y - s.me.y == HIT:
        if s.box.y > 0: s.up()
        else: s.down()


def run_vector(a: sokoban.Cell, b: sokoban.Cell, px: int=HIT, py: int=HIT, turn: bool = False):
    """
    Bewegt Spieler entlang des Vektors b->a.
    :param turn: Bewegt Spieler nach x-Bewegung um 90 Grad in relativer Richtung
    :param a: Zielzelle
    :param b: Startzelle
    :param px: relative x-Position
    :param py: relative y-Position
    :return: void
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

    if turn:
        if ty < py: s.down()
        if ty > py: s.up()
        if tx < px: s.left()
        if tx > px: s.right()

        if dy != 0:
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


# relative Position der Box zum Ziel ermitteln
target_pos = calculate_rel_pos(s.target, s.box)

# Kurz warten
sleep(1)

# Spielablauf starten
step_out()

if is_winnable():
    while not s.winning():
        run_vector(s.box, s.me, target_pos[0])
        run_vector(s.target, s.box, turn=True)

else:
    print("Dieses Spiel kann leider nicht gewonnen werden.", end="")
    sleep(3)
    exit(0)

