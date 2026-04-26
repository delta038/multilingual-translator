from os.path import expanduser
from typing import Optional
import asyncio
import flet as ft
from utils import log
from models import TranslatedState, Languages
from components.prompt_form import PromptForm
from components.language_selection import LanguagesSelectionView
from components.translated_view import TranslatedView
from utils import provide
from contexts import LanguagesContext
from models import Languages

from enum import Enum

class TabType(Enum):
    TRANSLATE = 0
    CONFIGURATION = 1

@ft.component
def TranslationView() -> ft.Control:
    translated, _ = ft.use_state(TranslatedState())
    log(f'[MainView] rendered.')

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
                expand=True
                ),
            expand=True
            )

@ft.component
def ConfigurationView() -> ft.Control:
    return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text('翻訳先言語設定'),
                    LanguagesSelectionView(),
                    ],
                       expand=True)
                ],
                expand=True
                ),
            expand=True
            )

@ft.component
def AppView() -> ft.Control:
    translated, _ = ft.use_state(TranslatedState())
    log(f"[AppView] rendered. translated={translated.translated}")

    current_tab_type, set_current_tab_type = ft.use_state(TabType.TRANSLATE)

    # 通知用のアニメーション状態
    show_notification, set_show_notification = ft.use_state(True)
    notification_opacity, set_notification_opacity = ft.use_state(0.0)
    notification_bottom, set_notification_bottom = ft.use_state(60)

    async def animate_notification():
        # 起動アニメーション: フェードイン + 少し上へ
        await asyncio.sleep(0.1)
        set_notification_opacity(1.0)
        set_notification_bottom(95)
        await asyncio.sleep(0.4)
        # 本来の位置へ落ち着く
        set_notification_bottom(80)

        # 10秒待機
        await asyncio.sleep(10)

        # 終了アニメーション
        await close_notification()

    async def close_notification():
        # 終了アニメーション: 一度浮き上がってから、戻りつつフェードアウト
        set_notification_bottom(95)
        await asyncio.sleep(0.3)
        set_notification_opacity(0.0)
        set_notification_bottom(80)
        await asyncio.sleep(0.3)
        set_show_notification(False)

    ft.use_effect(lambda: {asyncio.create_task(animate_notification())}, [])

    main_content: ft.Control = TranslationView()

    if current_tab_type == TabType.TRANSLATE:
        main_content = TranslationView()
    elif current_tab_type == TabType.CONFIGURATION:
        main_content = ConfigurationView()

    return ft.Container(
        content=ft.Stack(
            [
                ft.Column(
                    [
                        main_content,
                        ft.BottomAppBar(
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                controls=[
                                    ft.IconButton(
                                        ft.Icons.SEARCH,
                                        on_click=lambda e: set_current_tab_type(
                                            TabType.TRANSLATE
                                        ),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.SETTINGS,
                                        on_click=lambda e: set_current_tab_type(
                                            TabType.CONFIGURATION
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.NEW_RELEASES, color=ft.Colors.WHITE),
                                    ft.Text(
                                        "新機能：翻訳画面と設定画面をタブで分割しました(2026/4/26)",
                                        color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                                expand=True
                            ),
                            ft.IconButton(
                                ft.Icons.CLOSE,
                                icon_color=ft.Colors.WHITE,
                                on_click=lambda _: asyncio.create_task(close_notification()),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.Colors.BLUE_ACCENT_400,
                    padding=10,
                    margin=10,
                    border_radius=10,
                    bottom=notification_bottom,
                    left=10,
                    right=10,
                    opacity=notification_opacity,
                    visible=show_notification,
                    animate_opacity=300,
                    animate=ft.Animation(400, ft.AnimationCurve.DECELERATE),
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK26),
                ),
            ]
        ),
        expand=True,
    )

async def generate_languages() -> Languages:
    languages = Languages()
    
    # localStorageから値を取得
    if not await ft.SharedPreferences().contains_key('languages'):
        return languages

    lang_ids = await ft.SharedPreferences().get('languages')
    for lang_id in lang_ids:
        languages.append(lang_id)

    return languages

async def main(page: ft.Page):
    # localStorageから値を取得
    languages: Languages = await generate_languages()

    # page.renderを使用して、ルートコンポーネントとして描画する
    page.render(lambda: provide([
        (LanguagesContext, languages)
        ], AppView))

if __name__ == '__main__':
    ft.run(main)
