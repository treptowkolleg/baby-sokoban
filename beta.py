from time import sleep

import sokoban

s = sokoban.World("s09876543a")

# Konstanten zur relativen Bestimmung
LEFT = ABOVE = -1
RIGHT = BELOW = 1
HIT = 0

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
while not s.winning():
    run_vector(s.box, s.me, target_pos[0])
    run_vector(s.target, s.box, 0, 0, True)


