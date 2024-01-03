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

    user_id = None if "user_id" not in body else body.get('user_id')

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    if user_id:
        cursor.execute('SELECT u.username, u.avatar, u.id, m.id, m.message, m.adjunct, m.datetime FROM messages as m JOIN users as u ON m.user_id = u.id where user_id=%s LIMIT %s', (user_id, limit))
    else:
        cursor.execute('SELECT u.username, u.avatar, u.id, m.id, m.message, m.adjunct, m.datetime FROM messages as m JOIN users as u ON m.user_id = u.id LIMIT %s', (limit,))

    messages = [
        {
            'username': x[0],
            'avatar': x[1],
            'user_id': x[2],
            'message_id': x[3],
            'message': x[4],
            'adjunct': x[5],
            'timestamp': x[6].timestamp()
        } for x in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    if messages:
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(messages)
        }

    return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': 'No messages found'
    }
