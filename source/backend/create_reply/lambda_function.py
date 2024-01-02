import json
from datetime import datetime

import jwt
import pymysql

SECRET = "PROYECTO3SISDIS2024"
# Encode token: jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
# Decode token: jwt.decode(encoded, "secret", algorithms=["HS256"])

rds_host = "52.204.152.143"
username = "practica3"
password = "practica3"
database = "practica3"
bucketUrl = "https://0sc4r24sisdis2024.s3.us-east-1.amazonaws.com/"


def lambda_handler(event, context):
    # if "isBase64Encoded" in event:
    #     isEncoded = bool(event["isBase64Encoded"])
    #
    #     if isEncoded:
    #         decodedBytes = base64.b64decode(event["body"])
    #         decodedStr = decodedBytes.decode("ascii")
    #         print(json.dumps(parse_qs(decodedStr)))
    #         decodedEvent = json.loads(json.dumps(parse_qs(decodedStr)))
    #         user = decodedEvent["user"][0]
    #
    # else:
    #     user = event["body"]["user"]

    print(event)

    body = json.loads(event.get("body", "{}"))

    if "token" not in body or "message" not in body or "message_id" not in body:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Missing token, message or message_id"
        }

    try:
        decoded = jwt.decode(body.get("token"), SECRET, algorithms=["HS256"])
        user_id = decoded.get('id', None)
        exp = decoded.get('exp', 0)

        if datetime.now().timestamp() > exp:
            return {
                'statusCode': 401,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': "Token has expired"
            }

    except:
        return {
            'statusCode': 401,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Invalid token"
        }

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    if user_id:
        cursor.execute("INSERT INTO replies (message_id, user_id, comment) VALUE (%s, %s, %s)", (body.get("message_id"), user_id, body.get("message")))
        conn.commit()

    cursor.close()
    conn.close()

    if not user_id:
        return {
            'statusCode': 401,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': 'Reply not created'
        }

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': 'Reply created'
    }
