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
    log(f'[AppView] rendered. translated={translated.translated}')

    return ft.Container(
            content=ft.Row([
                ft.Column(
                    [
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
