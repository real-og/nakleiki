import asyncio
import logging
from typing import Any, Awaitable, Callable

from aiogram import types
from aiogram.utils.exceptions import (
    InvalidQueryID,
    MessageNotModified,
    NetworkError,
    RetryAfter,
    TelegramAPIError,
)


logger = logging.getLogger(__name__)

TELEGRAM_ATTEMPTS = 3
TELEGRAM_RETRY_DELAY = 1.0


def _is_retryable_telegram_api_error(exception: TelegramAPIError) -> bool:
    """Retry only temporary Telegram 5xx-like errors, not ordinary 4xx mistakes."""
    message = str(exception).lower()
    return any(
        marker in message
        for marker in (
            "bad gateway",
            "gateway timeout",
            "temporarily unavailable",
            "internal server error",
        )
    )


async def _telegram_call_with_retry(
    operation: Callable[..., Awaitable[Any]],
    *args,
    attempts: int = TELEGRAM_ATTEMPTS,
    **kwargs,
):
    """
    Execute one atomic Telegram API call with a small retry window.

    We retry only temporary transport/server errors. Non-temporary Telegram API
    errors are raised immediately so programming/data problems are not hidden.
    """
    last_exception = None

    for attempt in range(1, attempts + 1):
        try:
            return await operation(*args, **kwargs)

        except RetryAfter as exception:
            last_exception = exception
            if attempt == attempts:
                raise

            timeout = max(float(exception.timeout), TELEGRAM_RETRY_DELAY)
            logger.warning(
                "Telegram RetryAfter on attempt %s/%s; sleeping %.1fs",
                attempt,
                attempts,
                timeout,
            )
            await asyncio.sleep(timeout)

        except (NetworkError, asyncio.TimeoutError) as exception:
            last_exception = exception
            if attempt == attempts:
                raise

            logger.warning(
                "Temporary Telegram network error on attempt %s/%s: %r",
                attempt,
                attempts,
                exception,
            )
            await asyncio.sleep(TELEGRAM_RETRY_DELAY * attempt)

        except TelegramAPIError as exception:
            if not _is_retryable_telegram_api_error(exception):
                raise

            last_exception = exception
            if attempt == attempts:
                raise

            logger.warning(
                "Temporary Telegram API error on attempt %s/%s: %r",
                attempt,
                attempts,
                exception,
            )
            await asyncio.sleep(TELEGRAM_RETRY_DELAY * attempt)

    if last_exception is not None:
        raise last_exception


def safe_answer(message: types.Message, text: str, **kwargs):
    return _telegram_call_with_retry(message.answer, text, **kwargs)


def safe_bot_send_message(bot, chat_id, text: str, **kwargs):
    return _telegram_call_with_retry(bot.send_message, chat_id, text, **kwargs)


async def safe_callback_answer(callback: types.CallbackQuery, *args, **kwargs):
    try:
        return await _telegram_call_with_retry(callback.answer, *args, **kwargs)
    except InvalidQueryID as exception:
        # A callback may become too old while the handler is doing useful work.
        # Failing to ACK such an old callback should not undo/abort that work.
        logger.warning("Callback query is already too old to answer: %r", exception)
        return None


async def safe_edit_reply_markup(message: types.Message, **kwargs):
    try:
        return await _telegram_call_with_retry(message.edit_reply_markup, **kwargs)
    except MessageNotModified:
        # The desired keyboard state is already applied; nothing else is needed.
        return None


async def notify_user_about_error(update: types.Update):
    """Best-effort notification used by the global aiogram error handler."""
    message = None

    if update.message:
        message = update.message
    elif update.callback_query and update.callback_query.message:
        message = update.callback_query.message

    if message is None:
        return

    try:
        await safe_answer(
            message,
            "Произошла временная ошибка. Пожалуйста, повторите попытку. "
            "Если ошибка повторяется — нажмите /start.",
        )
    except Exception as exception:
        # Telegram itself can be unavailable, so even the error notification
        # must never create a second unhandled exception.
        logger.error(
            "Could not notify user about handler error: %r",
            exception,
            exc_info=(type(exception), exception, exception.__traceback__),
        )
