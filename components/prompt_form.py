import flet as ft
import asyncio
from typing import Callable, Coroutine
from utils import log
from models import Languages

@ft.component
def PromptForm(translate_async: Callable[[str, set[str]], Coroutine], languages: Languages) -> ft.Control:
    prompt, set_prompt = ft.use_state('')
    is_progressing, set_is_progressing = ft.use_state(False)

    def retrieve():
        async def retrieve_async():
            log('[PromptForm][retrieve] called.')
            if not await ft.SharedPreferences().contains_key('languages'):
                return

            lang_ids = await ft.SharedPreferences().get('languages')
            for lang_id in lang_ids:
                languages.append(lang_id)

        task = asyncio.create_task(retrieve_async())
        return lambda: task.cancel()

    ft.use_effect(retrieve, [])

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
                ft.TextField(label='日本語を入力', value=prompt, on_change=lambda e: update(e.control.value)),
                ft.Button('翻訳', on_click=execute_async)
                ]
            )
