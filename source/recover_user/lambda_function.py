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
    if "username" not in body or "password" not in body or "recover" not in body:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Missing username or password or recover"
        }

    # Variables de control
    lg_validated = True
    lg_recover_wrong = False

    # Variables de verificacion
    lg_username = body.get("username")
    lg_password = body.get("password")  # Ya tiene que estar encriptada en el cliente
    lg_recover = body.get("recover")

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    if cursor.execute("SELECT recover, validated FROM users WHERE username = %s", (lg_username,)) == 1:
        if cursor.rowcount != 0:
            lg_recover_bbdd, lg_validated = cursor.fetchone()
            if lg_recover != lg_recover_bbdd: lg_recover_wrong = True

        if lg_validated and not lg_recover_wrong:
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (lg_password, lg_username))
            conn.commit()

        cursor.close()
        conn.close()

    else: return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "User not found"
    }

    if not lg_validated: return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "User not validated. Contact an administrator"
    }

    if lg_recover_wrong: return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "Wrong recover code"
    }

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "Password changed successfully"
    }
