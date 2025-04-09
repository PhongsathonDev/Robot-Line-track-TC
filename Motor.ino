// กำหนดขาเชื่อมต่อมอเตอร์ซ้ายหน้า
#define LEFT_FRONT_IN1  25
#define LEFT_FRONT_IN2  26
// กำหนดขาเชื่อมต่อมอเตอร์ซ้ายหลัง
#define LEFT_REAR_IN1   23
#define LEFT_REAR_IN2   22

// กำหนดขาเชื่อมต่อมอเตอร์ขวาหน้า
#define RIGHT_FRONT_IN1 27
#define RIGHT_FRONT_IN2 14

// กำหนดขาเชื่อมต่อมอเตอร์ขวาหลัง
#define RIGHT_REAR_IN1  19
#define RIGHT_REAR_IN2  18

// ------------------ Pin Definitions ------------------
#define TRIG0 21 // Sensor ชั้นที่ 3
#define ECHO0 5

#define TRIG1 32 // Sensor ชั้นที่ 1
#define ECHO1 33

#define TRIG2 12 // Sensor ชั้นที่ 2
#define ECHO2 13

#define TRIG3 2  // Sensor ข้างหน้า
#define ECHO3 4

// กำหนดค่าความเร็วของมอเตอร์
int highSpeed = 220;
int normalSpeed = 220;
int slowSpeed = 100;  // ความเร็วลดลงเมื่อเลี้ยว
String command = "";
bool Stop = false;
int stopwalk = 0;

// ------------------ Global Variables ------------------
int stats1 = 0; // ชั้นที่ 1
int stats2 = 0; // ชั้นที่ 2
int stats3 = 0; // ชั้นที่ 3
int stats4 = 0; // ข้างหน้า

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

// ฟังก์ชันให้หุ่นยนต์เดินหน้า
void moveForwardMid() {
  analogWrite(LEFT_FRONT_IN1, highSpeed);
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, highSpeed);
  analogWrite(LEFT_REAR_IN2, LOW);
  analogWrite(RIGHT_FRONT_IN1, highSpeed);
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, highSpeed);
  analogWrite(RIGHT_REAR_IN2, LOW);
}

// ฟังก์ชันให้หุ่นยนต์ถอยหลัง
void moveBackward() {
  analogWrite(LEFT_FRONT_IN1, LOW);
  analogWrite(LEFT_FRONT_IN2, highSpeed);
  analogWrite(LEFT_REAR_IN1, LOW);
  analogWrite(LEFT_REAR_IN2, highSpeed);
  analogWrite(RIGHT_FRONT_IN1, LOW);
  analogWrite(RIGHT_FRONT_IN2, highSpeed);
  analogWrite(RIGHT_REAR_IN1, LOW);
  analogWrite(RIGHT_REAR_IN2, highSpeed);
}
void turnLeftSoft() {
  analogWrite(LEFT_FRONT_IN1, 150);  // ลดความเร็วฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, 150);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, highSpeed);  // ความเร็วปกติฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, highSpeed);
  analogWrite(RIGHT_REAR_IN2, LOW);
}
// ฟังก์ชันให้หุ่นยนต์เลี้ยวซ้าย (ฝั่งซ้ายช้าลง)
void turnLeftMid() {
  analogWrite(LEFT_FRONT_IN1, 100);  // ลดความเร็วฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, 100);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, highSpeed);  // ความเร็วปกติฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, highSpeed);
  analogWrite(RIGHT_REAR_IN2, LOW);
}
void turnLeftHard() {
  analogWrite(LEFT_FRONT_IN1, 20);  // ลดความเร็วฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, 20);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, highSpeed);  // ความเร็วปกติฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, highSpeed);
  analogWrite(RIGHT_REAR_IN2, LOW);
}

void turnRightSoft() {
  analogWrite(LEFT_FRONT_IN1, highSpeed);  // ความเร็วปกติฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, highSpeed);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, 150);  // ลดความเร็วฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, 150);
  analogWrite(RIGHT_REAR_IN2, LOW);
}
// ฟังก์ชันให้หุ่นยนต์เลี้ยวขวา (ฝั่งขวาช้าลง)
void turnRightMid() {
  analogWrite(LEFT_FRONT_IN1, highSpeed);  // ความเร็วปกติฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, highSpeed);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, 100);  // ลดความเร็วฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, 100);
  analogWrite(RIGHT_REAR_IN2, LOW);
}
void turnRightHard() {
  analogWrite(LEFT_FRONT_IN1, highSpeed);  // ความเร็วปกติฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, highSpeed);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, 20);  // ลดความเร็วฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, 20);
  analogWrite(RIGHT_REAR_IN2, LOW);
}

// ฟังก์ชันหยุดมอเตอร์
void stopMotor() {
  analogWrite(LEFT_FRONT_IN1, LOW);
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, LOW);
  analogWrite(LEFT_REAR_IN2, LOW);
  analogWrite(RIGHT_FRONT_IN1, LOW);
  analogWrite(RIGHT_FRONT_IN2, LOW);
  analogWrite(RIGHT_REAR_IN1, LOW);
  analogWrite(RIGHT_REAR_IN2, LOW);
}

void spin() {
  analogWrite(LEFT_FRONT_IN1, 255);  // ความเร็วปกติฝั่งซ้าย
  analogWrite(LEFT_FRONT_IN2, LOW);
  analogWrite(LEFT_REAR_IN1, 255);
  analogWrite(LEFT_REAR_IN2, LOW);

  analogWrite(RIGHT_FRONT_IN1, LOW);  // ลดความเร็วฝั่งขวา
  analogWrite(RIGHT_FRONT_IN2, 255);
  analogWrite(RIGHT_REAR_IN1, LOW);
  analogWrite(RIGHT_REAR_IN2, 255);
  delay(3100);
  stopMotor();


}


void setup() {
  Serial.begin(115200);  // เปิด Serial ผ่าน
  pinMode(LEFT_FRONT_IN1, OUTPUT);
  pinMode(LEFT_FRONT_IN2, OUTPUT);
  pinMode(LEFT_REAR_IN1, OUTPUT);
  pinMode(LEFT_REAR_IN2, OUTPUT);
  pinMode(RIGHT_FRONT_IN1, OUTPUT);
  pinMode(RIGHT_FRONT_IN2, OUTPUT);
  pinMode(RIGHT_REAR_IN1, OUTPUT);
  pinMode(RIGHT_REAR_IN2, OUTPUT);

  Serial.println("start");
  Serial.println("1off");
  Serial.println("2off");
  Serial.println("3off");
  pinMode(TRIG0, OUTPUT); pinMode(ECHO0, INPUT); // ชั้นที่ 3
  pinMode(TRIG1, OUTPUT); pinMode(ECHO1, INPUT); // ชั้นที่ 1
  pinMode(TRIG2, OUTPUT); pinMode(ECHO2, INPUT); // ชั้นที่ 2
  pinMode(TRIG3, OUTPUT); pinMode(ECHO3, INPUT); // ข้างหน้า
}

void loop() {

  long distance1 = readUltrasonicDistance(TRIG1, ECHO1); // ชั้นที่ 1
  long distance2 = readUltrasonicDistance(TRIG2, ECHO2); // ชั้นที่ 2
  long distance3 = readUltrasonicDistance(TRIG0, ECHO0); // ชั้นที่ 3
  long distance4 = readUltrasonicDistance(TRIG3, ECHO3); // ข้างหน้า

  Serial.println(distance4);
  // -------- ชั้นที่ 1 --------
  if (distance1 <= 27) {
    if (stats1 == 0) {
      Serial.println("1off");
      stats1 = 1;
    }
  } else {
    if (stats1 == 1) {
      Serial.println("1on");
      stats1 = 0;
    }
  }

  // -------- ชั้นที่ 2 --------
  if (distance2 <= 27) {
    if (stats2 == 0) {
      Serial.println("2off");
      stats2 = 1;
    }
  } else {
    if (stats2 == 1) {
      Serial.println("2on");
      stats2 = 0;
    }
  }

  // -------- ชั้นที่ 3 --------
  if (distance3 <= 27) {
    if (stats3 == 0) {
      Serial.println("3off");
      stats3 = 1;
    }
  } else {
    if (stats3 == 1) {
      Serial.println("3on");
      stats3 = 0;
    }
  }

  // -------- ข้างหน้า --------
  if (distance4 <= 20) {
    if (stats4 == 0) {
      Serial.println("4stop");
      stats4 = 1;
    }
  } else {
    if (stats4 == 1) {
      Serial.println("4walk");
      stats4 = 0;
    }
  }
  if (distance4 <= 40 ) {
    stopwalk = 10;
    stopMotor();
  }

  if (distance4 > 40 ) {
    if (stopwalk != 0) {
      stopwalk = stopwalk - 1;
    }
  }

  if (stopwalk == 0 ) {
    if (Serial.available()) {
      String command = Serial.readStringUntil('\n');
      if (command == "forwardMid") {
        moveForwardMid();
        Serial.println("forwardMid");
      }
      else if (command == "stop") {
        stopMotor();
        Serial.println("stop");
      }
      else if (command == "leftSoft") {
        turnLeftSoft();
        Serial.println("leftSoft");
      }
      else if (command == "leftMid") {
        turnLeftMid();
        Serial.println("leftMid");
      }
      else if (command == "leftHard") {
        turnLeftHard();
        Serial.println("leftHard");
      }

      else if (command == "rightSoft") {
        turnRightSoft();
        Serial.println("rightSoft");
      }
      else if (command == "rightMid") {
        turnRightMid();
        Serial.println("RightMid");
      }
      else if (command == "RightHard") {
        turnRightHard();
        Serial.println("RightHard");
      }
      else if (command == "Spin") {
        spin();
        Serial.println("Spin");
      }
    }
  }
}