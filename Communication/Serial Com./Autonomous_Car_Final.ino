#include <Wire.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#define MPU_ADDR 0x68
#define MEM_START_ADDR 0x6E
#define MEM_R_W 0x6F
#include <SoftwareSerial.h>

long lastRead = 0;
byte processed_packet[8];
byte readd_packet[50];
byte temp = 0;
byte fifoCountL = 0;
byte fifoCountL2 = 0;
byte packetCount = 0x00;
boolean longPacket = false;
boolean firstPacket = true;
float q[4];
float deg[3]; // Euler angles converted to degree angles
float hq[4]; // Home-quaternion
float a[4];
float b[4];
int first = 0;

//A partir daqui são variaveis de controle do carrinho
int ENA = 3; //PWM
int IN1 = 2;
int IN2 = 4;
int IN3 = 7;
int IN4 = 8;
int ENB = 5; //PWM
int EN_BT = 13; // Enable the Bluetooth module power supply
float sp = 0; //Setpoint
float actual_ang = 0;
float last_ang = 0;
int error = 0; // Error of the controller
double kp = 2.3; // Proportional Constant
double ki = 0.00005; // Integrative Constant
double kd = 10; // Derivative Constant
int cons = 80; // Lower Speed (Constant of the controller)
int x = 0; // Wheel 1 variable
int y = 0; // Wheel 2 variable
boolean reset_coord = false; // Request to new front of the car
boolean ok_coord = false; // Request to change the orientation of the car
float last_time = 0;
float actual_time = 0;
float dt;
float p = 0;
float i = 0;
float d = 0;
float pid = 0;

SoftwareSerial serial1(10, 11); // RX, TX

void setup(){
  
  Serial.begin(9600);
  //serial1.setTimeout(10); //When using serial.parseFloat, the default value of this function is 1000ms, wich makes the arduino takes too long to read the data from the bluetooth.
  serial1.begin(9600);
  MPU6050_setup();
  pinOutMode(ENA);
  pinOutMode(ENB);
  pinOutMode(IN1);
  pinOutMode(IN2);
  pinOutMode(IN3);
  pinOutMode(IN4);
  pinOutMode(EN_BT);
  digitalWrite(EN_BT, HIGH);
  while(first <= 400){ // If the car has a display screen, it is possible insert a bar from 0 to 100% showing the car initialization using this value
    MPU6050_loop();
  }
  Serial.println("Valendo");
} // End of the setup

void loop(){
  last_time = actual_time;
  actual_time = millis();
  MPU6050_loop();
   if (serial1.available()) { //Check the serial communication working
    //sp = serial1.parseFloat();
    sp = ((float) serial1.read()) - 100;
    Serial.print("Setpoint: "); Serial.println(sp);
    ok_coord = true;
    }
  last_ang = actual_ang;
  actual_ang = deg[0];
  error = sp - actual_ang;  
  if(error == 0 && ok_coord){
    sp = 0;
    reset_coord = true;
    ok_coord = false;
    }
  wheel_controller();
  mov_front(y,x);
  //Serial.print("Angle: "); Serial.println(deg[0]);
  //Serial.print("Setpoint: "); Serial.println(sp);
  /*Serial.print("Error: "); Serial.println(error);
  Serial.print("PID: "); Serial.println(pid);*/
  //Serial.print(x); Serial.print(" :X e Y: "); Serial.println(y); //Serial.println(y);
  //Serial.print("Angle: "); Serial.print(deg[0]);  Serial.print("  Setpoint: "); Serial.print(sp);  Serial.print("  Error: "); Serial.print(error);  Serial.print("  PID: "); Serial.print(pid);   Serial.print("  X:  "); Serial.print(x); Serial.print("  Y: "); Serial.println(y); //Serial.println(y);

}//End of the loop
