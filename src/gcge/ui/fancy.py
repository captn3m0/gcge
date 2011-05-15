import curses
import curses.wrapper
from curses.textpad import rectangle
import time

class UI:
    def __init__(self, engine, numPlayers):
        self.engine = engine
        self.numPlayers = numPlayers

    def start(self):
        curses.wrapper(self.run)

    def run(self, stdscr):
        self.stdscr = stdscr
        self.statscr = curses.newwin(20,80,0,0)
        self.optscr = curses.newwin(4,80,20,0)
        self.statscr.border(0)
        self.statscr.refresh()
        self.optscr.border(0)
        self.optscr.refresh()
        eng = self.engine
        while not eng.ended:
            self.statscr.refresh()
            eng.step()
            time.sleep(1)

    def status(self, status):
        self.statscr.move(1,1)
        self.statscr.insertln()
        self.statscr.addstr(1,1,status)
        self.statscr.border(0)
        self.statscr.refresh()

    def prompt(self, options):
        self.optscr.addstr(1,1,"Choose: " + 
            ", ".join(list(options.keys())) + "? ")
        self.optscr.refresh()
        choice = self.getInput()
        if choice in options:
            options[choice]()
        else:
            self.status("Bad option")

    def getInput(self):
        self.optscr.move(2,1)
        curses.curs_set(1)
        curses.echo()
        result = ''
        while True:
            ch = self.optscr.getch()
            if ch == ord('\n'):
                break
            result += chr(ch)
            self.optscr.refresh()
        curses.noecho()
        curses.curs_set(0)
        self.optscr.clear()
        self.optscr.border(0)
        self.optscr.refresh()
        return result
