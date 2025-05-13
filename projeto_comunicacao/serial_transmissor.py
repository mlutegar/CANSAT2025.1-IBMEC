import serial
import time
import datetime

# Configuração da porta serial (substitua 'COM12' pela porta correta do seu Arduino)
# No Linux, pode ser algo como '/dev/ttyUSB0' ou '/dev/ttyACM0'
porta_serial = 'COM9'
taxa_baud = 9600


def enviar_configuracao_arduino():
    # Solicita ao usuário as configurações
    numero_pacote = input("Digite o número do pacote: ")
    total_mensagens = input("Digite quantas mensagens terá esse pacote: ")

    # Abre a conexão serial
    arduino = serial.Serial(porta_serial, taxa_baud, timeout=1)
    time.sleep(2)  # Aguarda o Arduino inicializar

    # Lê as mensagens iniciais do Arduino (aguardando configuração)
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"Arduino diz: {linha}")
        if "Digite o número do pacote:" in linha:
            break

    # Envia o número do pacote
    arduino.write((numero_pacote + '\n').encode())
    time.sleep(0.5)

    # Lê a confirmação
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"Arduino diz: {linha}")
        if "Digite quantas mensagens" in linha:
            break

    # Envia o total de mensagens
    arduino.write((total_mensagens + '\n').encode())
    time.sleep(0.5)

    # Continua monitorando e salvando os dados
    monitorar_arduino(arduino)


def monitorar_arduino(arduino):
    # Abre o arquivo .txt para salvar os dados
    with open('dados_arduino.txt', 'a') as file:
        print("Iniciando monitoramento da porta serial. Pressione Ctrl+C para sair.")

        try:
            while True:
                # Lê a linha de dados da porta serial
                data = arduino.readline().decode('utf-8').strip()

                # Se houver dados, adiciona timestamp e escreve no arquivo
                if data:
                    # Obtém o timestamp atual
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                    # Formata a linha com timestamp
                    linha_com_timestamp = f"[{timestamp}] {data}"

                    # Escreve no arquivo
                    file.write(linha_com_timestamp + '\n')
                    file.flush()  # Garante que os dados sejam gravados imediatamente

                    # Mostra no console
                    print(linha_com_timestamp)

                    # Verifica se é necessário enviar nova configuração
                    if "Deseja enviar outro pacote? (S/N)" in data:
                        resposta = input("Deseja enviar outro pacote? (S/N): ")
                        arduino.write((resposta + '\n').encode())

                        if resposta.upper() == 'S':
                            # Espera pelas novas solicitações de configuração
                            time.sleep(1)
                            # Reinicia o processo de configuração
                            while True:
                                linha = arduino.readline().decode('utf-8').strip()
                                if linha:
                                    print(f"Arduino diz: {linha}")
                                if "Digite o número do pacote:" in linha:
                                    break

                            # Pede novas configurações
                            numero_pacote = input("Digite o número do pacote: ")
                            arduino.write((numero_pacote + '\n').encode())
                            time.sleep(0.5)

                            while True:
                                linha = arduino.readline().decode('utf-8').strip()
                                if linha:
                                    print(f"Arduino diz: {linha}")
                                if "Digite quantas mensagens" in linha:
                                    break

                            total_mensagens = input("Digite quantas mensagens terá esse pacote: ")
                            arduino.write((total_mensagens + '\n').encode())
                            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nMonitoramento encerrado pelo usuário.")
        finally:
            arduino.close()
            print("Porta serial fechada.")


# Inicia o programa
if __name__ == "__main__":
    print(f"Conectando ao Arduino na porta {porta_serial}...")
    try:
        enviar_configuracao_arduino()
    except Exception as e:
        print(f"Erro ao comunicar com Arduino: {e}")
        print(f"Verifique se o Arduino está conectado na porta {porta_serial} e se o código está carregado.")
