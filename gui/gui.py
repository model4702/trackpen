import serial

arduino_data = serial.Serial("/dev/cu.usbmodem1101", 9600)

while True:
    while arduino_data.inWaiting() == 0:
        pass
    data = arduino_data.readline()
    # print("raw data", data)
    data = data.decode("utf-8").strip("\r\n")
    left, right, up, down, clicked, released = [
        int(x) for x in data.split(",")]
