#include <pimoroniTrackball.h>  //From https://github.com/ncmreynolds/pimoroniTrackball
#include <Wire.h> 
#include <ITG3200.h>
#include <ADXL345.h> 

int ADXL345 = 0x53; // The ADXL345 sensor I2C address

ITG3200 gyro = ITG3200();
float  gx,gy,gz;
float  gx_rate, gy_rate, gz_rate;

float goffsetX, goffsetY, goffsetZ;

float X_out, Y_out, Z_out;  // Outputs



void setup() {
  Serial.begin(9600);
  while (!Serial);
  Wire.begin();       //Initialise I2C
  Wire.beginTransmission(ADXL345); // Start communicating with the device
  Wire.write(0x2D); // Access/ talk to POWER_CTL Register - 0x2D

  // Enable measurement
  Wire.write(8); // Bit D3 High for measuring enable (8dec -> 0000 1000 binary)
  Wire.endTransmission();

  for (int i = 0; i <= 200; i++) {
    gyro.readGyro(&gx,&gy,&gz); 
    if (i == 0) {
      goffsetX = gx;
      goffsetY = gy;
      goffsetZ = gz;
    }
    if (i > 1) {
      goffsetX = (gx + goffsetX) / 2;
      goffsetY = (gy + goffsetY) / 2;
      goffsetZ = (gz + goffsetZ) / 2;
    }
  }

  delay(1000);
  gyro.init(ITG3200_ADDR_AD0_LOW); 
  // //Off-set Calibration
  // //X-axis
  // Wire.beginTransmission(ADXL345);
  // Wire.write(0x1E);
  // Wire.write(1);
  // Wire.endTransmission();
  // delay(10);
  // //Y-axis
  // Wire.beginTransmission(ADXL345);
  // Wire.write(0x1F);
  // Wire.write(-2);
  // Wire.endTransmission();
  // delay(10);

  // //Z-axis
  // Wire.beginTransmission(ADXL345);
  // Wire.write(0x20);
  // Wire.write(-9);
  // Wire.endTransmission();
  // delay(10);

  trackball.begin();  //Initialise the trackball
  trackball.setBlue(255);
}

void loop() {
  Wire.beginTransmission(ADXL345);
  Wire.write(0x32); // Start with register 0x32 (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL345, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
  X_out = ( Wire.read() | Wire.read() << 8); // X-axis value
  X_out = X_out / 256; //For a range of +-2g, we need to divide the raw values by 256, according to the datasheet
  Y_out = ( Wire.read() | Wire.read() << 8); // Y-axis value
  Y_out = Y_out / 256;
  Z_out = ( Wire.read() | Wire.read() << 8); // Z-axis value
  Z_out = Z_out / 256;
  Serial.print(X_out);
  Serial.print(',');
  Serial.print(Y_out);
  Serial.print(',');
  Serial.print(Z_out);
  Serial.print(',');

  gyro.readGyro(&gx,&gy,&gz); 
  Serial.print(gx);
  Serial.print(',');
  Serial.print(gy);
  Serial.print(',');
  Serial.print(gz);
  Serial.print(',');

  if (trackball.changed()) {
    Serial.print(trackball.right() - trackball.left());
    Serial.print(',');
    Serial.print(trackball.up() - trackball.down());
    Serial.print(',');
    Serial.print(trackball.click());
    Serial.print(',');
    Serial.print(trackball.release());
  } else {
    Serial.print("0,0,0,0");
  }
  Serial.println();
  delay(50);
  // Serial.println();
  // Calculate Roll and Pitch (rotation around X-axis, rotation around Y-axis)
  // roll = atan(Y_out / sqrt(pow(X_out, 2) + pow(Z_out, 2))) * 180 / PI;
  // pitch = atan(-1 * X_out / sqrt(pow(Y_out, 2) + pow(Z_out, 2))) * 180 / PI;

  // Low-pass filter
  // rollF = 0.94 * rollF + 0.06 * roll;
  // pitchF = 0.94 * pitchF + 0.06 * pitch;

  // Serial.print(rollF);
  // Serial.print("/");
  // Serial.println(pitchF);
}

