//FLAN with servo SEM 7.7.2025
#include <Servo.h>
Servo servo1;// SEM mechanism
unsigned long interval=200;
unsigned long duration=90;
#include <CapacitiveSensor.h>
CapacitiveSensor cs_1 = CapacitiveSensor(7,2);
CapacitiveSensor cs_2 = CapacitiveSensor(7,11);
long c1_thresh;
long c1;
int licks1;
int drinks1;
int licks2;
int drinks2;
bool spout1_primed=true;
bool spout1_finished=true;
unsigned long t_drink1;
unsigned long now;
long c2_thresh;
long c2;
int licks3;
int drinks3;
int licks4;
int drinks4;
bool spout2_primed=true;
bool spout2_finished=true;
unsigned long t_drink2;
const int threshold_increment=1500;
const int spout1_drink1=A0;
const int spout1_drink2=A1;
const int spout2_drink3=A2;
const int spout2_drink4=A3;
const int led=13;
const int food_select1=3;
const int food_select2=4;
const int servoPin1 = 9;// nano pwm 3 5 6 9 10 11
//door angles
const int CLOSE= 1;
const int OPEN= 20;
int pos_current = CLOSE; //initial position variables for servos
int pos_target = CLOSE;

char receivedChar;

void setup() {
  servo1.attach(servoPin1);
  Serial.begin(115200);//setup serial
  digitalWrite(led,HIGH);
  pinMode(food_select1,INPUT);
  pinMode(food_select2,INPUT);
  pinMode(led,OUTPUT);
  pinMode(spout1_drink1,OUTPUT);
  digitalWrite(spout1_drink1,LOW);
  digitalWrite(spout1_drink1,HIGH);
  t_drink1=millis()-interval;
  pinMode(spout1_drink2,OUTPUT);
  digitalWrite(spout1_drink2,LOW);
  digitalWrite(spout1_drink2,HIGH);
  pinMode(spout2_drink3,OUTPUT);
  digitalWrite(spout2_drink3,LOW);
  digitalWrite(spout2_drink3,HIGH);
  pinMode(spout2_drink4,OUTPUT);
  digitalWrite(spout2_drink4,LOW);
  digitalWrite(spout2_drink4,HIGH);
  delay(500);
  long c1 = cs_1.capacitiveSensor(100);
  c1_thresh=c1+threshold_increment;
  licks1=0;
  drinks1=0;
  licks2=0;
  drinks2=0;
  long c2 = cs_2.capacitiveSensor(100);
  c2_thresh=c2+threshold_increment;
  licks3=0;
  drinks3=0;
  licks4=0;
  drinks4=0;
  digitalWrite(led,LOW);
//  Serial.print("cs_threshold   ");//show value for trouble shooting if serial monitor is on
//  Serial.println(c1_thresh); 
//  Serial.println(c2_thresh);
}

void loop() 
{
  Exp();
}

void Exp() 
{
  now=millis();
  c1 = cs_1.capacitiveSensor(3);
//  Serial.println(c1);
  if (c1>c1_thresh)
  {
    digitalWrite(led,HIGH);
    if (spout1_primed)
    {
      digitalWrite(spout1_drink2,LOW);t_drink1=millis();drinks2++;spout1_primed=false;spout1_finished=false;
      digitalWrite(spout1_drink1,LOW);t_drink1=millis();drinks1++;spout1_primed=false;spout1_finished=false;
    }
  }
  else{digitalWrite(led,LOW);}
  if((!spout1_primed) && (!spout1_finished) && (t_drink1+duration<now)) {digitalWrite(spout1_drink1,HIGH);digitalWrite(spout1_drink2,HIGH);spout1_finished=true;}
  if((!spout1_primed) && (spout1_finished) && (t_drink1+interval<now)) {spout1_primed=true;}
  
  c2 = cs_2.capacitiveSensor(3);
//  Serial.println(c2);
  if (c2>c2_thresh)
  {
    digitalWrite(led,HIGH);
    if (spout2_primed)
    {
      digitalWrite(spout2_drink4,LOW);t_drink2=millis();drinks4++;spout2_primed=false;spout2_finished=false;
      digitalWrite(spout2_drink3,LOW);t_drink2=millis();drinks3++;spout2_primed=false;spout2_finished=false;
    }
  }
  else{digitalWrite(led,LOW);}
  if((!spout2_primed) && (!spout2_finished) && (t_drink2+duration<now)) {digitalWrite(spout2_drink3,HIGH);digitalWrite(spout2_drink4,HIGH);spout2_finished=true;}
  if((!spout2_primed) && (spout2_finished) && (t_drink2+interval<now)) {spout2_primed=true;}
}
//
