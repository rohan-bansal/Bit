import itertools, sys, time, threading
from lib.colorizer import colorize

# rotating spinner :D
class Spinner:

    # write the spinner text
    def __init__(self, message, color, delay=0.05):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.color = color
        self.spinner_visible = False
        sys.stdout.write(colorize(message, color))

    # cycle the spinning dial
    def write_next(self):
        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(colorize(next(self.spinner), self.color))
                self.spinner_visible = True
                sys.stdout.flush()

    # remove spinner after finished
    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')
                    sys.stdout.write('\r')
                sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self): 
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write('\r')
