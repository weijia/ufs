


class CrossGuiLauncher:
    def __init__(self, gui_factory):
        self.gui_factory = gui_factory
        self.taskbar_icon = self.gui_factory.create_taskbar_icon()
        self.taskbar_icon["Exit"] = self.exit_clicked
        
    def exit_clicked(self):
        pass