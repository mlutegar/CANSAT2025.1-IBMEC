#include <SoftwareSerial.h>
SoftwareSerial lora(2,3); // RX, TX

void setup() {
  Serial.begin(9600);
  lora.begin(9600);
  Serial.println("Receptor LoRa pronto");
}

void loop() {
  if (lora.available()) {
    String line = lora.readStringUntil('\n');
    // espera formato "micros,pkt,msg,dist"
    int idx1 = line.indexOf(',');
    int idx2 = line.indexOf(',', idx1 + 1);
    int idx3 = line.indexOf(',', idx2 + 1);
    String micros = line.substring(0, idx1);
    String pkt    = line.substring(idx1+1, idx2);
    String msg    = line.substring(idx2+1, idx3);
    String dist   = line.substring(idx3+1);
    Serial.print(">> pkt#"); Serial.print(pkt);
    Serial.print(" msg#");    Serial.print(msg);
    Serial.print(" dist=");    Serial.print(dist);
    Serial.print("μs=");      Serial.println(micros);
  }
}
