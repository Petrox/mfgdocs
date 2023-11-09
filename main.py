#!/usr/bin/env python3
"""Main entry point for the application.

A separate main method is run in a separate thread for every client session on the web interface.
"""

import flet as ft

from config import Config
from mfgdocsapp import MFGDocsApp


def main(page: ft.Page):
    Config.init_config()
    app = MFGDocsApp(page)
    app.main()


ft.app(target=main,
       upload_dir="uploads",
       view=ft.AppView.WEB_BROWSER,
       port=8080)
