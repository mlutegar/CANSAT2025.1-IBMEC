#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 8);
const byte address[6] = "00001";

// Define os atrasos para cada rodada em milissegundos
const unsigned long delays[] = {1, 10, 100, 200, 300, 400, 500, 600, 700, 800};
const int NUM_ROUNDS = 10;
const int NUM_MESSAGES = 1000;

// Variáveis para controlar o estado do programa
int currentRound = 0;
int currentMessage = 0;
unsigned long previousMillis = 0;

char* gerarString(int qtd) {
  // Alocação dinâmica de memória para a string
  // +1 para o caractere nulo no final da string
  static char string[100]; // Buffer estático com tamanho máximo de 100

  // Garantir que não exceda o buffer
  if (qtd > 99) {
    qtd = 99; // Limita a 99 para deixar espaço para o '\0'
  }
  
  // Preenche a string com caracteres
  for (int i = 0; i < qtd; i++) {
    // Gera caracteres aleatórios ou pode personalizar aqui
    // Usando letras minúsculas como exemplo
    string[i] = 'a' + (i % 26); // Alternativa: 'a' + random(26);
  }
  
  // Adiciona o caractere nulo ao final da string
  string[qtd] = '\0';
  
  return string;
}

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  
  // Inicia a primeira rodada
  Serial.println("\n--- Iniciando Rodada 1 com delay de " + String(delays[0]) + "ms ---");
  previousMillis = millis();
}

void loop() {
	unsigned long currentMillis = millis();
	
	// Verifica se é hora de enviar uma nova mensagem
  if (currentMillis - previousMillis >= delays[currentRound]) {
    previousMillis = currentMillis;
    
    // Preparar a mensagem
    currentMessage++;
	String numeroMensagem = "#" + String(currentMessage);
	
	char* outraString = gerarString(1000);
	  String stringArduino = String(outraString); // Converte char* para String do Arduino
	  String messageContent = stringArduino;
	  int messageSize = messageContent.length() + 1;
	
	    
	char message[50];
    messageContent.toCharArray(message, sizeof(message));
	radio.write(&message, sizeof(message));
	
	Serial.print(numeroMensagem);
    Serial.print(" - ");
    Serial.print(messageSize);
    Serial.println(" bytes");
	
	    // Verificar se terminou o número de mensagens para essa rodada
    if (currentMessage >= NUM_MESSAGES) {
      currentRound++;
      currentMessage = 0;
      
      if (currentRound < NUM_ROUNDS) {
        // Iniciar próxima rodada
        Serial.println("\n--- Iniciando Rodada " + String(currentRound + 1) + 
                     " com delay de " + String(delays[currentRound]) + "ms ---");
      } else {
        // Finalizar todas as rodadas
        Serial.println("\n--- Todas as rodadas foram concluídas ---");
        Serial.println("Programa finalizado.");
        while (1) {
          // Loop infinito para parar a execução
          delay(1000);
        }
      }
	}
}}

