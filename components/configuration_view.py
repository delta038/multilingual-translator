import flet as ft
from language_selection import LanguagesSelectionView

@ft.component
def ConfigurationView() -> ft.Control:
    return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text('翻訳先言語設定'),
                    LanguagesSelectionView(),
                    ],
                       expand=True)
                ],
                expand=True
                )
            )
