import serial
import time

# Abre a porta serial (substitua 'COM5' pela porta que o seu Arduino está conectado)
# No Linux, pode ser algo como '/dev/ttyUSB0' ou '/dev/ttyACM0'
arduino = serial.Serial('COM5', 9600, timeout=1)

# Aguarda o Arduino iniciar
time.sleep(2)

# Abre o arquivo .txt para salvar os dados
with open('dados_arduino.txt', 'a') as file:
    print("Iniciando monitoramento da porta serial. Pressione Ctrl+C para sair.")
    
    try:
        while True:
            # Lê a linha de dados da porta serial
            data = arduino.readline().decode('utf-8').strip()

            # Se houver dados, adiciona timestamp e escreve no arquivo
            if data:
                # Obtém o tempo atual em microssegundos (como um número inteiro)
                # time.time() retorna segundos como float, multiplicamos por 1_000_000 para obter microssegundos
                microssegundos = int(time.time() * 1_000_000)
                
                # Formata a linha com timestamp em microssegundos
                linha_com_timestamp = f"{microssegundos},{data}"
                
                # Escreve no arquivo
                file.write(linha_com_timestamp + '\n')
                file.flush()  # Garante que os dados sejam gravados imediatamente
                
                # Mostra no console
                print(linha_com_timestamp)
                
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário.")
    finally:
        arduino.close()
        print("Porta serial fechada.")