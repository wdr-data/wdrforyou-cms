import os

from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL = os.environ.get('SLACK_CHANNEL')
CLIENT = SlackClient(SLACK_TOKEN)


def post_message(message, *, private=False, channel=CHANNEL, **kwargs):
    """
    Send message with attachments to Slack on channel. Set 'private' to a user ID to send a message
    that only that user can see. Set 'channel' to a specific ID to send in a channel different from
    the default channel.
    """
    if not private:
        return CLIENT.api_call(
            'chat.postMessage',
            channel=channel,
            text=message,
            **kwargs,
        )
    else:
        return CLIENT.api_call(
            'chat.postEphemeral',
            channel=channel,
            user=private,
            text=message,
            **kwargs,
        )
