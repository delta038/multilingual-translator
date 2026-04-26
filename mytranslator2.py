from typing import Optional
import flet as ft
from utils import log
from models import TranslatedState, Languages
from components.prompt_form import PromptForm
from components.language_selection import LanguagesSelectionView
from components.translated_view import TranslatedView
from utils import provide
from contexts import LanguagesContext
from models import Languages

from enum import Enum

class TabType(Enum):
    TRANSLATE = 0
    CONFIGURATION = 1

@ft.component
def TranslationView() -> ft.Control:
    translated, _ = ft.use_state(TranslatedState())
    log(f'[MainView] rendered.')

    return ft.Container(
            content = ft.Row([
                ft.Column([
                    ft.Row([
                        PromptForm(translated.translate_async),
                        LanguagesSelectionView(),
                        ]),
                    TranslatedView(translated)
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    margin=10,
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                )
            )

@ft.component
def ConfigurationView() -> ft.Control:
    return ft.Text('Configuration View')

@ft.component
def AppView() -> ft.Control:
    translated, _ = ft.use_state(TranslatedState())
    log(f'[AppView] rendered. translated={translated.translated}')

    current_tab_type, set_current_tab_type = ft.use_state(TabType.TRANSLATE)
    
    main_content: Optional[ft.Control] = None

    if current_tab_type == TabType.TRANSLATE:
        main_content = TranslationView()
    elif current_tab_type == TabType.CONFIGURATION:
        main_content = ConfigurationView()

    return ft.Container(
            content=ft.Column([
                main_content,
                ft.BottomAppBar(
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.IconButton(ft.Icons.SEARCH, on_click=lambda e: set_current_tab_type(TabType.TRANSLATE)),
                            ft.IconButton(ft.Icons.SETTINGS, on_click=lambda e: set_current_tab_type(TabType.CONFIGURATION))
                            ]
                        )
                    )
                ],
                expand=True),
            expand=True
            )

async def generate_languages() -> Languages:
    languages = Languages()
    
    # localStorageから値を取得
    if not await ft.SharedPreferences().contains_key('languages'):
        return languages

    lang_ids = await ft.SharedPreferences().get('languages')
    for lang_id in lang_ids:
        languages.append(lang_id)

    return languages

async def main(page: ft.Page):
    # localStorageから値を取得
    languages: Languages = await generate_languages()

    # page.renderを使用して、ルートコンポーネントとして描画する
    page.render(lambda: provide([
        (LanguagesContext, languages)
        ], AppView))

if __name__ == '__main__':
    ft.run(main)
