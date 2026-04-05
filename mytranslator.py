import flet as ft
from googletrans import Translator

async def main(page: ft.Page):
    translator = Translator()
    input_field = ft.TextField(label='日本語を入力')
    result_text = ft.Text()

    async def translate_click(e):
        # 非同期で翻訳を実行
        result = await translator.translate(input_field.value, dest='en')
        result_text.value = result.text
        page.update()

    page.add(
            input_field,
            ft.Button('翻訳', on_click=translate_click),
            result_text
            )

ft.app(target=main)
