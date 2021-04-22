import curses
import time

start_time = 0
wait_space_start = 0
wait_space = 2.5

solving = False

solves = []

def updateSolves(scr):
    scr.clear()
    lowest = float('inf')
    highest = 0

    lines = []
    solves_checked = []

    for index, solve in enumerate(solves):
        if index >= curses.LINES:
            break

        solve = round(solve, 4)

        if highest < solve:
            highest = solve

        if lowest > solve:
            lowest = solve
        
        solves_checked.append(solve)

    for index, solve in enumerate(solves_checked):
        line = f"{solve}s"

        try:
            if solves_checked[index + 1] > solve:
                line += f" -{round(solves_checked[index + 1] - solve, 2)}"

            elif solves_checked[index + 1] < solve:
                line += f" +{round(solve - solves_checked[index + 1], 2)}"

        except IndexError:
            pass

        if solve == highest:
            line += " Worst"

        if solve == lowest:
            line += " Best"

        lines.append(line)

    for index, line in enumerate(lines):
        scr.addstr(index, 0, line)

def main(scr):
    # Clear screen
    scr.clear()

    text = "0s"
    solving = False
    scr.nodelay(1)

    while True:
        scr.refresh()

        key = None

        try:
            key = scr.getkey()
        except Exception as e:
            time.sleep(1/60)

        if solving:
            text = f"{round(time.time() - start_time, 2)}s"

        scr.addstr(curses.LINES // 2, curses.COLS // 2 - len(text) // 2, text)
        guide = "Press space to start the timer"
        scr.addstr((curses.LINES // 2) + 5, curses.COLS // 2 - len(guide) // 2, guide)

        if key == ' ':
            if solving:
                # Rubik's cube finished!
                solving = False
                solve_time = time.time() - start_time
                solves.insert(0, solve_time)

                updateSolves(scr)

            else:
                # Start solving
                solving = True
                start_time = time.time()

curses.wrapper(main)
