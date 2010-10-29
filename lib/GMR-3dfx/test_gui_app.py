import engine

import event, gui

class main(object):
    def __init__(self):
        self.display = engine.display.Display()
        self.display.setup(screen_size=(640,480))
        self.display.build()
        self.display.clear()

        self.display.set_2d()
        self.display.set_lighting(False)

        self.event_handler = event.Handler()

        self.app = gui.App(self.event_handler)
        self.app.load_theme('gui_app_theme.txt')

        self._file = gui.DropDownMenu(self.app, (0,0), 'file',
                             (['save', True],
                              ['quit', False]))
        self._file.dispatch.bind('select', self.handle_file_select)

        self._help = gui.DropDownMenu(self.app, gui.RelativePos(to=self._file, x="right", y="top"),
                              'help', (['about', False],))
        self._help.dispatch.bind('select', self.handle_file_select)

        self._about = gui.Container(self.app, (150,150), (300,200))
        self._about.theme.set_val('visible', False)
        self._about.theme.set_val('always_active', True)
        gui.Label(self._about, (5,5), "Test application for GMR-gui\nSecond Line")
        b = gui.Button(self._about, gui.RelativePos(x="center", y="bottom", pady=25), "close")
        b.dispatch.bind('click', lambda: self._about.theme.set_val('visible', False))

        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.update()
        self.display.destroy()

    def update(self):
        self.event_handler.update()

        if self.event_handler.quit:
            self.running = False

        self.display.clear()
        self.app.render()
        self.display.refresh()

    def handle_file_select(self, item):
        if item.text == 'quit':
            self.running = False
        elif item.text == 'about':
            self._about.theme.set_val('visible', not self._about.theme.get_val('visible'))

main()
