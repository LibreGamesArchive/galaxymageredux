from lib import engine, event, gui
import random

from lib.gui import theme

def print_val(val):
    if not val.disabled:
        print val.text

def main():
    test = engine.display.Display()
    test.setup(screen_size=(640,480))
    test.build()
    test.clear()

    test.set_2d()
    test.set_lighting(False)

    event_handler = event.Handler()
    main_app = gui.App(event_handler)
    main_app.load_theme('gui_theme.txt')

    some_cont = gui.Container(main_app, (100,150), (300,200))

    gui.Icon(main_app, (0,0), 'archer')
    gui.Icon(main_app, (75,0), 'base')
    gui.Label(some_cont, (5, 5), "Hello Hello?")
    gui.Label(main_app, (0, 75), "Hello Hello?")

    drop = gui.DropDown(main_app, (150, 5), "press me!")
    drop.setChild(gui.Label(main_app, (0,0), 'woah!'))

    inp = gui.Input(main_app, (55,155))
    inp.theme.set_val('width', 290)

    l = gui.List(some_cont, gui.RelativePos(x="right", y="top"), ['test1', 'test2', 'test3'])
    l.theme.get_element('Entry').set_val('font', (None, 50, (0,.5,.5,1)))
    l.update_child_theme()

    menu = gui.Menu(main_app, gui.RelativePos(), ['abc', '123', ('come on now!', True)])
    menu.dispatch.bind('select', print_val)

    menu2 = gui.DropDownMenu(main_app, gui.RelativePos(x="right", y="top", to=menu),
                             'clickme!', ['abc', '123', 'come on now!'])
    menu2.theme.get_element('Menu').get_element('Entry').set_val('background',
                                    ['solid', 'color', [0,0,0,1]])
    menu2.update_child_theme()

    butt = gui.Button(some_cont, gui.RelativePos(), "test\nclick")
    text_box = gui.MessageBox(main_app, (50, 375), (300,100))
    butt.dispatch.bind('click',
                       lambda: text_box.add_line(
                           'test'+str(random.randint(0,45))))

    popup = gui.PopUp(butt, text="adds text to the message box below")

    while 1:
        event_handler.update()

        if event_handler.quit:
            test.destroy()
            return None

        test.clear()
        main_app.render()
        test.refresh()

main()
