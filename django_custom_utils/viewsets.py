from rest_framework import mixins, viewsets, status
from rest_framework.response import Response


__all__ = [
    'GenericViewSet',
    'BulkCreateModelMixin',
]


class GenericViewSet(viewsets.GenericViewSet):
    create_serializer_class = None
    update_serializer_class = None
    list_serializer_class = None
    retrieve_serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for action in ('create', 'update', 'list', 'retrieve'):
            field_name = f'{action}_serializer_class'
            if not getattr(self, field_name, None):
                setattr(self, field_name, self.serializer_class)
            elif not self.serializer_class:
                self.serializer_class = getattr(self, field_name)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        if self.action in ['update', 'partial_update']:
            return self.update_serializer_class
        if self.action == 'list':
            return self.list_serializer_class
        if self.action == 'retrieve':
            return self.retrieve_serializer_class
        return super().get_serializer_class()


class BulkCreateModelMixin(mixins.CreateModelMixin, GenericViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True, allow_empty=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
