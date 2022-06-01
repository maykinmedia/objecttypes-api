from django.db.models.query import QuerySet


class ObjectTypeQuerySet(QuerySet):
    def create_from_schema(self, json_schema: dict, **kwargs):
        object_type_data = {
            "name": json_schema.get("title", "").title(),
            "description": json_schema.get("description", ""),
        }
        object_type_data.update(kwargs)
        objecttype = self.create(**object_type_data)

        objecttype.versions.create(json_schema=json_schema)

        return objecttype
