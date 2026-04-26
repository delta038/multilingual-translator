import flet as ft
import asyncio
from typing import Callable, Coroutine
from contexts import LanguagesContext
from utils import log
from models import Languages

@ft.component
def PromptForm(translate_async: Callable[[str, set[str]], Coroutine]) -> ft.Control:
    prompt, set_prompt = ft.use_state('')
    is_progressing, set_is_progressing = ft.use_state(False)
    languages: Languages = ft.use_context(LanguagesContext)

    def update(new_prompt):
        set_prompt(new_prompt)
        log(f'{new_prompt=}')

    async def execute_async(e):
        log(f'[execute_async] called. {prompt=}')
        
        set_is_progressing(True)
        await translate_async(prompt, languages.value)
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
                ft.TextField(label='日本語を入力', value=prompt, on_change=lambda e: update(e.control.value), on_submit=execute_async, multiline=True, shift_enter=True),
                ft.Button('翻訳', on_click=execute_async)
                ]
            )
