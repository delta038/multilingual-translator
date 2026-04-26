import flet as ft
from utils import log
from models import TranslatedState, Languages
from components.prompt_form import PromptForm
from components.language_selection import LanguagesSelectionView
from components.translated_view import TranslatedView
from utils import provide
from contexts import LanguagesContext
from models import Languages

@ft.component
def AppView() -> ft.Control:
    translated, _ = ft.use_state(TranslatedState())
    languages, _ = ft.use_state(Languages())
    log(f'[AppView] rendered. translated={translated.translated} languages={languages.value}')

    return ft.Container(
            content=ft.Row([
                ft.Column(
                    [
                        ft.Row([
                            PromptForm(translated.translate_async, languages),
                            LanguagesSelectionView(languages),
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

async def main(page: ft.Page):
    # localStorageから値を取得


    # page.renderを使用して、ルートコンポーネントとして描画する
    page.render(lambda: provide([
        (LanguagesContext, Languages())
        ], AppView))

if __name__ == '__main__':
    ft.run(main)
