import flet as ft

from components.prompt_form import PromptForm
from components.translated_view import TranslatedView
from models import TranslatedState

@ft.component
def TranslationView() -> ft.Control:
    translated, _ = ft.use_state(TranslatedState())
    
    return ft.Container(
            content=ft.Row([
                ft.Column([
                    PromptForm(translated.translate_async),
                    TranslatedView(translated)
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    margin=10,
                          expand=True
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True),
            expand=True
            )
