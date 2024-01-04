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

    user_id = None if "user_id" not in body else body.get('user_id')
    token = None if "token" not in body else body.get('token')

    if token and user_id:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': 'Cannot receive more than one parameter. Only user_id or token can be passed, not both.'
        }

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    if token:
        try:
            decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_id = decoded.get('id')
            exp = decoded.get('exp')

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

    user = None
    if cursor.execute('select id, username, email, avatar, biography from users where id = %s', (user_id,)):
        userdata = cursor.fetchone()
        user = {
            'id': userdata[0],
            'username': userdata[1],
            'email': userdata[2],
            'avatar': userdata[3],
            'biography': userdata[4]
        }

    cursor.close()
    conn.close()

    if user:
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(user)
        }

    return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': 'No user found'
    }
