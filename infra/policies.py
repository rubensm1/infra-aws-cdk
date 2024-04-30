from aws_cdk import aws_iam as iam

# In order to successfully generate a CodeArtifact token, we must add a custom role granting
# a few permissions to CodeBuild
pipeline_policy = [
    iam.PolicyStatement(
        actions=[
            "codeartifact:GetAuthorizationToken",
            "codeartifact:GetRepositoryEndpoint",
            "codeartifact:ReadFromRepository",
            "codebuild:StartBuild",
            "codebuild:CreateReport",
            "codebuild:BatchPutTestCases",
            "codebuild:UpdateReport",
            "codebuild:BatchPutCodeCoverages",
        ],
        resources=["*"],
    ),
    iam.PolicyStatement(
        actions=["sts:GetServiceBearerToken"],
        resources=["*"],
        conditions={
            "StringEquals": {"sts:AWSServiceName": "codeartifact.amazonaws.com"}
        },
    ),
]
