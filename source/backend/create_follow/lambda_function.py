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
    if "action" not in body or "token" not in body or "following_id" not in body:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': 'Missing action, token or following_id'
        }

    action = body.get("action")
    token = body.get("token")
    following_id = body.get("following_id")

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
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

    if action == "follow":
        cursor.execute("INSERT INTO followers (user_id, following_id) VALUES (%s, %s)", (user_id, following_id))

    else:
        cursor.execute("DELETE FROM followers WHERE user_id = %s AND following_id = %s", (user_id, following_id))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': 'Follow created'
    }
