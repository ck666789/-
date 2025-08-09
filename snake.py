import curses
import random
from dataclasses import dataclass

@dataclass
class Point:
    y: int
    x: int


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]
    for i in range(box[0][0], box[1][0]):
        stdscr.addstr(i, box[0][1], "|")
        stdscr.addstr(i, box[1][1] - 1, "|")
    for i in range(box[0][1], box[1][1]):
        stdscr.addstr(box[0][0], i, "-")
        stdscr.addstr(box[1][0] - 1, i, "-")

    snake = [Point(box[0][0]+1, box[0][1]+1),
             Point(box[0][0]+1, box[0][1]+2),
             Point(box[0][0]+1, box[0][1]+3)]
    direction = curses.KEY_RIGHT

    food = Point(random.randint(box[0][0]+1, box[1][0]-2),
                 random.randint(box[0][1]+1, box[1][1]-2))
    stdscr.addch(food.y, food.x, "@")

    key_map = {curses.KEY_UP: (-1, 0),
               curses.KEY_DOWN: (1, 0),
               curses.KEY_LEFT: (0, -1),
               curses.KEY_RIGHT: (0, 1)}

    while True:
        next_key = stdscr.getch()
        if next_key in key_map:
            direction = next_key
        elif next_key == ord('q'):
            break

        dy, dx = key_map.get(direction, (0, 1))
        new_head = Point(snake[-1].y + dy, snake[-1].x + dx)

        if (new_head.y in (box[0][0], box[1][0]-1) or
                new_head.x in (box[0][1], box[1][1]-1) or
                new_head in snake):
            break

        snake.append(new_head)
        if new_head == food:
            food = Point(random.randint(box[0][0]+1, box[1][0]-2),
                         random.randint(box[0][1]+1, box[1][1]-2))
            stdscr.addch(food.y, food.x, "@")
        else:
            tail = snake.pop(0)
            stdscr.addch(tail.y, tail.x, " ")

        stdscr.addch(new_head.y, new_head.x, "#")

    stdscr.nodelay(False)
    stdscr.addstr(sh//2, sw//2 - 5, "Game Over")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
