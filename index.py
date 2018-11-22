# -*- coding: utf-8 -*-
__author__ = 'Eric Z. Eisberg'
__copyright__ = 'Copyright 2018 Eric Z. Eisberg'
__license__ = 'Licensed under MIT license'

import copy
import json
import os

import requests
# We can use this response template to error out early, and ultimately to
# signal success to the web page
RESPONSE_TEMPLATE = {'isBase64Encoded': False,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
SLACK_URL = 'https://slack.com/api/chat.postMessage'

def post_to_slack(event, context):
    """ Posts a message to the slack #admin channel

        Args:
            event (dict): A representation of the event (HTTP in our case)
                that triggered the Lambda
            context (dict): AWS metadata like the lambda timeout, request ID,
                etc

        Returns:
            response (dict): Response object required by AWS lambda
    """
    # I don't think we need to do this for a Lambda, but don't modify the
    # global variable just in case.
    response = copy.deepcopy(RESPONSE_TEMPLATE)
    try:
        details = json.loads(event['body'])
        email = details['email']
        blurb = details['blurb']
    except Exception as ex:
        # Should see this
        print(str(ex))
        response['statusCode'] = 400
        return response

    # We'll need to set the Slack key in the Lambda environment
    # TODO: Figure out if there's a free secret management system for this
    slack_key = os.environ.get('slack_key')
    bearer_token = 'Bearer %s' % slack_key
    headers = {'Content-Type': 'application/json', 'Authorization': bearer_token}
    body_text = 'Invitation request from *%s*.\n```%s```' % (email, blurb)
    data = {
        'as_user': False,
        'channel': 'admin',
        'text': body_text,
        'username': 'InviteBot',
    }
    slack_res = requests.post(SLACK_URL, json=data, headers=headers)
    # If we're not getting a 200, something is wrong with Slack
    if not slack_res.status_code == 200:
        response['statusCode'] == 503
        return response
    response['statusCode'] = 204
    return response
