import unittest

import json_evolver


class TestCreateAndExtend(unittest.TestCase):

    def test_evolve(self):
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
        result = {"E": "ValueE", "New-A": "Value-A",
                  "New-B": {"New-B1": "ValueB1", "B2": "ValueB2"}}
        json_evolver.evolve(data, schema)
        self.assertEqual(data, result)

    def test_alias(self):
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
                    },
                    "required": ["New-B1"]
                }
            },
            "required": ["New-A"]
        }
        result = {"New-A": "Value-A", "New-B": {"New-B1": "ValueB1"}}
        json_evolver.evolve(data, schema)
        self.assertEqual(data, result)

    def test_default(self):
        data = {"A": "Value-A", "B": {"B1": "ValueB1"}, "C": "ValueR",
                "D": ["valueD1", "ValueD2"]}
        schema = {
            "type": "object",
            "properties": {
                "A": {
                    "default": "ValueA"
                },
                "B": {
                    "type": "object",
                    "properties": {
                        "B1" : {
                            "default": "ValueB1"
                        }
                    },
                    "required": ["B1"],
                },
                "E" : {
                    "default": "ValueE"
                }
            },
            "required": ["A"]
        }
        result = {"A": "Value-A", "B": {"B1": "ValueB1"}, "E": "ValueE"}
        json_evolver.evolve(data, schema)
        self.assertEqual(data, result)

    def test_extraneousProperties(self):
        data = {"A": "Value-A", "B": {"B1": "ValueB1"}, "C": "ValueR",
                "D": ["valueD1", "ValueD2"]}
        schema = {
            "type": "object",
            "properties": {
                "A": {
                    "alias": "A"
                },
                "B": {
                    "alias": "B",
                    "type": "object",
                    "properties": {
                        "B1": {
                            "alias": "B1"
                        }
                    },
                    "required": ["B1"]
                }
            },
            "required": ["A"]
        }
        result = {"A": "Value-A",
                  "B": {"B1": "ValueB1"}}
        json_evolver.evolve(data, schema)
        self.assertEqual(data, result)
