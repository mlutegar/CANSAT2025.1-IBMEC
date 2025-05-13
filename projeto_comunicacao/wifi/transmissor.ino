#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 8);  // CE, CSN
const byte address[6] = "00001";  // Endereço do canal de comunicação

// Estrutura da mensagem
struct DataPacket {
  int packetNumber;
  int messageNumber;
};

// Variáveis para controlar o programa
int packetNumber = 0;
int totalMessages = 0;
int currentMessage = 0;
bool configReady = false;
unsigned long previousMillis = 0;
const unsigned long delayTime = 1;  // Delay de 1ms entre mensagens

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  
  Serial.println("Transmissor nRF24L01 iniciado!");
  Serial.println("Aguardando configuração...");
  
  getUserConfig();  // Obter configuração inicial do usuário
}

void getUserConfig() {
  Serial.println("\n--- CONFIGURAÇÃO DO PACOTE ---");
  
  // Solicitar número do pacote
  Serial.println("Digite o número do pacote:");
  while (!Serial.available()) {
    // Aguardar entrada do usuário
  }
  packetNumber = Serial.parseInt();
  Serial.print("Número do pacote configurado: ");
  Serial.println(packetNumber);
  Serial.flush();
  
  // Limpar buffer
  while (Serial.available()) {
    Serial.read();
  }
  
  // Solicitar quantidade de mensagens
  Serial.println("Digite quantas mensagens terá esse pacote:");
  while (!Serial.available()) {
    // Aguardar entrada do usuário
  }
  totalMessages = Serial.parseInt();
  Serial.print("Total de mensagens configurado: ");
  Serial.println(totalMessages);
  Serial.flush();
  
  // Limpar buffer
  while (Serial.available()) {
    Serial.read();
  }
  
  currentMessage = 0;  // Resetar contador de mensagens
  configReady = true;  // Configuração concluída
  
  Serial.println("\n--- INICIANDO TRANSMISSÃO ---");
  Serial.println("Pacote: " + String(packetNumber) + " | Total de mensagens: " + String(totalMessages));
  previousMillis = millis();  // Inicializar timer
}

void loop() {
  // Verifica se a configuração está pronta
  if (configReady) {
    unsigned long currentMillis = millis();
    
    // Verifica se é hora de enviar uma nova mensagem
    if (currentMillis - previousMillis >= delayTime && currentMessage < totalMessages) {
      previousMillis = currentMillis;
      
      // Preparar e enviar a mensagem
      currentMessage++;
      
      DataPacket dataPacket;
      dataPacket.packetNumber = packetNumber;
      dataPacket.messageNumber = currentMessage;

      // Obter o tempo em microssegundos
      unsigned long micro = micros();
      
      // Criar mensagem com o tempo em microssegundos incluído
      String messageContent = String(micro) + "," + String(dataPacket.packetNumber) + "," + String(dataPacket.messageNumber);
      
      char message[50];
      messageContent.toCharArray(message, sizeof(message));
      bool success = radio.write(&message, sizeof(message));
      
      // Exibir informações sobre a mensagem enviada
      Serial.print("Enviado - Pacote: ");
      Serial.print(dataPacket.packetNumber);
      Serial.print(" | Mensagem: ");
      Serial.print(dataPacket.messageNumber);
      Serial.print(" | Tempo: ");
      Serial.print(micro);
      Serial.print(" | Status: ");
      Serial.println(success ? "OK" : "Falha");
      
      // Verificar se todas as mensagens foram enviadas
      if (currentMessage >= totalMessages) {
        Serial.println("\n--- TRANSMISSÃO CONCLUÍDA ---");
        Serial.println("Pacote " + String(packetNumber) + " enviado com " + String(totalMessages) + " mensagens");
        
        // Perguntar se deseja enviar outro pacote
        Serial.println("\nDeseja enviar outro pacote? (S/N)");
        configReady = false;  // Aguardar nova configuração
        
        // Esperar resposta
        while (!Serial.available()) {
          // Aguardar entrada do usuário
        }
        
        char response = Serial.read();
        if (response == 'S' || response == 's') {
          // Limpar buffer
          while (Serial.available()) {
            Serial.read();
          }
          getUserConfig();  // Obter nova configuração
        } else {
          Serial.println("Programa finalizado. Reinicie o Arduino para enviar novos pacotes.");
          while (1) {
            // Loop infinito para parar a execução
            delay(1000);
          }
        }
      }
    }
  } else if (Serial.available()) {
    // Se houver dados disponíveis e não estiver configurado, iniciar nova configuração
    Serial.read();  // Limpar buffer
    getUserConfig();
  }
}
