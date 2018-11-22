# EngSciMath Slack Integration Lambda

This lambda allows us to handle incoming requests from a static splash page, while reducing the operational complexity associated with maintaining a server.

Runtime: Python 3.6

## Configuration and Deployment

The only requirement is `requests`. As of November 2018, we're uploading a deployment package manually.

AWS has good instructions for packaging a Python lambda for deployment. Follow the zip instructions at https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

(Note: You'll have to manually upload the file from the console)
