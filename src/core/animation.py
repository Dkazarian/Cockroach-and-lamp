class Animation:
    FRAME_DURATION = 2

    def __init__(self, item, images, auto=True):
        self.images = images
        self.item = item
        self.animation_step = 0
        self.animation_time = 0
        self.paused = True
        self.manual = not auto

    def setup(self):
        self.item.set_image(self.images[self.animation_step])

    def clear(self):
        self.pause()

    def update(self):
        if not(self.paused or self.manual):
            self.update_frame()
       
    def update_frame(self):
        if len(self.images) == 1:
            return

        self.animation_time = (self.animation_time + 1) % Animation.FRAME_DURATION
        if self.animation_time is 0:
            self.animation_step = (self.animation_step + 1) % len(self.images)
            position = self.item.get_position()
            self.item.set_image(self.images[self.animation_step])
            self.item.set_position(position)

    def pause(self):
        self.paused = True

    def play(self):
        if self.manual:
            self.update_frame()
        else:
            self.paused = False

    def set_manual(self):
        self.manual = True 

    def set_auto(self):
        self.manual = False
