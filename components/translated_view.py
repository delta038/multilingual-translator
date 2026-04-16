import flet as ft
from utils import log
from models import TranslatedState

@ft.component
def TranslatedView(state: TranslatedState) -> ft.Control:
    log(f'[TranslatedView] rendered. translated={state.translated}')
    return ft.Column(
            controls=[ft.Text(f'[{k}] {v}') for k, v in state.translated.items()]
            )
