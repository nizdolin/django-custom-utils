from django.conf import settings
from django.http import QueryDict
from django.utils.functional import classproperty


__all__ = [
    'site_url',
    'cached_classproperty',
]


def site_url(path: str, **kwargs) -> str:
    query_string = ''
    if kwargs:
        q = QueryDict('', mutable=True)
        for k, v in kwargs.items():
            if v is not None and v != '':
                q[k] = v
        query_string = '?' + q.urlencode()
    return settings.BASE_URL + path + query_string


class cached_classproperty(classproperty):
    def get_result_field_name(self):
        return self.fget.__name__ + "_property_result" if self.fget else None

    def __get__(self, instance, cls=None):
        result_field_name = self.get_result_field_name()

        if hasattr(cls, result_field_name):
            return getattr(cls, result_field_name)

        if not cls or not result_field_name:
            return self.fget(cls)

        setattr(cls, result_field_name, self.fget(cls))
        return getattr(cls, result_field_name)
