import pygame

from src import world
from src.cell import Cell
from src.world import World

# import serial
# ser = serial.Serial()  # open serial port
# print(ser.name)         # check which port was really used
# ser.write(b'hello')     # write a string
# ser.close()             # close port

s = World("0123456f",14,64,36)

ABOVE = LEFT = 1
BELOW = RIGHT = -1
HIT = 0

pygame.mixer.init()

target = pygame.mixer.Sound("./wav/smb2_coin.wav")
stomp = pygame.mixer.Sound("./wav/smw_stomp.wav")
pygame.mixer.music.load("./wav/POL-final-sacrifice-short.wav")
pygame.mixer_music.set_volume(0.6)


# Funktionen zur relativen Distanzbestimmung.
def x_distance(source: Cell, target2: Cell) -> int:
    if source.x - target2.x > 0: return LEFT
    if source.x - target2.x == 0: return HIT
    if source.x - target2.x < 0: return RIGHT


def y_distance(source: Cell, target2: Cell) -> int:
    if source.y - target2.y > 0: return ABOVE
    if source.y - target2.y == 0: return HIT
    if source.y - target2.y < 0: return BELOW


# Überprüfen, ob Spiel überhaupt gewonnen werden kann.
def unwinnable() -> bool:
    for target2 in s.targets:
        for box2 in s.boxes:
            # Box ist am unteren Rand, Ziel ist jedoch oberhalb Box
            if y_distance(box2, target2) == ABOVE and box2.y == s.h - 1: return True
            # Box ist am oberen Rand, Ziel ist jedoch unterhalb Box
            if y_distance(box2, target2) == BELOW and box2.y == 0: return True
            # Box ist am rechten Rand, Ziel ist jedoch links von Box
            if x_distance(box2, target2) == LEFT and box2.x == s.SIZE - 1: return True
            # Box ist am linken Rand, Ziel ist jedoch rechts von Box
            if x_distance(box2, target2) == RIGHT and box2.x == 0: return True
    return False

if unwinnable():
    print("Spiel kann nicht gewonnen werden!")
    font = pygame.font.SysFont(None, 100)
    text = font.render("Unlösbar!", True, world.WHITE)
    s.screen.blit(text, (
        s.screen.get_width() // 2 - text.get_width() // 2, s.screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    exit(0)


pygame.mixer.music.play(-1)

n = 0
s.get_box(n)
s.get_target(n)

# Spieler ausrücken, wenn auf einer Spalte mit Box
if x_distance(s.me, s.box) == HIT:
    if s.me.x > 0:
        s.left()
    else:
        s.right()

# # Spieler ausrücken, wenn in einer Zeile mit Box
if y_distance(s.me, s.box) == HIT:
    if s.me.y > 0:
        s.up()
    else:
        s.down()

while not s.winning():
    while n < len(s.boxes):

        s.get_box(n)
        s.get_target(n)

        while True:
            while True:
                # Ziel ist links von Box
                if x_distance(s.box, s.target) == LEFT:
                    # Spieler nach links bewegen, wenn Box weiter links von Spieler
                    if s.me.x - s.box.x > LEFT: s.left()
                    # Spieler nach rechts bewege, wenn Box weniger links (also rechts) von Spieler
                    if s.me.x - s.box.x < LEFT: s.right()
                    # Spieler nicht mehr bewegen, wenn Box genau links neben Spieler
                    if s.me.x - s.box.x == LEFT: break
                # Ziel ist rechts von Box
                if x_distance(s.box, s.target) == RIGHT:
                    # Spieler nach links bewegen, wenn Box weiter links von Spieler
                    if s.me.x - s.box.x > RIGHT: s.left()
                    # Spieler nach rechts bewegen, wenn Box weniger links (also rechts) von Spieler
                    if s.me.x - s.box.x < RIGHT: s.right()
                    # Spieler nicht mehr bewegen, wenn Box genau rechts neben Spieler
                    if s.me.x - s.box.x == RIGHT: break
                # Ziel ist über oder unter Box
                if x_distance(s.box, s.target) == HIT: break

            # Aufholen U/D
            while True:
                # Wenn Spieler unterhalb Box
                if s.me.y - s.box.y > HIT: s.up()
                # Wenn Spieler oberhalb Box
                if s.me.y - s.box.y < HIT: s.down()
                # Spieler anhalten, wenn auf gleicher Höhe mit Box
                if s.me.y - s.box.y == HIT: break

            # Schub der Box L/R
            stomp.play()
            while True:
                # Wenn Box rechts von Ziel
                if s.box.x - s.target.x > HIT: s.left()
                # Wenn Box links von Ziel
                if s.box.x - s.target.x < HIT: s.right()
                # Wenn Box ober- oder unterhalb von Ziel
                if s.box.x - s.target.x == HIT: break

            # Um die Ecke laufen:
            # Spieler nach unten bewegen, wenn Ziel oberhalb Box
            if y_distance(s.box, s.target) == ABOVE:
                s.down()
            # Spieler nach oben bewegen, wenn Ziel unterhalb Box
            if y_distance(s.box, s.target) == BELOW:
                s.up()
            # Spieler nach links bewegen, wenn Box links von Spieler
            if x_distance(s.me, s.box) == LEFT:
                s.left()
            # Spieler nach rechts bewegen, wenn Box rechts von Spieler
            if x_distance(s.me, s.box) == RIGHT:
                s.right()

            # Zur Box aufholen L/R (falls nötig)
            while True:
                if s.box.x == s.target.x: break;
                # Wenn Spieler rechts von Box
                if s.me.x - s.box.x > HIT: s.left()
                # Wenn Spieler links von Box
                if s.me.x - s.box.x < HIT: s.right()
                if s.me.x - s.box.x == HIT: break

            # Schub der Box U/D
            stomp.play()
            while True:
                # Wenn Ziel oberhalb von Box, Spieler nach oben bewegen
                if y_distance(s.box, s.target) == ABOVE: s.up()
                # Wenn Ziel unterhalb von Box, Spieler nach unten bewegen
                if y_distance(s.box, s.target) == BELOW: s.down()
                # Wenn Box auf Höhe von Ziel, Spieler stoppen
                if y_distance(s.box, s.target) == HIT: break

            if s.has_box(s.target):
                pygame.mixer.Sound.play(target)
                n += 1
                break
