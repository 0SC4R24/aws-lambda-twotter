import json

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

    limit = body.get('limit', 10)

    user_name = None if "username" not in body else body.get('username')

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    users = None
    if cursor.execute('SELECT id, username, avatar, biography FROM users where username LIKE %s LIMIT %s', (f'%{user_name}%', limit)):
        users = [
            {
                'id': x[0],
                'username': x[1],
                'avatar': x[2],
                'biography': x[3]
            } for x in cursor.fetchall()
        ]

    cursor.close()
    conn.close()

    if users:
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(users)
        }

    return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': 'No messages found'
    }
