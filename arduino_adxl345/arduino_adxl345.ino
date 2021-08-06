/*
    Arduino and ADXL345 Accelerometer Tutorial
     by Dejan, https://howtomechatronics.com
*/

#include <Wire.h>  // Wire library - used for I2C communication

int ADXL345 = 0x53; // The ADXL345 sensor I2C address

float X_out, Y_out, Z_out;  // Outputs

void setup() {
  Serial.begin(9600); // Initiate serial communication for printing the results on the Serial monitor
  Wire.begin(); // Initiate the Wire library
  // Set ADXL345 in measuring mode
  Wire.beginTransmission(ADXL345); // Start communicating with the device 
  Wire.write(0x2D); // Access/ talk to POWER_CTL Register - 0x2D
  
  //Calibração
  //X-axis
  Wire.beginTransmission(ADXL345);
  Wire.write(0x1E);  // X-axis offset register
  Wire.write(1);
  Wire.endTransmission();
  delay(10);
  //Y-axis
  Wire.beginTransmission(ADXL345);
  Wire.write(0x1F); // Y-axis offset register
  Wire.write(-1);
  Wire.endTransmission();
  delay(10);
  
  //Z-axis
  Wire.beginTransmission(ADXL345);
  Wire.write(0x20); // Z-axis offset register
  Wire.write(6);
  Wire.endTransmission();
  delay(10);
  
  // Enable measurement
  Wire.write(8); // (8dec -> 0000 1000 binary) Bit D3 High for measuring enable 
  Wire.endTransmission();
  delay(10);
}

void loop() {
  // === Read acceleromter data === //
  Wire.beginTransmission(ADXL345);
  Wire.write(0x32); // Start with register 0x32 (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL345, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
  X_out = ( Wire.read()| Wire.read() << 8); // X-axis value
  // 32 -> +-16g
  X_out = X_out/256; //For a range of +-4g, we need to divide the raw values by 128, according to the datasheet
  Y_out = ( Wire.read()| Wire.read() << 8); // Y-axis value
  Y_out = Y_out/256;
  Z_out = ( Wire.read()| Wire.read() << 8); // Z-axis value
  Z_out = Z_out/256;

  // Calibração: To solve this issue, we need to calibrate the accelerometer using the 3 offset calibration registers,
  // and here’s how we can do that. So, we need to position the sensor flat, and print the RAW values without dividing them by 256.
//  X_out = ( Wire.read()| Wire.read() << 8); // X-axis value
//  X_out = X_out; //x = 251; erro = 251 - 256 = -5 -> Xoffset = -Round(-5/4) = 1
//  Y_out = ( Wire.read()| Wire.read() << 8); // Y-axis value
//  Y_out = Y_out; // y = 258; erro = 258 - 256 = 2 -> Yoffset = -Round(2/4) = -1
//  Z_out = ( Wire.read()| Wire.read() << 8); // Z-axis value
//  Z_out = Z_out; // z = 234; erro = 234 - 256 = -22 -> Zoffset = -Round(-22/4) = 6

  Serial.print("X= ");
  Serial.print(X_out);
  Serial.print("   Y= ");
  Serial.print(Y_out);
  Serial.print("   Z= ");
  Serial.println(Z_out);
  delay(20);
}
