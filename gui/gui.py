import serial
import customtkinter
import time

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("500×350")

frame = customtkinter.CTkFrame(root)
frame.pack(padx=20, pady=60, fill="both", expand=True)

label = customtkinter.CTkLabel(frame, text="TrackPen UI v0.1")
label.pack(padx=12, pady=10)

accelerometer_label = customtkinter.CTkLabel(frame, text="Accelerometer")
accelerometer_label.pack(padx=12, pady=10)

accelerometer_str = customtkinter.StringVar(value="X: 0, Y: 0, Z: 0")
accelerometer_data = customtkinter.CTkLabel(
    frame, textvariable=accelerometer_str)
accelerometer_data.pack(padx=12, pady=10)

trackball_label = customtkinter.CTkLabel(frame, text="Trackball")
trackball_label.pack(padx=12, pady=10)

trackball_str = customtkinter.StringVar(value="X: 0, Y: 0, Is Clicked?: False")
trackball_data = customtkinter.CTkLabel(frame, textvariable=trackball_str)
trackball_data.pack(padx=12, pady=10)


# root.mainloop()
arduino_data = serial.Serial("/dev/cu.usbmodem1101", 9600)

accel_x = accel_y = accel_z = tb_x = tb_y = 0
is_clicked = False

while True:
    while arduino_data.inWaiting() == 0:
        pass

    data = arduino_data.readline()
    # print(data.decode("utf-8").strip("\r\n"))
    data = data.decode("utf-8").strip("\r\n")
    (
        accel_x,
        accel_y,
        accel_z,
        change_tb_x,
        change_tb_y,
        clicked,
        released,
    ) = data.split(",")

    accel_x, accel_y, accel_z, change_tb_x, change_tb_y, clicked, released = (
        float(accel_x),
        float(accel_y),
        float(accel_z),
        int(change_tb_x),
        int(change_tb_y),
        int(clicked),
        int(released),
    )

    accelerometer_str.set(f"X: {accel_x}, Y: {accel_y}, Z: {accel_z}")
    accelerometer_data.update()

    tb_x += change_tb_x
    tb_y += change_tb_y
    if clicked:
        is_clicked = True
    elif released:
        is_clicked = False

    trackball_str.set(f"X: {tb_x}, Y: {tb_y}, Is Clicked?: {is_clicked}")
    trackball_data.update()

    root.update()


# while True:
#     while arduino_data.inWaiting() == 0:
#         pass
#     data = arduino_data.readline()
#     # print("raw data", data)
#     data = data.decode("utf-8").strip("\r\n")
#     left, right, up, down, clicked, released = [
#         int(x) for x in data.split(",")]


# while True:
#     while arduino_data.inWaiting() == 0:
#         pass
#     data = arduino_data.readline()
#     data = data.decode("utf-8").strip("\r\n")
#     # print(data)
#     # print([float(x) for x in data.split("/")])
#     rollF, pitchF = [float(x) for x in data.split("/")]
#     print(rollF, pitchF)
