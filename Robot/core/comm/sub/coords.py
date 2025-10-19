slot = None

def callback(client, userinfo, message):
    payload_str: str = message.payload.decode()
    coords = payload_str.split(',')
    slot(float(coords[0]) , float(coords[1])) # type: ignore

