import flet as ft
from googletrans import Translator
import asyncio

async def translate_async(translator, text, lang) -> str:
    # 個別の翻訳タスク
    try:
        result = await translator.translate(text, dest=lang)
        return result.text
    except:
        return ''

async def main(page: ft.Page):
    translator = Translator()
    input_field = ft.TextField(label='日本語を入力')
    result_text = ft.Text()
    result_text2 = ft.Text()
    result_text3 = ft.Text()

    async def translate_click(e):
        # 非同期で翻訳を実行
        tasks = [translate_async(translator, input_field.value, lang) for lang in ['en', 'de', 'fr']]

        results = await asyncio.gather(*tasks)

        result_text.value = results[0]
        result_text2.value = results[1]
        result_text3.value = results[2]
        page.update()

    page.add(
            ft.Row(
                controls=[
                    input_field,
                    ft.Button('翻訳', on_click=translate_click)
                    ]
                ),
            result_text,
            result_text2,
            result_text3
            )

ft.run(main)
