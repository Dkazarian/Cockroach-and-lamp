from libs.terminal import print_colored


class Logger:
    
    LEVEL = 1
    LEVELS = {'ERROR': 1, 'WARNING': 2, 'INFO': 3, 'DEBUG': 4}

    @classmethod
    def log_error(self, message):
        self.log(message, 'ERROR', 'red')

    @classmethod
    def log_warning(self, message):
        self.log(message, 'WARNING', 'orange')

    @classmethod
    def log_info(self, message):
        self.log(message, 'INFO', 'green')

    @classmethod
    def log_debug(self, message):
        self.log(message, 'DEBUG', 'blue')
   
    @classmethod
    def log(self, message, level, color):
        if self.LEVELS[level] <= self.LEVEL:
            print_colored("["+ level + "] " + message, color)