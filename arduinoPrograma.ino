int trigPin = 10;
int echoPin = 9;

long laikoTarpas;
int atstumas;
int pauze = 1000;

void setup() 
{
  Serial.begin(9600);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() 
{  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  laikoTarpas = pulseIn(echoPin, HIGH);
  atstumas = (laikoTarpas*0.034)/2;

  Serial.println(atstumas);

  delay(pauze);
}
