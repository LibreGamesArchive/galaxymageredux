import engine

import event, gui

def handle_file_select(item):
    print item.text

def main():
    display = engine.display.Display()
    display.setup(screen_size=(640,480))
    display.build()
    display.clear()

    display.set_2d()
    display.set_lighting(False)

    event_handler = event.Handler()

    app = gui.App(event_handler)
    app.load_theme('gui_app_theme.txt')

    f = gui.DropDownMenu(app, (0,0), 'file',
                         (['save', True],
                          ['quit', False]))
    f.dispatch.bind('select', handle_file_select)

    while 1:
        event_handler.update()

        if event_handler.quit:
            display.destroy()
            return None

        display.clear()
        app.render()
        display.refresh()

main()
