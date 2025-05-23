#include <SoftwareSerial.h>
SoftwareSerial lora(2,3); 

struct DataPacket {
  int packetNumber;
  int messageNumber;
};

// Valores fixos definidos
const int packetNumber = 1;
const int totalMessages = 1500;
const float distancia = 1.0;

int currentMessage = 0;
unsigned long previousMillis = 0;
const unsigned long delayTime = 10;  // Aumentado para 10ms entre mensagens

void setup() {
  Serial.begin(9600);
  lora.begin(9600);

  Serial.println("\n--- CONFIGURAÇÃO FIXA DO PACOTE ---");
  Serial.println("Pacote: " + String(packetNumber) +
               " | Total de mensagens: " + String(totalMessages) +
               " | Distância: " + String(distancia) + "m");

  Serial.println("\n--- INICIANDO TRANSMISSÃO ---");

  lora.print("CFG;");
  previousMillis = millis();  // Inicializar timer
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= delayTime && currentMessage < totalMessages) {
    previousMillis = currentMillis;

    currentMessage++;

    DataPacket dataPacket;
    dataPacket.packetNumber = packetNumber;
    dataPacket.messageNumber = currentMessage;
    unsigned long micro = micros();

    // Adicionar distância na mensagem
    String messageContent = String(micro) + "," +
                          String(dataPacket.packetNumber) + "," +
                          String(dataPacket.messageNumber) + "," +
                          String(distancia);

    lora.println(messageContent);
    lora.flush(); // Garantir que os dados foram enviados
    delay(1); // Pequeno delay adicional para estabilidade
    bool success = true; // assume OK (UART não devolve ack)

    Serial.print("Enviado - Pacote: ");
    Serial.print(dataPacket.packetNumber);
    Serial.print(" | Mensagem: ");
    Serial.print(dataPacket.messageNumber);
    Serial.print(" | Tempo: ");
    Serial.print(micro);
    Serial.print(" | Distância: ");
    Serial.print(distancia);
    Serial.print("m | Status: ");
    Serial.println(success ? "OK" : "Falha");

    // A cada 100 mensagens, dar uma pausa maior para estabilidade
    if (currentMessage % 100 == 0) {
      delay(50);
      Serial.println("--- Checkpoint: " + String(currentMessage) + " mensagens enviadas ---");
    }

    if (currentMessage >= totalMessages) {
      Serial.println("\n--- TRANSMISSÃO CONCLUÍDA ---");
      Serial.println("Pacote " + String(packetNumber) +
                   " enviado com " + String(totalMessages) +
                   " mensagens a " + String(distancia) + "m");

      Serial.println("\nTodas as mensagens foram enviadas. Programa finalizado.");

      // Loop infinito para parar o programa
      while (1) {
        delay(1000);
      }
    }
  }
}