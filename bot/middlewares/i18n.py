from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from bot.config import Settings
from bot.utils import WORKDIR

DEFAULT_LOCALE_PATH = WORKDIR / 'common' / 'locales'

settings = Settings()


i18n = I18n(path=DEFAULT_LOCALE_PATH, default_locale=settings.DEFAULT_LOCALE, domain="messages")
simple_locale_middleware = SimpleI18nMiddleware(i18n)

gettext = i18n.gettext
lazy_gettext = i18n.lazy_gettext
