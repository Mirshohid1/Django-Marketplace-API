def sync_related_entities(
    *,
    existing_objects: dict,
    incoming_data: list[dict],
    objects_to_create: list,
    objects_to_update: list,
    update_fields: list[str],
    model_class,
):
    incoming_ids = {obj.get("id") for obj in incoming_data if obj.get("id")}
    existing_ids = set(existing_objects.keys())

    ids_to_delete = existing_ids - incoming_ids

    model_class.objects.filter(id__in=ids_to_delete).delete()

    model_class.objects.bulk_create(
        objects_to_create,
    )

    model_class.objects.bulk_update(
        objects_to_update,
        update_fields,
    )
