import re, socket

def get_host_addr(host):
    if re.match(r"([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})", host):
        return host
    
    try:
        return socket.gethostbyname(host)       
    except socket.gaierror:
        raise "[!] Invalid hostname !!"

def decode_frame(frame):
    opcode_and_fin = frame[0]

    # assuming it's masked, hence removing the mask bit(MSB) to get len. also assuming len is <125
    payload_len = frame[1] - 128

    mask = frame [2:6]
    encrypted_payload = frame [6: 6+payload_len]

    payload = bytearray([ encrypted_payload[i] ^ mask[i%4] for i in range(payload_len)]).decode()

    return payload

def encode_frame(payload):
    # setting fin to 1 and opcpde to 0x1
    frame = [129]
    # adding len. no masking hence not doing +128
    frame += [len(payload)]
    # adding payload
    frame_to_send = bytearray(frame) + payload

    return frame_to_send