#include <Servo.h>

// Initialize servo objects for tilt and door control
Servo servo_tilt, servo_door;

// Define pin connections for tilt and door controls
int PIN_BNC_TILT = 3;               // Binary control pin for tilt
int PIN_OVERRIDE_TILT = 4;          // Override switch pin for tilt
int PIN_SERVO_TILT = 11;            // Servo motor control pin for tilt
int PIN_POT_TILT = A7;              // Analog potentiometer pin for tilt speed

int PIN_BNC_DOOR = 5;               // Binary control pin for door
int PIN_OVERRIDE_DOOR = 6;          // Override switch pin for door
int PIN_SERVO_DOOR = 12;            // Servo motor control pin for door
int PIN_POT_DOOR = A7;              // Analog potentiometer pin for door speed (shares pin with tilt potentiometer)

// Define tilt and door positions
int POS_TILT_LOW = 80, POS_TILT_HIGH = 140;    // Tilt range: low and high positions
int POS_DOOR_OPEN = 150, POS_DOOR_CLOSE = 30;  // Door range: open and close positions

// Define current position and state variables for tilt and door
int current_pos_tilt, current_pos_door;        // Tracks the current position of tilt and door
int current_state_tilt, current_state_door;    // Tracks the current state of tilt and door (high or low for tilt; open or close for door)

// Input readings and processed speed values
int bnc_tilt_in, override_tilt_in, pot_tilt_spd_raw, servo_tilt_spd;  // Tilt control-related variables
int bnc_door_in, override_door_in, pot_door_spd_raw, servo_door_spd;  // Door control-related variables



void setup()
{
  // Set pin modes for tilt and door input pins
  pinMode(PIN_BNC_TILT, INPUT);
  pinMode(PIN_OVERRIDE_TILT, INPUT_PULLUP);
  pinMode(PIN_POT_TILT, INPUT);
  
  pinMode(PIN_BNC_DOOR, INPUT);
  pinMode(PIN_OVERRIDE_DOOR, INPUT_PULLUP);
  pinMode(PIN_POT_DOOR, INPUT);
  
  // Attach and initialize tilt servo
  servo_tilt.attach(PIN_SERVO_TILT);    // Attach servo for tilt control
  servo_tilt.write(POS_TILT_HIGH);      // Set initial position to high
  current_pos_tilt = POS_TILT_HIGH;     // Store current position
  tiltStateTest();                      // Test and set tilt state

  // Attach and initialize door servo
  servo_door.attach(PIN_SERVO_DOOR);    // Attach servo for door control
  servo_door.write(POS_DOOR_CLOSE);     // Set initial position to closed
  current_pos_door = POS_DOOR_CLOSE;    // Store current position
  doorStateTest();                      // Test and set door state
  
  Serial.begin(9600);                   // Initialize serial communication for system output
}



void loop()
{
  // Read the inputs about the tilt and door controls
  bnc_tilt_in = digitalRead(PIN_BNC_TILT);
  override_tilt_in = !(digitalRead(PIN_OVERRIDE_TILT));  // '1' if override switch is ON. '0' normally.
  bnc_door_in = digitalRead(PIN_BNC_DOOR);
  override_door_in = !(digitalRead(PIN_OVERRIDE_DOOR));  // '1' if override switch is ON. '0' normally.
  
  // Execute routines to control tilt and door
  tiltRoutine();
  doorRoutine();
}

// Routine to manage tilt servo movement
void tiltRoutine()
{
  pot_tilt_spd_raw = analogRead(PIN_POT_TILT);              // Read tilt potentiometer for speed
  servo_tilt_spd = map(pot_tilt_spd_raw, 0, 1023, 80, 10);  // Map potentiometer to servo speed

  // Logic for handling tilt control based on override and binary control states
  if((override_tilt_in) && (!current_state_tilt))
  {
    tiltLow();
  }
  else if((override_tilt_in) && (current_state_tilt))
  {
    tiltHigh();
  }
  else if((!override_tilt_in) && (bnc_tilt_in))
  {
    tiltLow();
    tiltStateTest();
  }
  else if((!override_tilt_in) && (!bnc_tilt_in))
  {
    tiltHigh();
    tiltStateTest();
  }
}

// Move tilt servo to high position
void tiltHigh()
{
  if(current_pos_tilt < POS_TILT_HIGH)
  {
    current_pos_tilt++;     // Increment position until high position is reached
    servo_tilt.write(current_pos_tilt);
    delay(servo_tilt_spd);  // Delay based on speed setting
  }
}

// Move tilt servo to low position
void tiltLow()
{
  if(current_pos_tilt > POS_TILT_LOW)
  {
    current_pos_tilt--;     // Decrement position until low position is reached
    servo_tilt.write(current_pos_tilt);
    delay(servo_tilt_spd);  // Delay based on speed setting
  }
}

// Test and update tilt state based on current position
void tiltStateTest()
{
  if(current_pos_tilt == POS_TILT_HIGH)
  {
    current_state_tilt = 0; // Set state to high if at high position
  }
  else if(current_pos_tilt == POS_TILT_LOW)
  {
    current_state_tilt = 1; // Set state to low if at low position
  }
}

// Routine to manage door servo movement
void doorRoutine()
{
  pot_door_spd_raw = analogRead(PIN_POT_DOOR);              // Read door potentiometer for speed
  servo_door_spd = map(pot_door_spd_raw, 0, 1023, 80, 10);  // Map potentiometer to servo speed

  // Logic for handling door control based on override and binary control states
  if((override_door_in) && (!current_state_door))
  {
    doorOpen();
  }
  else if((override_door_in) && (current_state_door))
  {
    doorClose();
  }
  else if((!override_door_in) && (bnc_door_in))
  {
    doorOpen();
    doorStateTest();
  }
  else if((!override_door_in) && (!bnc_door_in))
  {
    doorClose();
    doorStateTest();
  }
}

// Move door servo to open position
void doorOpen()
{
  if(current_pos_door < POS_DOOR_OPEN)
  {
    current_pos_door++;     // Increment position until open position is reached
    servo_door.write(current_pos_door);
    delay(servo_door_spd);  // Delay based on speed setting
  }
}

// Move door servo to closed position
void doorClose()
{
  if(current_pos_door > POS_DOOR_CLOSE)
  {
    current_pos_door--;     // Decrement position until close position is reached
    servo_door.write(current_pos_door);
    delay(servo_door_spd);  // Delay based on speed setting
  }
}

// Test and update door state based on current position
void doorStateTest()
{
  if(current_pos_door == POS_DOOR_CLOSE)
  {
    current_state_door = 0; // Set state to closed if at close position
  }
  else if(current_pos_door == POS_DOOR_OPEN)
  {
    current_state_door = 1; // Set state to open if at open position
  }
}

// Debugging function to read digital pin value
void tempDebugD1(int pin_num) {
  int debug_val_D1 = digitalRead(pin_num);
  Serial.print("Digital@");
  Serial.print(pin_num);
  Serial.print("@");
  Serial.print(debug_val_D1);
  Serial.println();
}

// Debugging function to read analog pin value
void tempDebugA1(int pin_num) {
  int debug_val_A1 = analogRead(pin_num);
  Serial.print("Analog@");
  Serial.print(pin_num);
  Serial.print("@");
  Serial.print(debug_val_A1);
  Serial.println();
}
