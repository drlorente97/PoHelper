# PoHelper (PoHelper Telegram bot powered by Python)
# Copyright (C) 2022  drlorente97.eth <drlorente97@gmail.com>

# General Declarations
import curses

def set_colors():
    """
    Define all colors used on pytelebot
    """
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_BLACK)
    curses.init_pair(5,curses.COLOR_WHITE,curses.COLOR_RED)
    curses.init_pair(6,curses.COLOR_BLACK,curses.COLOR_WHITE)

def terminate():
    """
    Returns terminal to original pre-curses state
    """
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

class window():
    def __init__(self, h=0, w=0, y=0, x=0):
        """
        Main window object, this is the parent
        if h or w is < 1
            it perform an correction based on percent of the screen

        Example:
            window(0.3, 0.2, 5, 5)
            it create a widnow on x=5 and y=5
            the width of window is 20% of the value of curses.COLS
            the heigh is 50% of the value of curses.LINES
        """
        curses.curs_set(0)
        ww = curses.COLS
        hh = curses.LINES
        set_colors()
        if not w < 1 and not h < 1:
            self.x = int(x)
            self.y = int(y)
            self.w = int(w)
            self.h = int(h)
        else:
            self.x = int(x * ww)
            self.y = int(y * hh)
            self.w = int(y * ww)
            self.h = int(x * hh)
        self.screen_buffer = []
        self.bookmark = 0

    def create_window(self):
        """
        Create new window object
        """
        self.winObject = curses.newwin(self.h, self.w, self.y, self.x)

    def build(self):
        """
        Draw the created window
        """
        self.create_window()
        self.refresh()

    def border(self):
        """
        Add borders to window
        """
        self.winObject.border()
        self.refresh()

    def refresh(self):
        """
        Macro for window refresh
        """
        self.winObject.refresh()

    def scroll_on(self):
        """
        Enable window for scroll
        """
        self.winObject.scrollok(True)
        self.winObject.idlok(True)

    def scroll_off(self):
        """
        Disable window for scroll
        """
        self.winObject.scrollok(False)
        self.winObject.idlok(False)

    def reset_cursor(self):
        """
        Move the cursor to the first character
        """
        self.write("", x=0, y=0)

    def clean(self):
        """
        Clean all the window except the border
        """
        for i in range(self.h - 1):
            self.write(" " * (self.w-2), x=i, y=0)
        self.reset_cursor()

    def destroy(self):
        """
        Destroy/Delete the window
        """
        self.create_window()
        self.refresh()

    def write(self, text, color=4, y=None, x=None):
        """
        Macro for Write & Refresh
        """
        if x == None or y == None:
            self.winObject.addstr(text, curses.color_pair(color))
        else:
            self.winObject.addstr(y, x, text, curses.color_pair(color))

    def read(self):
        """
        Macro for read a character from input
        """
        key = self.winObject.getch()
        return key

    def write_buffer(self):
        """
        Write All the buffer to window
        """
        self.clean()
        count = 1
        for x in range(self.bookmark - 1,len(self.screen_buffer) - bookmark):
            self.write(self.screen_buffer[x - 1], x=count, y=1)
            count += 1
        self.refresh()

    def screen_buffer_add(self, string):
        """
        add newlines to screen buffer
        """
        self.screen_buffer.append(string)
        if len(self.screen_buffer) > (self.h - 2) :
            self.bookmark = self.screen_buffer - (self.h - 2)
        self.write_buffer()


class intro(window):
    def __init__(self, h=4, w=80, x=0, y=0):
        """
        Exclusive Intro Window
        """
        super().__init__(h, w, x, y)


class log(window):
    def __init__(self, h=15, w=80, x=5, y=0):
        """
        Exclusive Logger Window
        """
        super().__init__(h, w, x, y)

class logbox(log):
    def __init__(self, h=13, w=77, x=6, y=2):
        """
        Draw Log Box
        """
        self.draw_log_window()
        self.maxlines = (h - 1)
        super().__init__(h, w, x, y)

    def draw_log_window(self):
        """
        Draw Log Window
        """
        logWindow = log()
        logWindow.build()
        logWindow.border()
        logWindow.write('[Log box]',y=0,x=35)
        logWindow.write('[UP ARROW: Scroll up log]──[DOWN ARROW: Scroll down log]',y=14,x=12)
        logWindow.refresh()
