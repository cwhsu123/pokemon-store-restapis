import json
import pytest

from aws_cdk import core
from pokemon_store_cdk_stack import PokemonStoreCdkStack


def get_template():
    app = core.App()
    PokemonStoreCdkStack(app, "pokemon-store-cdk")
    return json.dumps(app.synth().get_stack("pokemon-store-cdk").template)


def test_dynamodb_table_created():
    assert("AWS::DynamoDB::Table" in get_template())
