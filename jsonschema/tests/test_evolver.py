import json_evolver

data = {"A": "Value-A", "B": {"B1": "ValueB1"}, "C": "ValueR",
        "D": ["valueD1", "ValueD2"]}
schema = {
    "type": "object",
    "properties": {
        "New-A": {
            "alias": "A"
        },
        "New-B": {
            "alias": "B",
            "type": "object",
            "properties": {
                "New-B1": {
                    "alias": "B1"
                },
                "B2" : {
                    "default": "ValueB2"
                }
            },
            "required": ["New-B1"]
        },
        "E" : {
            "default": "ValueE"
        }
    },
    "required": ["New-A"]
}
json_evolver.evolve(data, schema)
print "Evolved JSON -> ", data
