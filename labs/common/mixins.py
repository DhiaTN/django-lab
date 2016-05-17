import json
from functools import partial

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist


JSONSerializer = partial(serializers.serialize, 'json')


class SerializationMixin(object):

    excluded_fields = []

    @property
    def model_name(self):
        return self._meta.model_name

    def _get_concrete_fields(self):
        all_fields = self._meta.get_fields()
        return {f.attname: f for f in all_fields if f.concrete}

    def _is_concrete_field(self, field_name):
        return field_name in self.field_name_list

    def _get_field_value(self, field_name):
        field_type = self._get_field_type(field_name)
        field_value = getattr(self, field_name)
        if field_type in ['ImageField', 'FileField']:
                field_value = field_value.name
        return field_value

    def _get_field_object(self, field_name):
        fields_info = self._get_concrete_fields()
        return fields_info[field_name]

    def _get_field_type(self, field_name):
        field_obj = self._get_field_object(field_name)
        return field_obj.get_internal_type()

    def _is_foreign_key(self, field_name, one2one=True):
        foreign_key_types = ['ForeignKey']
        if one2one:
            foreign_key_types.append('OneToOneField')
        field_type = self._get_field_type(field_name)
        return field_type in foreign_key_types

    def _is_one_to_one_field(self, field_name):
        return field_name in self._one_to_one_fields()

    def _one_to_one_fields(self):
        all_fields = self._meta.get_fields()
        fields_list = list()
        push = fields_list.append
        for f in all_fields:
            if f.one_to_one:
                if f.concrete:
                    push(f.attname[:-3])
                    continue
                push(f.get_accessor_name())
        return fields_list

    def _non_concrete_one_to_one(self):
        all_fields = self._meta.get_fields()
        fields_list = list()
        push = fields_list.append
        for f in all_fields:
            if f.one_to_one and not f.concrete:
                push(f.get_accessor_name())
        return fields_list

    def foreignkey_list(self, one2one=True, non_concrete=False):
        field_list = list()
        push = field_list.append
        for field_name in self.field_name_list:
            if self._is_foreign_key(field_name, one2one):
                foreign_field = field_name[:-3]
                if foreign_field not in self.excluded_fields:
                    push(field_name[:-3])
        if non_concrete:
            field_list.extend(self._non_concrete_one_to_one())
        return field_list

    @property
    def field_name_list(self):

        def not_excluded(f):
            return f not in self.excluded_fields

        concrete_fields_dict = self._get_concrete_fields()
        return filter(not_excluded, concrete_fields_dict.keys())

    def to_dict(self):
        data = self.serialize()
        return data[0]['fields']

    def serialize(self):
        data = JSONSerializer([self])
        json_data = json.loads(data)
        for field in json_data[0]['fields'].keys():
            if field in self.excluded_fields:
                del json_data[0]['fields'][field]
        return json_data

    def deep_serialize(self, one2one=True):
        data = self.serialize()
        for field_name in self.foreignkey_list(one2one):
            try:
                one2one_flag = self._is_one_to_one_field(field_name)
                field_content = getattr(self, field_name)
                field_content = field_content.deep_serialize(one2one_flag)
                data.extend(field_content)
            except (ObjectDoesNotExist, AttributeError) as e:
                # 1. ObjectDoesNotExist: is external model but is null
                # 2. AttributeError: field_content is not external model
                #    relation and has not `.to_full_dict` attribute
                continue
        return data

