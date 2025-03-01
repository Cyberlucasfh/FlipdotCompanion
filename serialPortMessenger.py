import serial


def checkForAscii(string:str ) -> str:
    text = string
    sonderzeichen = {
        "ä":"{",
        "ö":"|",
        "ü":"}",
        "ß":"~",
        "Ä":"[",
        "Ö":"\\",
        "Ü":"]",
    }
    for char, ersatz in sonderzeichen.items():
        text = text.replace(char, ersatz)
    return text

def calc_paritybyte(data: bytes) -> bytes:
    parity_byte = 0x7F
    for byte in data:
        parity_byte ^= byte
    return bytes([parity_byte])

def calc_lenghtbyte(telegram: str):
    lenght = len(telegram)
    if lenght <= 11:
        return "1"
    elif lenght <= 27:
        return "2"
    else:
        return "3"


def send_data(line1: str, line2: str):
    ser = serial.Serial(
        port='COM5',  # COMX for Win, /dev/ttyUSB0 for Raspi
        baudrate=1200,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        timeout=1
    )
    if ser.isOpen():
        print("Comport offen")
    cleanedLine1 = checkForAscii(line1)
    cleanedLine2 = checkForAscii(line2)
    lenghtbyte = calc_lenghtbyte(cleanedLine1+cleanedLine2)
    #linie = b'l200\r'
    data = b'aA1'+lenghtbyte.encode('ascii')+b'A8'+cleanedLine1.encode('ascii')+b'\n'+cleanedLine2.encode('ascii')+b'\n\n              \r'
    #linientelegramm = linie + berechne_paritybyte(linie)
    parity = calc_paritybyte(data)
    telegram = data+parity

    print(telegram)

    try:
        ser.write(telegram)
    finally:
        ser.close()
