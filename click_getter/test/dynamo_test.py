import dynamo
from boto3.dynamodb.types import Decimal as D


def test_decimal_conversion():
    convert_from = {"N": "10"}
    non_decimal = dynamo.deserialize(convert_from)
    assert non_decimal == 10
