from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)


class PokemonStoreCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define an AWS Dynamo DB Table 
        my_table = dynamodb.Table(
            self, 'PokemonStoreTable',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING}
        )

        # Define an AWS Lambda resource
        list_lambda = _lambda.Function(
            self, 'PokemonListHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='list.handler', 
            environment={
                'POKEMON_STORE_TABLE_NAME': my_table.table_name,
            }
        )
        my_table.grant_read_write_data(list_lambda)

        # Define an AWS Lambda resource
        create_lambda = _lambda.Function(
            self, 'PokemonCreateHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='create.handler', 
            environment={
                'POKEMON_STORE_TABLE_NAME': my_table.table_name,
            }
        )
        my_table.grant_read_write_data(create_lambda)

        # Define an AWS Lambda resource
        get_lambda = _lambda.Function(
            self, 'PokemonGetHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='get.handler', 
            environment={
                'POKEMON_STORE_TABLE_NAME': my_table.table_name,
            }
        )
        my_table.grant_read_write_data(get_lambda)

        update_lambda = _lambda.Function(
            self, 'PokemonUpdateHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='update.handler', 
            environment={
                'POKEMON_STORE_TABLE_NAME': my_table.table_name,
            }
        )
        my_table.grant_read_write_data(update_lambda)

        delete_lambda = _lambda.Function(
            self, 'PokemonDeleteHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='delete.handler', 
            environment={
                'POKEMON_STORE_TABLE_NAME': my_table.table_name,
            }
        )
        my_table.grant_read_write_data(delete_lambda)

        # Define an AWS API Gateway Rest API
        # You can also supply proxy: false, in which case you will have to explicitly define the API model:
        api_stage_options = apigw.StageOptions(stage_name="dev")
        my_api = apigw.LambdaRestApi(
            self, 'PokemonStoreEndpoint',
            handler=list_lambda,
            proxy=False,
            deploy_options=api_stage_options
        )

        # LambdaIntegration - can be used to invoke an AWS Lambda function.
        create_lambda_integration = apigw.LambdaIntegration(create_lambda)
        list_lambda_integration = apigw.LambdaIntegration(list_lambda)
        get_lambda_integration = apigw.LambdaIntegration(get_lambda)
        update_lambda_integration = apigw.LambdaIntegration(update_lambda)
        delete_lambda_integration = apigw.LambdaIntegration(delete_lambda)

        # define REST API model and associate methods with LambdaIntegrations
        pokemons = my_api.root.add_resource('pokemons')
        pokemons.add_method('GET', list_lambda_integration);    # GET /pokemons/
        pokemons.add_method('POST', create_lambda_integration); # POST /pokemons/

        pokemon = pokemons.add_resource('{id}')
        pokemon.add_method('GET', get_lambda_integration);    # GET /pokemons/{id}
        pokemon.add_method('PUT', update_lambda_integration);    # PUT /pokemons/{id}
        pokemon.add_method('DELETE', delete_lambda_integration);    # DELETE /pokemons/{id}