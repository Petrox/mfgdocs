import flet as ft


md1="""
![Image from Flet assets](/icons/icon-192.png)
"""

md1 = """
hello

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://myoctocat.com/assets/images/base-octocat.svg)

world
"""

def main(page: ft.Page):
    page.scroll = "auto"
    page.add(
        ft.Markdown(
            md1,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data),
        )
    )

ft.app(target=main)

#ft.app(target=main, view=ft.AppView.WEB_BROWSER)

#ft.app(target=main)
