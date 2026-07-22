import json
import os
import urllib.request

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def lambda_handler(event, context):

    message = "📢 StreamingApp Alert\n\n"

    if "Records" in event:
        for record in event["Records"]:
            sns_message = record["Sns"]["Message"]
            message += sns_message
    else:
        message += json.dumps(event)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": message
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    urllib.request.urlopen(req)

    return {
        "statusCode": 200,
        "body": "Telegram notification sent!"
    }