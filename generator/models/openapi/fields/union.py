import typing as t

import marshmallow
import marshmallow.error_store
import marshmallow.exceptions


class MarshmallowUnionException(Exception):
    """Base exception for marshmallow_union."""


class ExceptionGroup(MarshmallowUnionException):
    """Collection of possibly multiple exceptions."""

    def __init__(self, msg: str, errors):
        self.msg = msg
        self.errors = errors
        super().__init__(msg, errors)


class Union(marshmallow.fields.Field):
    """Field that accepts any one of multiple fields.
    Each argument will be tried until one succeeds."""

    def __init__(
        self,
        fields: t.List[marshmallow.fields.Field],
        reverse_serialize_candidates: bool = False,
        **kwargs
    ):
        self._candidate_fields = fields
        self._reverse_serialize_candidates = reverse_serialize_candidates
        super().__init__(**kwargs)

    def _serialize(self, value: t.Any, attr: str, obj: str, **kwargs):
        """Pulls the value for the given key from the object, applies the
        field's formatting and returns the result."""

        error_store = kwargs.pop("error_store", marshmallow.error_store.ErrorStore())
        fields = self._candidate_fields
        if self._reverse_serialize_candidates:
            fields = list(reversed(fields))

        for candidate_field in fields:

            try:
                # pylint: disable=protected-access
                return candidate_field._serialize(
                    value, attr, obj, error_store=error_store, **kwargs
                )
            except (TypeError, ValueError) as e:
                error_store.store_error({attr: e})

        raise ExceptionGroup("All serializers raised exceptions.\n", error_store.errors)

    def _deserialize(self, value, attr=None, data=None, **kwargs):
        """Deserialize ``value``."""

        errors = []
        for candidate_field in self._candidate_fields:
            try:
                return candidate_field.deserialize(value, attr, data, **kwargs)
            except marshmallow.exceptions.ValidationError as exc:
                errors.append(exc.messages)
        raise marshmallow.exceptions.ValidationError(message=errors, field_name=attr)
