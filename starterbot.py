import os
import time
import re
import OnTap
from slackclient import SlackClient


# Many thanks to Matt Makai for the shell that runs the bot. 
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "fills"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
HELP = "Commands:\n *taps* (now pouring)\n*fills* (beers available for growler fills)\n*products* (available in bottles and/or cans)\n*breweries* (list of breweries OnTap can query)\n\nSample usage: Luppolo taps"
BREWERIES = ['ThirtyThreeAcres', 'Bomber', 'Brassneck', 'Faculty', 'Luppolo', 'Parallel49', 'RnB', 'StrangeFellows']
BREWERY_VARIANTS = [('33 Acres', 'ThreeAcres', '33Acres', 'thirtythreeacres', '33acres'), ('Bomber', 'bomber'), ('Brassneck', 'brassneck'), ('Fauclty', 'faculty'), ('Luppolo', 'luppolo'), ('Parallel 49', 'Parallel49', 'parallel49'), ('R&B', 'RnB', 'rnb', 'RandB'), ('Strange Fellows', 'StrangeFellows', 'strangefellows')]


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def pretty_up_response(ugly_list):
    if isinstance(ugly_list[2], list):
        formatted_collection = []
        formatted_collection.append(ugly_list[0] + ugly_list[1])
        for i in range(2, len(ugly_list)):
            ugly_list[i][0] = "*" + ugly_list[i][0] + "*"
            formatted_collection.append(ugly_list[i])
        return formatted_collection
    else:
        formatted_msg = ""
        for item in ugly_list: 
            formatted_msg = formatted_msg + item + "\n"
        return formatted_msg


def confirm_brewery_name(brewery):
    proper_name = None
    for items in BREWERY_VARIANTS:
        if brewery in items:
            proper_name = items[0]
    return proper_name 


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """

    # Default response 
    default_response = "Try *{}*.".format(EXAMPLE_COMMAND) + " Or use *{}* for a list of valid commands.".format("Commands")

    # Finds and executes the given command, filling in response
    response = None
    
    # split command into words
    query = command.lower().split()

    if len(query) == 1: 

        # chatty responses 
        if query[0] == ':beer:' or query[0] == ':beers:':
            response = ":beer:"
        
        elif query[0] == "hello":
            response = "cheers!"
        
        # help & instructions 
        elif query[0] == 'help' or query[0] == 'commands':
            response = HELP

        elif query[0] == 'breweries':
            response = pretty_up_response(BREWERIES)

        # error 
        elif  query[0] in [x.lower() for x in BREWERIES]:
            response = "Add a command (taps, fills, or products) after brewery name" 

    elif len(query) == 2: 
        # core functionality 
        if query[0] not in [x.lower() for x in BREWERIES]:
            response = "Brewery name invalid or not on list OnTap can query."

        elif query[1] == 'taps' or query[1] == 'fills' or query[1] == 'products':
            brewery_name = confirm_brewery_name(query[0])
            list_to_format = OnTap.main(brewery_name, query[1])
            response = pretty_up_response(list_to_format)
        

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")