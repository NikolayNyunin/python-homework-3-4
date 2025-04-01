from src.links.utils import validate_short_code, is_free, generate_short_code
from src.links.models import Link

import pytest


def test_validate_short_code():
    """Тестирование функции `validate_short_code`."""

    # Слишком короткие коды
    assert validate_short_code('') is False
    assert validate_short_code('Ab') is False

    # Коды валидной длины
    assert validate_short_code('Tst') is True
    assert validate_short_code('MAXLENGTH1') is True

    # Слишком длинный код
    assert validate_short_code('MAXLENGTH12') is False

    # Коды с недопустимыми символами
    assert validate_short_code('ТестКод') is False
    assert validate_short_code('Test_01') is False
    assert validate_short_code('@#$%') is False

    # Валидные коды
    assert validate_short_code('ggl') is True
    assert validate_short_code('Google') is True
    assert validate_short_code('Yandex') is True


@pytest.mark.asyncio
async def test_is_free(mocker):
    """Тестирование функции `is_free`."""

    # Мок сессии взаимодействия с БД
    mock_result = mocker.MagicMock()
    mock_session = mocker.AsyncMock()
    mock_session.execute.return_value = mock_result

    # Тестовые сценарии
    test_cases = (
        (None, 'free_code', True),                   # Код свободен
        (Link(short_code='taken'), 'taken', False),  # Код занят
        (None, 'shorten', False),                    # Код принимает системно занятое значение
        (None, 'search', False),                     # Код принимает системно занятое значение
        (None, 'user', False)                        # Код принимает системно занятое значение
    )

    # Проверка сценариев
    for db_return, code, expected in test_cases:
        mock_result.scalar_one_or_none.return_value = db_return
        assert await is_free(code, mock_session) == expected


@pytest.mark.asyncio
async def test_generate_short_code(mocker):
    """Тестирование функции `generate_short_code`."""

    # Мок сессии взаимодействия с БД
    mock_result = mocker.MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session = mocker.AsyncMock()
    mock_session.execute.return_value = mock_result

    # Проверка длины кода
    assert len(await generate_short_code(mock_session)) == 8

    # Проверка доступности кода
    assert await is_free(await generate_short_code(mock_session), mock_session) == True

    # # Проверка случая бесконечной генерации занятых кодов
    # mock_result.scalar_one_or_none.return_value = Link()
    # assert run_with_timeout_async(generate_short_code, session=mock_session) is False
