import aws_cdk as core
import aws_cdk.assertions as assertions

from application.resource_stack import ResourceStack


# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_hello/cdk_hello_stack.py
def test_sqs_queue_created(env):
    app = core.App()
    stack = ResourceStack(app, "cdk-hello", env)
    template = assertions.Template.from_stack(stack)

    # breakpoint()


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
