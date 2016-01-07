from core.scenario import Scenario
from core.logger import Logger
from ConfigParser import SafeConfigParser
from tank_items.lamp import Lamp
from tank_items.cockroach import Cockroach

class Tank(Scenario):

    def __init__(self):
        Scenario.__init__(self)
        self.load_settings()
        self.add(Lamp(self, self.parse_tuple('lamp')))
        self.add(Cockroach(self, self.parse_tuple('cockroach')))
    
    def load_settings(self):
        self.settings = SafeConfigParser()
        self.settings.read('../settings.ini')
        self.set_background(self.settings.get('tank', 'background'))
        self.set_limits(self.parse_tuple('tank', 'limits'))
        Logger.LEVEL = self.settings.getint('general', 'log_level')
    
        Logger.log_info("======================")
        Logger.log_info("Cockroach Controls: ")
        Logger.log_info("A LEFT, D RIGHT")
        Logger.log_info("======================")
        Logger.log_info("Use the arrows and backspace to control the lamp")
        Logger.log_info("======================")
        
    def parse_tuple(self, item_name, attr='position'):
        return tuple(map(int, self.settings.get(item_name,attr).split(",")))

