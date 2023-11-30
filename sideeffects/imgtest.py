import flet as ft



def main(page: ft.Page):
    page.scroll = "auto"
    page.add(
        ft.Image(src="img/dot.svg", width=400, height=400)
        #ft.Image(src="img/8666681_edit_icon.svg", width=400, height=400)
    )

ft.app(target=main)

#ft.app(target=main, view=ft.AppView.WEB_BROWSER)

#ft.app(target=main)
