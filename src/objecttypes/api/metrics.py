from opentelemetry import metrics

meter = metrics.get_meter("objecttypes.api.v2")

objecttype_create_counter = meter.create_counter(
    "objecttypes.objecttype.creates",
    description="Amount of objecttypes created (via the API).",
    unit="1",
)
objecttype_update_counter = meter.create_counter(
    "objecttypes.objecttype.updates",
    description="Amount of objecttypes updated (via the API).",
    unit="1",
)
objecttype_delete_counter = meter.create_counter(
    "objecttypes.objecttype.deletes",
    description="Amount of objecttypes deleted (via the API).",
    unit="1",
)
