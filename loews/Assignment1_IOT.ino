int light_intensity = 0;    // Variable stores the light intensity
int ldr_sensor = A0;        // LDR sensor connected on Analog input 
int led1 = 11;              // LED input
int buzz = 12;             // Buzzer variable input

void setup() {
    // baud speed Indicates rate of data transmission between board and comp via usb 
    pinMode(led1, OUTPUT);
    pinMode(buzz, OUTPUT); 
    Serial.begin(9600);
 
}

void loop() {
    // Get light intensity readings from Board
    light_intensity = analogRead(ldr_sensor);
    Serial.print("ldr sensor intensity value : ");
    Serial.print(light_intensity);

    if (light_intensity > 100) {       
        Serial.print("High intensity ");
        digitalWrite(led1, HIGH);
        digitalWrite(buzz, LOW); // Turn off the buzzer
    } else {
        Serial.print("Low Intensity ");
        digitalWrite(led1, LOW);
        digitalWrite(buzz, HIGH); // Turn on the buzzer
    }

    delay(1000);
}
