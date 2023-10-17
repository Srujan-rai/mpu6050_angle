#include <Wire.h>
#include <MPU6050.h>
#include <I2Cdev.h>
#include <Math.h>

MPU6050 mpu;
int16_t ax, ay, az, gx, gy, gz;

float roll = 0.0;
float pitch = 0.0;
float yaw = 0.0;

void setup() {
  Wire.begin();
  mpu.initialize();
  Serial.begin(9600);
}

void loop() {
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);


  float gyroX = gx / 131.0; 
  float gyroY = gy / 131.0;
  float gyroZ = gz / 131.0;


  float accelX = atan2(ay, az) * 180.0 / M_PI;
  float accelY = atan2(-ax, az) * 180.0 / M_PI;


  pitch = 0.98 * (pitch + gyroX * 0.01) + 0.02 * accelX;
  roll = 0.98 * (roll + gyroY * 0.01) + 0.02 * accelY;

 
  yaw += gyroZ * 0.01;


  Serial.print("Pitch: ");
  Serial.print(pitch);
  Serial.print(" Roll: ");
  Serial.print(roll);
  Serial.print(" Yaw: ");
  Serial.println(yaw);

  delay(10); 
}
