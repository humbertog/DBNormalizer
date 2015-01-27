__author__ = 'Humberto, Gabriela'


def get_schema_attribute_property(attr_schema, att_property='type', attr_name=None):
    attributes = []
    if attr_name is None:
        for x in attr_schema:
            attributes.append(x[att_property])
    else:
        attributes = [x[att_property] for x in self.attributes if x['name'] == attr_name]
    return attributes


def get_schema_keys(key_schema, key_property='constrained_columns'):
    return key_schema[key_property]


def get_schema_unique(unique_schema, un_property='column_names'):
    unique = []
    for x in unique_schema:
        unique.append(x[un_property])
    return unique