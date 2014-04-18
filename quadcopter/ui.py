import curses
import time
import sys

def main(stdscr):

    def center(win, width, text):
        win.addstr(0, width/2-len(text)/2, text)

    curses.curs_set(0) #hide cursor


    tlwin = curses.newwin(15, 40, 0, 0)
    tlwin.border()
    center(tlwin, 40, "Top View")

    llwin = curses.newwin(15, 40, 15, 0)
    llwin.border()
    center(llwin, 40, "Rear View")

    lrwin = curses.newwin(15, 40, 15, 40)
    lrwin.border()
    center(lrwin, 40, "Side View" + curses.ACS_PI)
    lrwin.refresh()



#    stdscr.addstr(10,0, str(dir(tlwin)))
#    stdscr.refresh()

    tlwin.refresh()
    llwin.refresh()
    lrwin.refresh()


    while True:
      time.sleep(.001)

if __name__ == '__main__':
    curses.wrapper(main)
