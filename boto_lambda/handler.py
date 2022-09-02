import boto3

_SESSION = boto3.Session(region_name="us-west-2")
_IOT_DATA_CLIENT = _SESSION.client("iot-data")


def handler(entry, context):

    return _IOT_DATA_CLIENT.get_thing_shadow(
        thingName="MyThingName", shadowName="MyShadowName"
    )['payload'].read()
