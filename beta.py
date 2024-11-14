
import sokoban

str_a = "s0123456"  # RRRRRRUUUUUULLLDLU
str_b = "s0596553"  # DDDDDDDDRRRRRRRRRRDRUUU
str_c = "s0596553a" # RRDLLLLLLLLLLLLLDLUUUU
str_d = "s0596553b" # RRRRRRRRRRRRRRRRDDDDDLLLLLLULDDDD
str_e = "s0596553c" # LLDDDRRRRRRRDRUUUUUUUU
str_f = "s0596553d" # nicht gewinnbar
str_g = "s0596553e" # URRDLLLLULD
str_h = "s0596553f" # RRRRRRRRDDDRRRRRRRRRURDDDDDDDDDDDDD
str_i = "s0596553g" # Glitch, nach Reparatur: LLLLLLLLLLLLLLLLLDDDDDDDDDDDLUUUUUUUUUUUUUU
str_j = "s0596553h" # LLLLLLLLLLLUUUUUURRRRRRDRUUUUUUUU

s = sokoban.World(str_i)

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
    if pos == ABOVE and s.box.y == s.h - 1: return False
    # Box ist am oberen Rand, Ziel ist jedoch unterhalb Box
    if pos == BELOW and s.box.y == 0: return False
    # Box ist am rechten Rand, Ziel ist jedoch links von Box
    if pos == LEFT and s.box.x == s.w - 1: return False
    # Box ist am linken Rand, Ziel ist jedoch rechts von Box
    if pos == RIGHT and s.box.x == 0: return False
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
        case _: output.append(HIT)

    match dy:
        case dy if dy < HIT: output.append(ABOVE)
        case dy if dy > HIT: output.append(BELOW)
        case _: output.append(HIT)

    return output


def step_out():
    rel_pos = calculate_rel_pos(s.box, s.me)

    if rel_pos[0] == HIT:
        if s.box.x > 0: s.left()
        else: s.right()

    if rel_pos[1] == HIT:
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

    if turn:
        match ty:
            case ty if ty < py: s.down()
            case ty if ty > py: s.up()
        match tx:
            case tx if tx < px: s.left()
            case tx if tx > px: s.right()

        # Beginn, Glitch-Reparatur
        if s.box.x - s.me.x < HIT: s.left()
        if s.box.x - s.me.x > HIT: s.right()
        # Ende, Glitch-Reparatur

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

# Spielablauf starten
step_out()

if is_winnable():
    while not s.winning():
        # Beginn, Glitch-Reparatur
        if target_pos[0] == HIT:
            target_pos[0] = target_pos[0]-1
        # Ende, Glitch-Reparatur
        run_vector(s.box, s.me, target_pos[0])
        run_vector(s.target, s.box, 0, 0, True)


else:
    print("Dieses Spiel kann leider nicht gewonnen werden.")
    exit(0)

