import serial
import customtkinter
import time
from enum import Enum

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("750x750")

frame = customtkinter.CTkFrame(root)
frame.pack(padx=20, pady=60, fill="both", expand=True)

label = customtkinter.CTkLabel(frame, text="TrackPen UI v0.1")
label.pack(padx=12, pady=10)

accelerometer_enabled = gyro_enabled = trackball_enabled = True


class DataStream(Enum):
    ACCELEROMETER = 1
    GYROSCOPE = 2
    TRACKBALL = 3


def toggle_data(data_stream: DataStream):
    global accelerometer_enabled, gyro_enabled, trackball_enabled
    if data_stream == DataStream.ACCELEROMETER:
        accelerometer_enabled = not accelerometer_enabled
    elif data_stream == DataStream.GYROSCOPE:
        gyro_enabled = not gyro_enabled
    elif data_stream == DataStream.TRACKBALL:
        trackball_enabled = not trackball_enabled


accelerometer_label = customtkinter.CTkLabel(frame, text="Accelerometer")
accelerometer_label.pack(padx=12, pady=10)

accelerometer_button = customtkinter.CTkButton(
    frame, text="Start/Stop", command=lambda: toggle_data(DataStream.ACCELEROMETER)
)
accelerometer_button.pack(padx=12, pady=10)

accelerometer_str = customtkinter.StringVar(value="X: 0, Y: 0, Z: 0")
accelerometer_data = customtkinter.CTkLabel(
    frame, textvariable=accelerometer_str)
accelerometer_data.pack(padx=12, pady=10)

gyro_label = customtkinter.CTkLabel(frame, text="Gyroscope")
gyro_label.pack(padx=12, pady=10)

gyro_button = customtkinter.CTkButton(
    frame, text="Start/Stop", command=lambda: toggle_data(DataStream.GYROSCOPE)
)
gyro_button.pack(padx=12, pady=10)

gyro_str = customtkinter.StringVar(value="X: 0, Y: 0, Z: 0")
gyro_data = customtkinter.CTkLabel(frame, textvariable=gyro_str)
gyro_data.pack(padx=12, pady=10)


trackball_label = customtkinter.CTkLabel(frame, text="Trackball")
trackball_label.pack(padx=12, pady=10)

trackball_button = customtkinter.CTkButton(
    frame, text="Start/Stop", command=lambda: toggle_data(DataStream.TRACKBALL)
)
trackball_button.pack(padx=12, pady=10)

trackball_str = customtkinter.StringVar(value="X: 0, Y: 0, Is Clicked?: False")
trackball_data = customtkinter.CTkLabel(frame, textvariable=trackball_str)
trackball_data.pack(padx=12, pady=10)


arduino_data = serial.Serial("/dev/cu.usbmodem1101", 9600)

accel_x = accel_y = accel_z = gyro_x = gyro_y = gyro_z = tb_x = tb_y = 0

is_clicked = False
click_status = {
    False: "Not Clicked",
    True: "Clicked",
}

data_file = f"data/{time.time()}.txt"


while True:
    while arduino_data.inWaiting() == 0:
        pass

    data = arduino_data.readline()
    data = data.decode("utf-8").strip("\r\n")
    (
        accel_x,
        accel_y,
        accel_z,
        gyro_x,
        gyro_y,
        gyro_z,
        change_tb_x,
        change_tb_y,
        clicked,
        released,
    ) = data.split(",")

    (
        accel_x,
        accel_y,
        accel_z,
        gyro_x,
        gyro_y,
        gyro_z,
        change_tb_x,
        change_tb_y,
        clicked,
        released,
    ) = (
        float(accel_x),
        float(accel_y),
        float(accel_z),
        float(gyro_x),
        float(gyro_y),
        float(gyro_z),
        int(change_tb_x),
        int(change_tb_y),
        int(clicked),
        int(released),
    )

    with open(data_file, "a") as f:
        if accelerometer_enabled:
            f.write(
                f"Accelerometer: X: {accel_x}, Y: {accel_y}, Z: {accel_z}\n")
        if gyro_enabled:
            f.write(f"Gyroscope: X: {gyro_x}, Y: {gyro_y}, Z: {gyro_z}\n")
        if trackball_enabled:
            f.write(
                f"Trackball: X: {tb_x}, Y: {tb_y}, Button Status: {click_status[is_clicked]}\n"
            )

    accelerometer_str.set(f"X: {accel_x}, Y: {accel_y}, Z: {accel_z}")
    accelerometer_data.update()

    gyro_str.set(f"X: {gyro_x}, Y: {gyro_y}, Z: {gyro_z}")
    gyro_data.update()

    tb_x += change_tb_x
    tb_y += change_tb_y
    if clicked:
        is_clicked = True
    elif released:
        is_clicked = False

    trackball_str.set(
        f"X: {tb_x}, Y: {tb_y}, Button Status: {click_status[is_clicked]}"
    )
    trackball_data.update()

    root.update()
