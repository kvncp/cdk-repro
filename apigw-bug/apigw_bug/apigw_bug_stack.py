from aws_cdk import Stack, aws_apigateway, aws_lambda
from constructs import Construct


class ApigwBugStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fake_lambda = aws_lambda.Function(
            self,
            "lambda",
            code=aws_lambda.Code.from_inline("..."),
            handler="handler",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
        )

        api = aws_apigateway.RestApi(
            self,
            "api",
            default_method_options=aws_apigateway.MethodOptions(
                authorization_type=aws_apigateway.AuthorizationType.CUSTOM,
                authorizer=aws_apigateway.TokenAuthorizer(
                    self, "auth", handler=fake_lambda
                ),
            ),
        )

        api.root.add_resource("authenticated_endpoint").add_method(
            "GET", integration=aws_apigateway.HttpIntegration("http://www.example.com")
        )

        noauth_method = api.root.add_resource("unauthenticated_endpoint").add_method(
            "GET",
            integration=aws_apigateway.HttpIntegration("http://www.example.com"),
            # This does not work, but should
            # Error: ApigwBugStack/api/Default/unauthenticated_endpoint/GET -
            #   Authorization type is set to NONE which is different from what is required by the authorizer [CUSTOM]
            # authorization_type=aws_apigateway.AuthorizationType.NONE,
        )
        # This workaround does work, showing this is a CDK problem, not a CF or API GW problem.
        noauth_method.node.default_child.add_property_override("AuthorizationType", "NONE")
