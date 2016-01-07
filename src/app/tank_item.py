from core.item import Item


class TankItem(Item):

    def get_tank(self):
        return self.scenario

    def get_settings(self):
        return self.get_tank().settings