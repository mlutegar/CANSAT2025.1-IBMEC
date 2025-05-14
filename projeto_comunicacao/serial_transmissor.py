import serial
import time
import datetime

# Configuração da porta serial
porta_serial = 'COM9'
taxa_baud = 9600


def enviar_configuracao_arduino():
    # Abre a conexão serial
    arduino = serial.Serial(porta_serial, taxa_baud, timeout=1)
    time.sleep(2)  # Aguarda o Arduino inicializar

    # Lê as mensagens iniciais do Arduino
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"Arduino diz: {linha}")
        if "Digite o número do pacote:" in linha:
            break

    # Solicita e envia as configurações
    numero_pacote = input("Digite o número do pacote: ")
    arduino.write((numero_pacote + '\n').encode())
    time.sleep(0.5)

    # Aguarda pedido de total de mensagens
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"Arduino diz: {linha}")
        if "Digite quantas mensagens" in linha:
            break

    total_mensagens = input("Digite quantas mensagens terá esse pacote: ")
    arduino.write((total_mensagens + '\n').encode())
    time.sleep(0.5)

    # Aguarda pedido de distância
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"Arduino diz: {linha}")
        if "Digite a distância" in linha:
            break

    distancia = input("Digite a distância em metros do receptor: ")
    arduino.write((distancia + '\n').encode())
    time.sleep(0.5)

    # Continua monitorando
    monitorar_arduino(arduino)


def monitorar_arduino(arduino):
    with open('dados_arduino.txt', 'a') as file:
        print("Monitoramento iniciado. Pressione Ctrl+C para sair.")
        try:
            while True:
                data = arduino.readline().decode('utf-8').strip()
                if data:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    linha_com_timestamp = f"[{timestamp}] {data}"
                    file.write(linha_com_timestamp + '\n')
                    file.flush()
                    print(linha_com_timestamp)

                    if "Deseja enviar outro pacote?" in data:
                        resposta = input("Deseja enviar outro pacote? (S/N): ").upper()
                        arduino.write((resposta + '\n').encode())

                        if resposta == 'S':
                            # Processo de reconfiguração
                            while True:
                                linha = arduino.readline().decode('utf-8').strip()
                                if linha:
                                    print(f"Arduino diz: {linha}")
                                if "Digite o número do pacote:" in linha:
                                    break

                            numero_pacote = input("Digite o novo número do pacote: ")
                            arduino.write((numero_pacote + '\n').encode())
                            time.sleep(0.5)

                            while True:
                                linha = arduino.readline().decode('utf-8').strip()
                                if linha:
                                    print(f"Arduino diz: {linha}")
                                if "Digite quantas mensagens" in linha:
                                    break

                            total_mensagens = input("Digite o novo total de mensagens: ")
                            arduino.write((total_mensagens + '\n').encode())
                            time.sleep(0.5)

                            while True:
                                linha = arduino.readline().decode('utf-8').strip()
                                if linha:
                                    print(f"Arduino diz: {linha}")
                                if "Digite a distância" in linha:
                                    break

                            distancia = input("Digite a nova distância em metros: ")
                            arduino.write((distancia + '\n').encode())
                            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nMonitoramento encerrado.")
        finally:
            arduino.close()


if __name__ == "__main__":
    print(f"Conectando ao Arduino em {porta_serial}...")
    try:
        enviar_configuracao_arduino()
    except Exception as e:
        print(f"Erro: {e}")
        print("Verifique a porta e a conexão do Arduino.")
