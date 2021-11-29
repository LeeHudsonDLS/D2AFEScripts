import telnetlib
import time
import datetime

host = "172.23.241.15"
#host = "localhost"
port = 7003
timeout = 100

def getLogSuffix():
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year

    return f"{day}-{month}-{year}"

def compute_lrc(stringIn):
    checksum = 0x0
    bytes = str.encode(stringIn)
    for b in bytes:
        checksum ^= b
    return checksum


def logToFile(message,fileName):
    f = open(fileName, "a")
    f.write(message)
    f.close()


with telnetlib.Telnet(host, port, timeout) as session:
    while 1:
        session.write(b"1 mon\r\n")
        fullMessage = session.read_until(b"\n")
        messageRaw = fullMessage[:-5]
        lrc = int(fullMessage[-4:-2].decode(),16)

        print(fullMessage)

        fileSuffix = getLogSuffix()
        errorFile = f"/home/jjc62351/work/D2AFE/err{fileSuffix}.txt"
        fullFile = f"/home/jjc62351/work/D2AFE/log{fileSuffix}.txt"
        
        calcLrc = compute_lrc(messageRaw.decode())
        logToFile(fullMessage.decode(),fullFile)
        if calcLrc != lrc:
            logToFile(fullMessage.decode(),errorFile)
            logToFile(f"\tRecieved LRC (hex) = {hex(lrc)}\r\n",errorFile)
            logToFile(f"\tCalculate LRC (dec) = {hex(calcLrc)}\r\n",errorFile)
        if len(fullMessage) < 110:
            logToFile(fullMessage.decode(),errorFile)
            logToFile(f"\tMessage len = {len(fullMessage)}",errorFile)


        time.sleep(0.2)