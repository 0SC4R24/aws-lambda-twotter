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
    if "username" not in body or "password" not in body:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Missing username or password"
        }

    # Parametros del usuario
    rg_username = body.get('username', 'None')
    rg_email = body.get('email', 'None')
    rg_password = body.get('password', 'None')
    rg_recover = body.get('recover', 'None')
    rg_avatar = body.get('avatar', 'https://cdn-icons-png.flaticon.com/512/9205/9205233.png')
    rg_biography = body.get('biography', 'None')

    conn = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
    cursor = conn.cursor()

    error_value = {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "Username or email already exists"
    }

    # Suponemos que cursor execute verifica el SQL Injection (revisarlo en futuro)
    try:
        if cursor.execute("INSERT INTO users (username, email, password, recover, avatar, biography) VALUES (%s, %s, %s, %s, %s, %s)", (rg_username, rg_email, rg_password, rg_recover, rg_avatar, rg_biography)) == 1:
            error_value = None
            conn.commit()
    except: pass

    cursor.close()
    conn.close()

    if error_value: return error_value

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': 'Created'
    }
