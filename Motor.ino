// ------------------ Pin Definitions ------------------
//#define TRIG0 2//
//#define ECHO0 4 // ยังไม่ใช้งาน

#define TRIG1 32 // Sensor ชั้นที่ 1
#define ECHO1 33

#define TRIG2 12// Sensor ชั้นที่ 2
#define ECHO2 13

#define TRIG3 2 // Sensor ชั้นที่ 
#define ECHO3 4

// ------------------ Global Variables ------------------
int stats1 = 0; // ชั้นที่ 2
int stats2 = 0; // ชั้นที่ 1
int stats3 = 0; // ชั้นที่ 3

// ------------------ Read Ultrasonic Distance ------------------
long readUltrasonicDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // Timeout after 30ms
  long distance = duration * 0.034 / 2; // Convert to cm
  return distance;
}

// ------------------ Setup ------------------
void setup() {
  Serial.begin(1200);
  delay(1000);
  Serial.println("start");

  pinMode(TRIG1, OUTPUT);
  pinMode(ECHO1, INPUT);

  pinMode(TRIG2, OUTPUT);
  pinMode(ECHO2, INPUT);

  pinMode(TRIG3, OUTPUT);
  pinMode(ECHO3, INPUT);
}

// ------------------ Main Loop ------------------
void loop() {
  long distance1 = readUltrasonicDistance(TRIG1, ECHO1); // ชั้นที่ 2
  long distance2 = readUltrasonicDistance(TRIG2, ECHO2); // ชั้นที่ 3
  long distance3 = readUltrasonicDistance(TRIG3, ECHO3); // ชั้นที่ 1
   Serial.println(distance1);
   Serial.println(distance2);
   Serial.println(distance3);
  // -------- ชั้นที่ 1 --------
  if (distance1 <= 20) {
    if (stats1 == 0) {
      Serial.println("1 off");
      stats1 = 1;
    }
  } else {
    if (stats1 == 1) {
      Serial.println("1 on");
      stats1 = 0;
    }
  }

  // -------- ชั้นที่ 2 --------
  if (distance2 <= 20) {
    if (stats3 == 0) {
      Serial.println("2 off");
      stats3 = 1;
    }
  } else {
    if (stats3 == 1) {
      Serial.println("2 on");
      stats3 = 0;
    }
  }

  // -------- ข้างหน้า -------
  if (distance3 <= 20) {
    if (stats2 == 0) {
      Serial.println("3 off");
      stats2 = 1;
    }
  } else {
    if (stats2 == 1) {
      Serial.println("3 on");
      stats2 = 0;
    }
  }
 
  delay(1000); // หน่วงเวลา 1 วินาที
}