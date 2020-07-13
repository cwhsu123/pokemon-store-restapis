#!/usr/bin/env python3

from aws_cdk import core

from pokemon_store_cdk.pokemon_store_cdk_stack import PokemonStoreCdkStack


app = core.App()
PokemonStoreCdkStack(app, "pokemon-store-cdk", env={'region': 'us-west-2'})

app.synth()
