import flet as ft
from googletrans import Translator
import asyncio
from dataclasses import dataclass, field
from utils import log

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
        log(f'[Languages][append] current languages {self.value}')

    def delete(self, target: str):
        log(f'[Languages][delete] called. {target=}')
        # self.value.discardだと変更通知がUIに届かないので、丸ごと変更する
        copied = self.value.copy()
        copied.discard(target)
        self.value = copied.copy()
        log(f'[Languages][delete] current languages {self.value}')

@ft.observable
@dataclass
class TranslatedState:
    translated: dict = field(default_factory=dict)

    async def translate_async(self, prompt: str, target_langs: set[str]):
        log(f'[TranslatedState][translated_async] called. {prompt=}, {target_langs=}')

        if not isinstance(prompt, str):
            raise ValueError(f'Invalid argument type: expected str, but {type(prompt)}')

        if not isinstance(target_langs, set):
            raise ValueError(f'Invalid argument type: expected set, but {type(target_langs)}')

        langs = list(target_langs)
        translator = Translator()
        tasks = [self._translate_async(translator, prompt, lang) for lang in langs]
        results = await asyncio.gather(*tasks)

        log(f'[TranslatedState][translate_async] {results=}')
        self.translated = {lang_id: result for lang_id, result in zip(langs, results)}
    

    async def _translate_async(self, translator, prompt, lang) -> str:
        # 個別の翻訳タスク
        try:
            result = await translator.translate(prompt, dest=lang)
            return result.text
        except Exception as e:
            log(f'Translation error: {e}')
            return ''
