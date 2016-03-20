from functools import partial
from django.db.models import Model


class ModelMixin(Model):

    def _get_fields(self):
        all_fields = self._meta.get_fields()
        return [f for f in all_fields if f.concrete]

    @property
    def concrete_field_list(self):
        field_list = self._get_fields()
        return [f.attname for f in field_list]

    def to_dict(self):
        result = dict()
        push = result.update
        get_value = partial(getattr, self)
        for field_name in self.concrete_field_list:
            field_content = get_value(field_name)
            is_m2m_field = hasattr(field_content, 'source_field')
            if is_m2m_field:
                field_content = field_content.values_list('id', flat=True)
            push({field_name: field_content})
        return result

    def to_full_dict(self):
        full_data = dict()
        fields = self._get_fields()
        get_value = partial(getattr, self)
        for field in fields:
            field_content = get_value(field.attname)
            if field.is_relation:
                if hasattr(field_content, 'values'):
                    field_content = field_content.values()
            full_data.update({field.attname: field_content})
        return full_data

    class Meta:
        abstract = True
