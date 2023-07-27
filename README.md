# TrackPen

## Setup

1. Clone the repository on your local machine

```
$ git clone https://github.com/charliesabino/trackpen.git
```

2. Enter the gui folder.

```
$ cd trackpen/gui
```

3. Connect the Arduino and its modules.

- GY-85:
  - 3.3V to 5V
  - GND to GND
  - SCL tO A5
  - SDA to A4
- Trackball:
  - 3-5V to 3.3V
  - GND to GND
  - SCL to A5
  - SDA to A4

4. Install the .zip libraries in the arduino_libraries folder using the Arduino IDE

5. Upload gui/gui.ino sketch to Arduino using the Arduino IDE.

6. Configure and activate virtual environment:

```
$ python3 -m venv venv
$ . venv/bin/activate
```

7. Install requirements

```
$ pip install -r requirements.txt
```

8. Run the GUI

```
$ python3 gui.py
```

If you have troubles with tkinter, you must configure your local Python installation for it. On mac, run

```
$ brew install python-tk
```
