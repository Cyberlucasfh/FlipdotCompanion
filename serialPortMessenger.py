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

def berechne_paritybyte(daten: bytes) -> bytes:
    parity_byte = 0x7F
    for byte in daten:
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


def sende_daten(zeile1: str, zeile2: str):
    ser = serial.Serial(
        port='COM5',  # COMX for Win, /dev/ttyUSB0 for Raspi
        baudrate=1200,
        bytesize=serial.SEVENBITS,  # 7 Datenbits
        parity=serial.PARITY_EVEN,  # Gerade Parität
        stopbits=serial.STOPBITS_TWO,  # 2 Stopbits
        timeout=1
    )
    if ser.isOpen():
        print("Comport offen")
    cleanedLine1 = checkForAscii(zeile1)
    cleanedLine2 = checkForAscii(zeile2)
    lenghtbyte = calc_lenghtbyte(cleanedLine1+cleanedLine2)
    #linie = b'l200\r'
    daten = b'aA1'+lenghtbyte.encode('ascii')+b'A8'+cleanedLine1.encode('ascii')+b'\n'+cleanedLine2.encode('ascii')+b'\n\n              \r'
    #linientelegramm = linie + berechne_paritybyte(linie)
    parity = berechne_paritybyte(daten)
    telegram = daten+parity

    print(telegram)

    try:
        ser.write(telegram)
    finally:
        ser.close()
