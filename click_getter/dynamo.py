import boto3
import os
from loggers import logger
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.types import Decimal as D

deserializer = TypeDeserializer()


def deserialize(value):
    d_value = deserializer.deserialize(value)
    if isinstance(d_value, D):
        return int(d_value)
    else:
        return d_value


class Dynamo:
    def __init__(self, region, clicksTable):
        os.environ["AWS_DEFAULT_REGION"] = region
        self.dynamo = boto3.client("dynamodb")
        self.clicksTable = clicksTable
        # self.ipTable = ipTable

    def get_all_country_clicks(self):
        deserialized_items = []
        try:
            response = self.dynamo.scan(
                TableName=self.clicksTable,
            )
        except Exception as e:
            logger.error("Failed to get clicks due to: {}".format(str(e)))
            raise
        logger.info("Obtained clicks")
        items = response["Items"]
        if items:
            for item in items:
                deserialized_items.append({k: deserialize(v) for k, v in item.items()})
            return deserialized_items
        else:
            return deserialized_items


d = Dynamo("us-east-2", "click_bags_dev")
print(d.get_all_country_clicks())
