void MPU6050_setup(){
  Wire.begin();
  delay(1);
  check_MPU();
  Serial.println("MPU-6050 6-Axis");
  regWrite(0x6B, 0xC0);regWrite(0x6C, 0x00);delay(10);
  regWrite(0x6B, 0x00);regWrite(0x6D, 0x70);regWrite(0x6E, 0x06);
  temp = regRead(0x6F);
  Serial.print("Bank 1, Reg 6 = ");
  Serial.println(temp);
  regWrite(0x6D, 0x00);
  temp = regRead(0x00);
  Serial.println(temp);
  Serial.println(temp);
  temp = regRead(0x01);
  Serial.println(temp);
  temp = regRead(0x02);
  Serial.println(temp);
  temp = regRead(0x6A);
  Serial.println(temp);
  regWrite(0x37, 0x32);
  temp = regRead(0x6B);
  Serial.println(temp);
  delay(5);
  mem_init();
  delay(20);

  bank_sel(0x00);
  regWrite(0x6E, 0x60);
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6F);
  Wire.write(0x04); Wire.write(0x00); Wire.write(0x00); Wire.write(0x00);
  Wire.endTransmission();
  bank_sel(1);
  regWrite(0x6E, 0x62);
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6F);
  Wire.endTransmission();
  Wire.beginTransmission(MPU_ADDR);
  Wire.requestFrom(MPU_ADDR,2);
  temp = Wire.read();
  temp = Wire.read();
  firstPacket = false;
  
}

void MPU6050_loop(){
    if(fifoReady()){
      getPacket();
      if(fifoCountL == 42){
        processQuat();
        writeQuat();
      }
    }
  }
