### Diese Datei main.py soll bearbeitet (editiert) werden.
### Wenn für die Lösung einer Übungsaufgabe eine Datei abgegeben werden soll, dann diese!
import pygame

import sokoban

# Benutzen Sie für die Abgaben Ihre eigene Matrikelnummer.
# Jede Matrikelnummer erzeugt eine andere Welt.
# In seltenen Fällen ist ihr Spiel nicht lösbar weil die z.B. Box am Rand steht. 
# Wenden sie sich in diesem Fall an den Dozenten um eine alternativen Startwert zu erhalten.
 
# Die hier angegebene Matrikelnummer erzeugt nur meine Referenzwelt die auch in der Doku verwendet wird, bitte ändern.

s = sokoban.World("s0123456")
# using seed: s0123456 moves: RRRRRRUUUUUULLLDLU

#s = sokoban.World("s0596553")
# using seed: s0596553 moves: DDDDDDDDRRRRRRRRRRDRUUU

#s = sokoban.World("s0596553a")
# using seed: s0596553a moves: RRDLLLLLLLLLLLLLDLUUUU

#s = sokoban.World("s0596553b")
# using seed: s0596553b moves: RRRRRRRRRRRRRRRRDDDDDLLLLLLULDDDD

#s = sokoban.World("s0596553c")
# using seed: s0596553c moves: LLDDDRRRRRRRDRUUUUUUUU

#s = sokoban.World("s0596553d")
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
def x_distance(source: sokoban.Cell=s.box, target: sokoban.Cell=s.target) ->int:
    if source.x - target.x > 0: return LEFT
    if source.x - target.x == 0: return HIT
    if source.x - target.x < 0: return RIGHT

def y_distance(source: sokoban.Cell=s.box, target: sokoban.Cell=s.target) ->int:
    if source.y - target.y > 0: return ABOVE
    if source.y - target.y == 0: return HIT
    if source.y - target.y < 0: return BELOW

# Überprüfen, ob Spiel überhaupt gewonnen werden kann.
def unwinnable() ->bool:
    # Box ist am unteren Rand, Ziel ist jedoch oberhalb Box
    if y_distance() == ABOVE and s.box.y == s.SIZE-1: return True
    # Box ist am oberen Rand, Ziel ist jedoch unterhalb Box
    if y_distance() == BELOW and s.box.y == 0: return True
    # Box ist am rechten Rand, Ziel ist jedoch links von Box
    if x_distance() == LEFT and s.box.x == s.SIZE-1: return True
    # Box ist am linken Rand, Ziel ist jedoch rechts von Box
    if x_distance() == RIGHT and s.box.x == 0: return True
    return False

## Einmaliger Aufruf:
# Prüfen, ob Welt unlösbar ist
if unwinnable():
    print("Spiel kann nicht gewonnen werden!")
    font = pygame.font.SysFont(None, 100)
    text = font.render("Unlösbar!", True, sokoban.WHITE)
    s.screen.blit(text, (
    s.screen.get_width() // 2 - text.get_width() // 2, s.screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    exit(0)

# Spieler ausrücken, wenn auf einer Spalte mit Box
if x_distance(s.me, s.box) == HIT:
    if s.me.x > 0:
        s.left()
    else:
        s.right()

# Spieler ausrücken, wenn in einer Zeile mit Box
if y_distance(s.me, s.box) == HIT:
    if s.me.y > 0:
        s.up()
    else:
        s.down()

## Schleife, bis Spiel gewonnen ist:
while not s.winning():

    # Aufholen L/R
    while True:
        # Ziel ist links von Box
        if x_distance() == LEFT:
            # Spieler nach links bewegen, wenn Box weiter links von Spieler
            if s.me.x - s.box.x > LEFT: s.left()
            # Spieler nach rechts bewege, wenn Box weniger links (also rechts) von Spieler
            if s.me.x - s.box.x < LEFT: s.right()
            # Spieler nicht mehr bewegen, wenn Box genau links neben Spieler
            if s.me.x - s.box.x == LEFT: break
        # Ziel ist rechts von Box
        if x_distance() == RIGHT:
            # Spieler nach links bewegen, wenn Box weiter links von Spieler
            if s.me.x - s.box.x > RIGHT: s.left()
            # Spieler nach rechts bewegen, wenn Box weniger links (also rechts) von Spieler
            if s.me.x - s.box.x < RIGHT: s.right()
            # Spieler nicht mehr bewegen, wenn Box genau rechts neben Spieler
            if s.me.x - s.box.x == RIGHT: break
        # Ziel ist über oder unter Box
        if x_distance() == HIT: break

    # Aufholen U/D
    while True:
        # Wenn Spieler unterhalb Box
        if s.me.y - s.box.y > HIT: s.up()
        # Wenn Spieler oberhalb Box
        if s.me.y - s.box.y < HIT: s.down()
        # Spieler anhalten, wenn auf gleicher Höhe mit Box
        if s.me.y - s.box.y == HIT: break

    # Schub der Box L/R
    while True:
        # Wenn Box rechts von Ziel
        if s.box.x - s.target.x > HIT: s.left()
        # Wenn Box links von Ziel
        if s.box.x - s.target.x < HIT: s.right()
        # Wenn Box ober- oder unterhalb von Ziel
        if s.box.x - s.target.x == HIT: break

    # Um die Ecke laufen:
    # Spieler nach unten bewegen, wenn Ziel oberhalb Box
    if y_distance() == ABOVE: s.down()
    # Spieler nach oben bewegen, wenn Ziel unterhalb Box
    if y_distance() == BELOW: s.up()
    # Spieler nach links bewegen, wenn Box links von Spieler
    if x_distance(s.me,s.box) == LEFT: s.left()
    # Spieler nach rechts bewegen, wenn Box rechts von Spieler
    if x_distance(s.me,s.box) == RIGHT: s.right()

    # Zur Box aufholen L/R (falls nötig)
    while True:
        # Wenn Spieler rechts von Box
        if s.me.x - s.box.x > HIT: s.left()
        # Wenn Spieler links von Box
        if s.me.x - s.box.x < HIT: s.right()
        if s.me.x - s.box.x == HIT: break

    # Schub der Box U/D
    while True:
        # Wenn Ziel oberhalb von Box, Spieler nach oben bewegen
        if y_distance(s.box, s.target) == ABOVE: s.up()
        # Wenn Ziel unterhalb von Box, Spieler nach unten bewegen
        if y_distance(s.box, s.target) == BELOW: s.down()
        # Wenn Box auf Höhe von Ziel, Spieler stoppen
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