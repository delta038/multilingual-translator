import flet as ft
from utils import log
from models import TranslatedState, Languages
from components.prompt_form import PromptForm
from components.language_selection import LanguagesSelectionView
from components.translated_view import TranslatedView

@ft.component
def AppView() -> list[ft.Control]:
    translated, _ = ft.use_state(TranslatedState())
    languages, _ = ft.use_state(Languages())
    log(f'[AppView] rendered. translated={translated.translated} languages={languages.value}')

    return [
            ft.Column(
                [
                    ft.Row([
                        PromptForm(translated.translate_async, languages),
                        LanguagesSelectionView(languages),
                        ]),
                    TranslatedView(translated),
                    ],
                scroll=ft.ScrollMode.ADAPTIVE,
                margin=10
                )
        ]

if __name__ == '__main__':
    ft.run(lambda page: page.render(AppView))
