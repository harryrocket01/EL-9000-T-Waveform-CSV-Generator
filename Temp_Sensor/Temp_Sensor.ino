const int thermistorPin = A0;  // Analog pin connected to the thermistor

void setup() {
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  // Read temperature from thermistor
  float temperature = readTemperature();
  float voltage = (temperature/1023)*5;

  temperature = -30.25*log((10*voltage)/(5-voltage))+94.377;

  // Send temperature data over serial
  Serial.print(temperature);
  int clocktime=millis();      // time in milli seconds
  Serial.print(",");
  Serial.println  (clocktime);


  // Delay before next reading (adjust according to your needs)
  delay(100);  // Logging every minute
}

float readTemperature() {
  // Read analog value from thermistor
  int rawValue = analogRead(thermistorPin);

  float temperature = map(rawValue, 0, 1023, 0, 1023); // Example formula, replace with actual calculation

  return temperature;
} 


float convert() {
  // Read analog value from thermistor
  int rawValue = analogRead(thermistorPin);

  float temperature = map(rawValue, 0, 1023, 0, 1023); // Example formula, replace with actual calculation

  return temperature;
}
