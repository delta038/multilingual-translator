import flet as ft
import googletrans
import asyncio
from typing import Callable
from contexts import LanguagesContext
from utils import log
from models import Languages

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
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="言語を削除",
                    on_click=lambda e: delete()
                )
                ]
            )

@ft.component
def LanguagesSelectionView() -> ft.Control:
    """
    言語設定ボタンとダイアログを管理するコンポーネント。
    
    FletのAlertDialogは、条件分岐(if)でコンポーネント自体を生成・破棄するよりも、
    常にコントロールツリーに配置しておき `open` プロパティで表示・非表示を切り替える構成にすることで、
    イベントハンドラ（on_click, on_dismiss）の動作と状態管理が安定します。
    """
    log(f'[LanguagesSelectionView] rendered.')
    
    is_open_popup, set_is_open_popup = ft.use_state(False)
    lang_id, set_lang_id = ft.use_state('')

    is_first = ft.use_ref(True)

    languages: Languages = ft.use_context(LanguagesContext)

    def save():
        if is_first.current:
            is_first.current = False
            return
        log(f'[LanguagesSelectionView][save] called. languages={languages.value}')
        async def save_async():
            await ft.SharedPreferences().set('languages', list(languages.value))

        task = asyncio.create_task(save_async())
        return lambda: task.cancel()

    ft.use_effect(save, [languages.value])

    def show_popup(e):
        log(f'[LanguagesSelectionView][show_popup] called.')
        set_is_open_popup(True)

    def close_popup(e=None):
        log(f'[LanguagesSelectionView][close_popup] called.')
        set_is_open_popup(False)

    def add():
        log(f'[LanguagesSelectionView][add] called. {lang_id=}')
        if lang_id:
            languages.append(lang_id)

    # 設定ボタンとダイアログをセットで返し、ダイアログは open プロパティで制御する
    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                tooltip="翻訳言語の設定",
                on_click=show_popup
            ),
            ft.AlertDialog(
                title=ft.Text('言語選択'),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text('設定済みの言語:'),
                                ],
                            margin=ft.margin.only(top=20),
                            ),
                        ft.Column(
                            [
                                LanguagesSelectionForm(lang, languages.delete) for lang in languages.value
                                ]
                            ),
                        ft.Row(
                            [
                                ft.Text('言語を追加:'),
                                ],
                            margin=ft.Margin.only(top=20),
                            ),                        
                        ft.Row(
                            [
                                ft.Dropdown(
                                    width=220,
                                    value=lang_id,
                                    options=[ft.DropdownOption(key=k, text=v) for k, v in googletrans.LANGUAGES.items()],
                                    on_select=lambda e: set_lang_id(str(e.data)),
                                    ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    tooltip="言語を追加",
                                    on_click=lambda e: add()
                                )
                                ]
                            ),
                     ],
                    tight=True,
                    ),
                actions=[
                    ft.TextButton('閉じる', on_click=close_popup)
                    ],
                open=is_open_popup,
                on_dismiss=close_popup,
                )
        ]
    )
