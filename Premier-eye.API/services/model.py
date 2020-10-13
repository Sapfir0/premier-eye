import os
from config import Config
import json


def getSchema(schemaPath):
    with open(os.path.join(Config.dtoDirectory, schemaPath)) as json_schema:
        schema = json.load(json_schema)
        return schema


def getModel(modelName: str, api):
    schema = getSchema(modelName + ".json")
    model = api.schema_model(modelName, schema)
    return model
