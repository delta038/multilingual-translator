import flet as ft
from googletrans import Translator
import asyncio
from dataclasses import dataclass, field

DEBUG = True

def log(message: str):
    if DEBUG:
        print(message)

@ft.component
def PromptForm(translate_async) -> ft.Control:
    prompt, set_prompt = ft.use_state('')

    def clear():
        set_prompt('')

    def update(new_prompt):
        set_prompt(new_prompt)
        print(new_prompt)

    async def execute_async(e):
        log(f'[execute_async] called. {prompt=}')
        # await translate_and_output_console_async(prompt)
        await translate_async(prompt)
        clear()

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

@ft.component
def TranslatedView(state: TranslatedState) -> ft.Control:
    log(f'[TranslatedView] rendered. translated={state.translated}')
    return ft.Column(
            controls=[ft.Text(v) for k, v in state.translated.items()]
            )

@ft.component
def AppView() -> list[ft.Control]:
    translated, _ = ft.use_state(TranslatedState())
    log(f'[AppView] rendered. translated={translated.translated}')

    return [
            PromptForm(translated.translate_async),
            TranslatedView(translated)
            ]

ft.run(lambda page: page.render(AppView))
