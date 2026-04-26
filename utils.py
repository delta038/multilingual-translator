import flet as ft
from typing import Callable


DEBUG = True

def log(message: str):
    if DEBUG:
        print(message)

def provide(pairs: list[tuple], content: Callable[[], ft.Control] | ft.Control):
    """
    (Context, Value)のリストを受け取り、ネストされたプロバイダーを生成する
    """
    def wrap(index: int):
        if index == len(pairs):
            # 最後まで到達したらコンテンツを呼び出す
            return content() if callable(content) else content
        ctx, val = pairs[index]
        # 次のネストをコールバックとして渡す
        return ctx(val, lambda: wrap(index + 1))

    return wrap(0)

