### Diese Datei main.py soll bearbeitet (editiert) werden.
### Wenn für die Lösung einer Übungsaufgabe eine Datei abgegeben werden soll, dann diese!
import pygame

import sokoban

# Benutzen Sie für die Abgaben Ihre eigene Matrikelnummer.
# Jede Matrikelnummer erzeugt eine andere Welt.
# In seltenen Fällen ist ihr Spiel nicht lösbar weil die z.B. Box am Rand steht. 
# Wenden sie sich in diesem Fall an den Dozenten um eine alternativen Startwert zu erhalten.
 
# Die hier angegebene Matrikelnummer erzeugt nur meine Referenzwelt die auch in der Doku verwendet wird, bitte ändern.

#s = sokoban.World("s0123456")
# using seed: s0123456 moves: RRRRRRUUUUUULLLDLU

#s = sokoban.World("s0596553")
# using seed: s0596553 moves: DDDDDDDDRRRRRRRRRRDRUUU

#s = sokoban.World("s0596553a")
# using seed: s0596553a moves: RRDLLLLLLLLLLLLLDLUUUU

#s = sokoban.World("s0596553b")
# using seed: s0596553b moves: RRRRRRRRRRRRRRRRDDDDDLLLLLLULDDDD

#s = sokoban.World("s0596553c")
# using seed: s0596553c moves: LLDDDRRRRRRRDRUUUUUUUU

s = sokoban.World("s0596553d")
# using seed: s0596553d moves:
# Spiel kann nicht gewonnen werden!

#s = sokoban.World("s0596553e")
# using seed: s0596553e moves: URRDLLLLULD

#s = sokoban.World("s0596553f")
# using seed: s0596553f moves: RRRRRRRRDDDRRRRRRRRRURDDDDDDDDDDDDD

#s = sokoban.World("s0596553g")
# using seed: s0596553g moves: DDDDDDDDDDDLLLLLLLLLLLLLLLLLLUUUUUUUUUUUUUU

#s = sokoban.World("s0596553h")
# using seed: s0596553h moves: LLLLLLLLLLLUUUUUURRRRRRDRUUUUUUUU

### BEGIN fügen sie unter dieser Zeile ihren Code zur Lösung ein.

# Konstanten für die relative Position.
ABOVE = LEFT = 1
BELOW = RIGHT = -1
HIT = 0

# Funktionen zur relativen Distanzbestimmung.
def x_distance(source: sokoban.Cell=s.box, target: sokoban.Cell=s.target):
    if source.x - target.x > 0: return LEFT
    if source.x - target.x == 0: return HIT
    if source.x - target.x < 0: return RIGHT

def y_distance(source: sokoban.Cell=s.box, target: sokoban.Cell=s.target):
    if source.y - target.y > 0: return ABOVE
    if source.y - target.y == 0: return HIT
    if source.y - target.y < 0: return BELOW

# Überprüfen, ob Spiel überhaupt gewonnen werden kann.
def unwinnable():
    if y_distance() == ABOVE and s.box.y == s.SIZE-1: return True
    if y_distance() == BELOW and s.box.y == 0: return True
    if x_distance() == LEFT and s.box.x == s.SIZE-1: return True
    if x_distance() == RIGHT and s.box.x == 0: return True
    return False

# Einmaliger Aufruf:
if unwinnable():
    print("Spiel kann nicht gewonnen werden!")
    font = pygame.font.SysFont(None, 100)
    text = font.render("Unlösbar!", True, sokoban.WHITE)
    s.screen.blit(text, (
    s.screen.get_width() // 2 - text.get_width() // 2, s.screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    print(".")
    exit(0)

if x_distance(s.me, s.box) == HIT:
    if s.me.x > 0:
        s.left()
    else:
        s.right()
if y_distance(s.me, s.box) == HIT:
    if s.me.y > 0:
        s.up()
    else:
        s.down()

# Schleife, bis Spiel gewonnen ist:
while not s.winning():

    while True:
        if x_distance() == LEFT:
            if s.me.x - s.box.x > LEFT: s.left()
            if s.me.x - s.box.x < LEFT: s.right()
            if s.me.x - s.box.x == LEFT: break
        if x_distance() == RIGHT:
            if s.me.x - s.box.x > RIGHT: s.left()
            if s.me.x - s.box.x < RIGHT: s.right()
            if s.me.x - s.box.x == RIGHT: break
        if x_distance() == HIT: break

    # Falls hier schon am Ziel
    s.winning()

    while True:
        if s.me.y - s.box.y > HIT: s.up()
        if s.me.y - s.box.y < HIT: s.down()
        if s.me.y - s.box.y == HIT: break

    # Falls hier schon am Ziel
    s.winning()

    while True:
        if s.box.x - s.target.x > HIT: s.left()
        if s.box.x - s.target.x < HIT: s.right()
        if s.box.x - s.target.x == HIT: break

    # Falls hier schon am Ziel
    s.winning()

    # Um die Ecke laufen:
    if y_distance() == ABOVE: s.down()
    if y_distance() == BELOW: s.up()
    if x_distance(s.me,s.box) == LEFT: s.left()
    if x_distance(s.me,s.box) == RIGHT: s.right()

    while True:
        if s.me.x - s.box.x > HIT: s.left()
        if s.me.x - s.box.x < HIT: s.right()
        if s.me.x - s.box.x == HIT: break

    while True:
        if y_distance(s.box, s.target) == ABOVE: s.up()
        if y_distance(s.box, s.target) == BELOW: s.down()
        if y_distance(s.box, s.target) == HIT: break

### END

# Idealerweie ist die Box jetzt auf dem Target und das Spiel gewonnen.
# Falls (noch) nicht, können sie den Sokoban mit der Tastatur (Pfeiltasten) bewegen.
# Ändern Sie ab hier nichts mehr. 

# manual keyboard control
# while not s.winning():
#     k = s.waitKey()
#     if k=='q':
#         break
#     if k == 'w':
#         s.up()
#     if k == 'a':
#         s.left()
#     if k == 's':
#         s.down()
#     if k == 'd':
#         s.right()

# ende, sie haben gewonnen