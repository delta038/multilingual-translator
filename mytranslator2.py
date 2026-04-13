import flet as ft
from googletrans import Translator
import googletrans
import asyncio
from dataclasses import dataclass, field
from collections.abc import Callable

DEBUG = True

def log(message: str):
    if DEBUG:
        print(message)

@ft.component
def PromptForm(translate_async) -> ft.Control:
    prompt, set_prompt = ft.use_state('')
    is_progressing, set_is_progressing = ft.use_state(False)

    def update(new_prompt):
        set_prompt(new_prompt)
        log(f'{new_prompt=}')

    async def execute_async(e):
        log(f'[execute_async] called. {prompt=}')
        
        set_is_progressing(True)
        await translate_async(prompt)
        set_is_progressing(False)

    if is_progressing:
        return ft.Row(
                controls=[
                    ft.TextField(label='日本語を入力', value=prompt, on_change=lambda e: update(e.control.value), read_only=True),
                    ft.ProgressRing()
                    ]
                )

    return ft.Row(
            controls=[
                ft.TextField(label='日本語を入力', value=prompt, on_change=lambda e: update(e.control.value)),
                ft.Button('翻訳', on_click=execute_async)
                ]
            )

@ft.observable
@dataclass
class TranslatedState:
    translated: dict = field(default_factory=dict)

    async def translate_async(self, prompt: str):
        log(f'[TranslatedState][translated_async] called. {prompt=}')
        if not isinstance(prompt, str):
            ValueError('Invalid argument type.')

        translator = Translator()
        tasks = [self._translate_async(translator, prompt, lang) for lang in ['en', 'de', 'fr']]
        results = await asyncio.gather(*tasks)

        log(f'[TranslatedState][translated_async] {results=}')
        self.translated = {
                'en': results[0],
                'de': results[1],
                'fr': results[2]
                }

    async def _translate_async(self, translator, prompt, lang) -> str:
        # 個別の翻訳タスク
        try:
            result = await translator.translate(prompt, dest=lang)
            return result.text
        except:
            return ''

@ft.observable
@dataclass
class Languages:
    value: set = field(default_factory=set)

    def append(self, target: str):
        log(f'[Languages][append] called. {target=}')
        # self.value.addだと変更通知がUIに届かないので、丸ごと変更する
        copied = self.value.copy()
        copied.add(target)
        self.value = copied.copy()
        # self.value.add(target)
        log(f'[Languages][append] current languages {self.value}')

    def delete(self, target: str):
        log(f'[Languages][delete] called. {target=}')
        # self.value.discardだと変更通知がUIに届かないので、丸ごと変更する
        copied = self.value.copy()
        copied.discard(target)
        self.value = copied.copy()
        # self.value.discard(target)
        log(f'[Languages][delete] current languages {self.value}')

@ft.component
def LanguagesSelectionForm(lang: str, delete_from_store: Callable[[str], None]) -> ft.Control:
    log(f'[LanguagesSelectionForm] rendered.')

    def delete():
        log(f'[LanguagesSelectionForm][delete] called.')
        delete_from_store(lang)

    return ft.Row(
                [
                ft.Dropdown(
                    width=220,
                    value=lang,
                    options=[ft.DropdownOption(key=k, text=v) for k, v in googletrans.LANGUAGES.items()]
                ),
                ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e: delete())
                ]
            )

@ft.component
def LanguagesSelectionView(languages: Languages) -> ft.Control:
    log(f'[LanguagesSelectionView] rendered.')
    
    is_open_popup, set_is_open_popup = ft.use_state(False)
    lang_id, set_lang_id = ft.use_state('')

    def show_popup():
        log(f'[LanguagesSelectionView][show_popup] called.')
        set_is_open_popup(True)

    def close_popup():
        log(f'[LanguagesSelectionView][close_popup] called.')
        set_is_open_popup(False)

    def add():
        log(f'[LanguagesSelectionView][add] called. {lang_id=}')
        languages.append(lang_id)

    if is_open_popup:
        return ft.AlertDialog(
                title=ft.Text('言語選択'),
                content=ft.Column(
                    [
                        ft.Column(
                            [LanguagesSelectionForm(lang, languages.delete) for lang in languages.value]),
                        
                        ft.Row(
                            [
                                ft.Dropdown(
                                    value=lang_id,
                                    options=[ft.DropdownOption(key=k, text=v) for k, v in googletrans.LANGUAGES.items()],
                                    on_select=lambda e: set_lang_id(str(e.data)),
                                    ),
                                ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e: add())
                                ]
                            )
                     ]
                    ),
                open=True,
                on_dismiss=lambda e: close_popup(),
                )

    return ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e: show_popup())


@ft.component
def TranslatedView(state: TranslatedState) -> ft.Control:
    log(f'[TranslatedView] rendered. translated={state.translated}')
    return ft.Column(
            controls=[ft.Text(f'[{k}] {v}') for k, v in state.translated.items()]
            )

@ft.component
def AppView() -> list[ft.Control]:
    translated, _ = ft.use_state(TranslatedState())
    languages, _ = ft.use_state(Languages())
    log(f'[AppView] rendered. translated={translated.translated}')

    return [
            PromptForm(translated.translate_async),
            TranslatedView(translated),
            ft.Dropdown(
                width=220,
                options=[ft.DropdownOption(key=k, text=v) for k, v in googletrans.LANGUAGES.items()]
                ),
            LanguagesSelectionView(languages)
            ]

ft.run(lambda page: page.render(AppView))
