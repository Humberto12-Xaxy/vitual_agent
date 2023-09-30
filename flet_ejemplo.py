import flet
from flet import (
    Page,
    UserControl,
    Image
)


class TodoApp(UserControl):
    def build(self):
        return Image(src= './image/bot_escucha.gif', width= 300, height=300)
        

def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.update()

    # create application instance
    app = TodoApp()

    # add application's root control to the page
    page.add(app)


flet.app(target=main)