import os

from slack import WebClient

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL = os.environ.get('SLACK_CHANNEL')
CLIENT = WebClient(SLACK_TOKEN)


def section(text, type='mrkdwn'):
    return {
        "type": 'section',
        "text": {
            "type": type,
            "text": text
        }
    }


def context(*elements):
    return {
        "type": 'context',
        "elements": elements,
    }


def element(text, type='mrkdwn'):
    return {
        "type": type,
        "text": text
    }


def divider():
    return {"type": "divider"}


def post_message(*, private='', channel=CHANNEL, **kwargs):
    """
    Send message with attachments to Slack on channel. Set 'private' to a user ID to send a message
    that only that user can see. Set 'channel' to a specific ID to send in a channel different from
    the default channel.
    """
    if not private:
        return CLIENT.chat_postMessage(
            channel=channel,
            **kwargs,
        )
    else:
        return CLIENT.chat_postEphemeral(
            channel=channel,
            user=private,
            **kwargs,
        )
