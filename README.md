# Projeto de Sistema Embarcado - Comunicação LORA (CANSAT 2025)

## Links
[Overleaf](https://www.overleaf.com/project/67d9fed686f30143346a00f5)

## Descrição do Projeto
Este projeto consiste na implementação de um sistema de comunicação sem fio utilizando a tecnologia LORA (Long Range), desenvolvido para a disciplina de Projeto de Sistema Embarcado. O objetivo principal é estabelecer uma comunicação eficiente entre um transmissor e um receptor, possibilitando a troca de dados a longa distância com baixo consumo de energia.

## Tecnologias Utilizadas
- Arduino
- Módulos LORA OSOYOO UART
- Software Arduino IDE
- Impressão 3D para o case dos dispositivos

## Implementação

### Comunicação LORA
Em nossa implementação, utilizamos módulos LORA OSOYOO UART para estabelecer a comunicação sem fio. Após alguns testes iniciais e ajustes, conseguimos com sucesso realizar a transmissão de dados entre o receptor e o transmissor na aula do dia 27/03/2025.

#### Código de Comunicação
O código abaixo foi implementado para estabelecer a comunicação entre os dispositivos:

```cpp
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); //TX, RX
// (Send and Receive)

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {

  if(Serial.available() > 0){//Read from serial monitor and send over OSOYOO UART LoRa wireless module
    String input = Serial.readString();
    mySerial.println(input);
  }

  if(mySerial.available() > 1){//Read from OSOYOO UART LoRa wireless module and send to serial monitor
    String input = mySerial.readString();
    Serial.println(input);
  }
  delay(20);
}
```

Este código utiliza a biblioteca SoftwareSerial para criar uma porta serial virtual, permitindo a comunicação entre o Arduino e o módulo LORA. O programa monitora constantemente duas entradas:
1. Dados recebidos pela porta serial do computador, que são enviados para o módulo LORA
2. Dados recebidos pelo módulo LORA, que são enviados para a porta serial do computador

### Materiais para Impressão 3D
Após pesquisa e análise, selecionamos o material PLA.

## Fotos e Vídeos do Projeto

### Testes de Comunicação (27/03/2025)

#### Receptor LORA
![Receptor LORA]("imgs/lorax receptor.jpg")
*Receptor LORA em funcionamento durante os testes*

#### Transmissor LORA
![Transmissor LORA](caminho/para/foto_transmissor.jpg)
*Transmissor LORA em funcionamento durante os testes*

### Vídeo de Demonstração
<video width="640" height="360" controls>
  <source src="caminho/para/video_demonstracao.mp4" type="video/mp4">
  Seu navegador não suporta o elemento de vídeo.
</video>
*Demonstração do sistema em funcionamento com transmissão de dados em tempo real*

### Material para Impressão 3D
![Material de Impressão 3D](caminho/para/foto_material.jpg)

[Link do .stl](https://www.thingiverse.com/thing:6189990)

*Material selecionado para impressão do case dos dispositivos*

## Progresso do Projeto

| Data | Atividade | Status |
|------|-----------|--------|
| 27/03/2025 | Testes de comunicação LORA | ✅ Concluído |
| 27/03/2025 | Seleção de material para impressão 3D | ✅ Concluído |
| 27/03/2025 | Documentação fotográfica e em vídeo | ✅ Concluído |
| Próxima aula | Início da impressão 3D do case | 🔄 Pendente |

## Equipe
- André C. Coelho
- Marceu V. A. Filho
- Michel L. D'orsi
- Rigel P. Fernandes
