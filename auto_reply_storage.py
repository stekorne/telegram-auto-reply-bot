import json
from datetime import datetime
from pathlib import Path

from loguru import logger


class AutoReplyStorage:
    def __init__(self, path: str):
        self._path = Path(path)
        self._storage: dict[int, datetime] = {}

        self._load()

    def _load(self):
        if self._path.exists():
            try:
                with open(self._path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._storage = {
                        int(k): datetime.fromisoformat(v)
                        for k, v in data.items()
                    }
                logger.info(f'Загружено {len(self._storage)} записей из {self._path}')
            except Exception as e:
                logger.error(f'Ошибка загрузки из JSON: {e}')
        else:
            logger.warning('Файл хранения не найден. Будет создан при первом сохранении')

    def _save(self):
        try:
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump(
                    {str(k): v.isoformat() for k, v in self._storage.items()},
                    f, indent=2, ensure_ascii=False
                )
            logger.info(f'Состояние успешно сохранено в {self._path}')
        except Exception as e:
            logger.error(f'Ошибка при сохранении: {e}')

    def get_last_time(self, group_id: int) -> datetime | None:
        return self._storage.get(group_id)

    def update_time(self, group_id: int, when: datetime):
        self._storage[group_id] = when
        self._save()
