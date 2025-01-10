from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class BaseGenericViewSet(GenericViewSet):
    create_serializer_class = None
    update_serializer_class = None
    list_serializer_class = None
    retrieve_serializer_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for action in ("create", "update", "list", "retrieve"):
            field_name = f"{action}_serializer_class"
            if not getattr(self, field_name, None):
                setattr(self, field_name, self.serializer_class)
            elif not self.serializer_class:
                self.serializer_class = getattr(self, field_name)

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class
        if self.action in ["update", "partial_update"]:
            return self.update_serializer_class
        if self.action == "list":
            return self.list_serializer_class
        if self.action == "retrieve":
            return self.retrieve_serializer_class
        return super().get_serializer_class()


class BaseModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    BaseGenericViewSet,
):
    """
    Base view set with all http methods
    """
