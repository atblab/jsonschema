import jsonschema

def evolve_json(instance, schema):
    """
    Evolves the JSON data before validating.
    The provided new schema will compare with JSON data and evolves it.
    """
    subschemas = [(instance, schema)]
    while subschemas:
        subinstance, subschema = subschemas.pop()

        DefaultSetter(subschema).validate(subinstance)
        subschemas.extend(
            (subinstance.setdefault(property_v, {}), subsubschema)
            for property_v, subsubschema in
            subschema.get("properties", {}).items()
        )


def _evolve(validator, properties, instance, schema):
    """
    Checks aliases and new fields by iterating the items in properties and
    change the JSON data accordingly.
    """
    for property_val, subschema in properties.items():
        if "alias" in subschema and property_val not in instance:
            instance[property_val] = instance[subschema["alias"]]
            del instance[subschema["alias"]]
        if "default" in subschema:
            instance.setdefault(property_val, subschema["default"])
    for temp_instance in instance.keys():
            if temp_instance not in properties:
                del instance[temp_instance]
DefaultSetter = jsonschema.validators.create(
    meta_schema={}, validators={"properties": _evolve},
)

def extend(validator_cls):
    '''
    Extended validator class to add new validations,
    Currently the JSON data evolution process is done before validation.
    '''
    Validator = jsonschema.validators.extend(
        validator_cls, {
#           "properties" : _properties_with_aliases(validator_cls),
        }
    )

    class Blueprinter(Validator):
        def instantiate(self, data, blueprint):
            self.validate(data)
            return data

    return Blueprinter


def evolve(data, schema):
    evolve_json(data, schema)
    Validator = jsonschema.validators.validator_for(schema)
    blueprinter = extend(Validator)(schema)
    return blueprinter.instantiate(data, schema)
