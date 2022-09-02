from aws_cdk import Stack, Duration
import aws_cdk.aws_lambda_python_alpha as lambda_python
import aws_cdk.aws_lambda as lambda_
from constructs import Construct
import aws_cdk.aws_iam as iam


class CdkReproStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        func = lambda_python.PythonFunction(
            self,
            "Func",
            entry="boto_lambda",
            index="handler.py",
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(30)
        )

        func.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["iot:GetThingShadow"],
                resources=["*"],
            )
        )


