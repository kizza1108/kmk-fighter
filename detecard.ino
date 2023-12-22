const int trigPin = 3;
const int echoPin = 2;

unsigned long startTime = 0; 
boolean objectDetected = false;  // Flag to indicate if an object is detected

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration; 
  int distance;

  
  digitalWrite(trigPin, LOW);// the arduino sends a pulse and expects a return
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

 
  duration = pulseIn(echoPin, HIGH);  // Reads time the pulse took to get there and back

  
  distance = duration / 58;


  if (distance < 10 && !objectDetected) {
    startTime = millis();  // Record the time if and when the object is detected
    objectDetected = true;
  }

  
  if (objectDetected && distance > 10) {
    // actually prints the time in which the object crosses the sensor
    Serial.print("Object detected at: ");
    Serial.println(startTime);
    objectDetected = false;
  }
}


