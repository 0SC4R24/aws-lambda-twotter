import json
from datetime import timedelta, datetime

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
    if "username" not in body or "password" not in body:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Missing username or password"
        }

    # Variables de control
    lg_id = None
    lg_validated = True
    lg_password_wrong = False

    # Variables de verificacion
    lg_username = body.get("username")
    lg_password = body.get("password")  # Ya tiene que estar encriptada en el cliente

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    cursor.execute("SELECT id, password, validated FROM users WHERE username = %s", (lg_username,))

    if cursor.rowcount != 0:
        lg_id, lg_password_bbdd, lg_validated = cursor.fetchone()
        if lg_password != lg_password_bbdd: lg_password_wrong = True

    if lg_password_wrong and cursor.execute("SELECT tries FROM users WHERE username = %s", (lg_username,)) == 1:
        tries = cursor.fetchone()[0]
        if tries < 3: cursor.execute("UPDATE users SET tries = %s WHERE username = %s", (tries + 1, lg_username))
        else: cursor.execute("UPDATE users SET tries = %s, validated = 0 WHERE username = %s", (3, lg_username))
        conn.commit()

    cursor.close()
    conn.close()

    if not lg_validated: return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "User not validated. Contact an administrator"
    }

    if lg_password_wrong: return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "Incorrect password"
    }

    if not lg_id: return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "Incorrect username"
    }

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': jwt.encode({"id": lg_id, 'exp': (datetime.now() + timedelta(days=1)).timestamp()}, SECRET, algorithm="HS256")  # Token con expiracion de 1 dia y el id del usuario
    }
