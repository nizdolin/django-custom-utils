import logging

from django.conf import settings
from django.http import QueryDict
from django.utils.functional import classproperty

logger = logging.getLogger(__name__)


def site_url(path: str, **kwargs) -> str:
    query_string = ""
    if kwargs:
        qd = QueryDict("", mutable=True)
        for key, value in kwargs.items():
            if value is not None and value != "":
                qd[key] = value
        query_string = f"?{qd.urlencode()}"
    return settings.BASE_URL + path + query_string


class cached_classproperty(classproperty):
    def get_result_field_name(self):
        return f"{self.fget.__name__}_property_result" if self.fget else None

    def __get__(self, instance, cls=None):  # noqa: WPS117
        result_field_name = self.get_result_field_name()

        if hasattr(cls, result_field_name):
            return getattr(cls, result_field_name)

        if not cls or not result_field_name:
            return self.fget(cls)

        setattr(cls, result_field_name, self.fget(cls))
        return getattr(cls, result_field_name)


def pluralize(value, forms, language=settings.LANGUAGE_CODE):
    """
    Selects the ending of a noun after the number
    """
    try:
        if language == settings.LANGUAGE_RU:
            one, two, many = forms.split(",")
            if value % 10 == 1 and value % 100 != 11:
                return one
            elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
                return two
            else:
                return many
        else:
            one, many = forms.split(",")
            if value == 1:
                return one
            else:
                return many

    except (ValueError, TypeError) as e:
        logger.error(
            f"Pluralize error.\nValue: {value}\nForms: {forms}\nLanguage: {language}\nError: {e}"
        )
        return ""
