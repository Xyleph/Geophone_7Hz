
int pinA = A0;
int pinB = A2;
int pinC = A4;

char data[14];

int a,b,c = 0;

void setup() {
  Serial.begin(220000);
}

void loop() {
  a = analogRead(pinA);
  b = analogRead(pinB);
  c = analogRead(pinC);

  sprintf(data,"%d,%d,%d", a, b, c);

  Serial.println(data);
}
