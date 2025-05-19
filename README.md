# JavaLinter

- [x] Добавлен `.gitignore`. Убедитесь, что там есть `.venv` и `.idea`
- [x] Создано виртуальное окружение
- [x] Есть файл `requirements.txt` или `pyproject.toml`. Исключения: если у вас нет внешних зависимостей.
- [x] Настроены линтеры: `mypy` и `flake8`
- [x] Настроены форматтеры: `isort` и `black`
- [x] Написаны тесты
- [x] Написана документация к каждому методу, классу и функции
- [x] Написан красивый `README.md` (для форматирования можно использовать markdown), где есть информация о том, как проект установить и запустить, что он делает  и умеет, какие фунции там есть
- [x] (Для консольных утилит) написан help
- [ ] (Опционально) Есть прекоммит


Это программа, которая ищет стилистические ошибки в .java файлах

Запуск ```python main.py <Файл с описанием стиля> <Файл1.java> [Файл2.java] ...```

# Формат файла стиля

Расширение: json

```
{
  "naming": {
    "classes": NamingRule,
    "methods": NamingRule,
    "variables": NamingRule
  },
  "spaces": {
    "around_operators": bool,
    "no_around_brackets": bool,
    "after_comma": bool,
    "no_before_comma": bool,
    "may_be_more_that_one_space": bool,
    "no_before_dot_comma": bool,
    "no_around_dot": bool
  },
  "empty_lines": {
    "max_empty": int,
    "after_method": int,
    "after_class": int
  }
}
```

Где NamingRule одно из:
1. "CAMEL_CASE_CAPITAL"
2. "CAMEL_CASE_LOWER"
3. "SNAKE_CASE"

В главной папке уже лежит подходящий файл dialect_example.json