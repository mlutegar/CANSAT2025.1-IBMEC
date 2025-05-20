import serial
import time
import datetime
import pandas as pd

arduino = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)

header = ("Tempo total receptor,"
          "Tempo total emissor,"
          "Id do pacote,"
          "Id da mensagem,"
          "Distancia (m),"
          "Tempo zerado receptor,"
          "Tempo zerado emissor,"
          "Delta tempo,"
          "Velocidade (m/s)")

mensagens = 1500
distancia_input = 150

with open(f'data/tentativa1-{mensagens}n-{distancia_input}m.csv', 'a') as file:
    # Escreve o cabeçalho no arquivo
    file.write(header + '\n')

    print("Iniciando monitoramento da porta serial. Pressione Ctrl+C para sair.")

    # Variáveis para armazenar os primeiros valores para zerar os tempos
    primeiro_tempo_receptor = None
    primeiro_tempo_emissor = None

    try:
        while True:
            # Lê a linha de dados da porta serial
            data = arduino.readline().decode('utf-8').strip()

            # Se houver dados, processa e escreve no arquivo
            if data:
                try:
                    # Obtém o timestamp atual em microssegundos (tempo do receptor)
                    tempo_receptor = int(time.time() * 1000000)

                    # Decompõe os dados recebidos
                    dados = data.split(',')

                    if len(dados) >= 4:
                        tempo_emissor = int(dados[0])
                        id_pacote = int(dados[1])
                        id_mensagem = int(dados[2])
                        distancia = distancia_input

                        # Inicializa os valores de referência na primeira medição
                        if primeiro_tempo_receptor is None:
                            primeiro_tempo_receptor = tempo_receptor
                            primeiro_tempo_emissor = tempo_emissor

                        # Calcula os tempos zerados
                        tempo_zerado_receptor = tempo_receptor - primeiro_tempo_receptor
                        tempo_zerado_emissor = tempo_emissor - primeiro_tempo_emissor

                        # Calcula o delta de tempo (diferença entre os tempos zerados)
                        delta_tempo = tempo_zerado_receptor - tempo_zerado_emissor

                        # Calcula a velocidade (distância / delta_tempo)
                        # Convertendo delta_tempo de microssegundos para segundos
                        if delta_tempo > 0:
                            velocidade = distancia / (delta_tempo / 1000000)
                        else:
                            velocidade = 0

                        # Formata a linha completa com todos os dados calculados
                        linha_completa = f"{tempo_receptor},{tempo_emissor},{id_pacote},{id_mensagem},{distancia},{tempo_zerado_receptor},{tempo_zerado_emissor},{delta_tempo},{velocidade}"

                        # Obtém o timestamp para exibição
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        linha_com_timestamp = f"[{timestamp}] {linha_completa}"

                        # Escreve no arquivo
                        file.write(linha_completa + '\n')
                        file.flush()  # Garante que os dados sejam gravados imediatamente

                        # Mostra no console
                        print(linha_com_timestamp)

                except Exception as e:
                    print(f"Erro ao processar dados: {e}")
                    print(f"Dados recebidos: {data}")

    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário.")
    finally:
        arduino.close()
        print("Porta serial fechada.")

        # Analisa os dados coletados após encerrar a coleta
        try:
            print("\nAnalisando os dados coletados...")
            df = pd.read_csv('teste1-50m.txt')

            # Estatísticas básicas
            print("\nEstatísticas do tempo de transmissão:")
            print(f"Média do delta tempo: {df['Delta tempo'].mean():.2f} μs")
            print(f"Média da velocidade: {df['Velocidade (m/s)'].mean():.2f} m/s")
            print(f"Velocidade máxima: {df['Velocidade (m/s)'].max():.2f} m/s")
            print(f"Velocidade mínima: {df['Velocidade (m/s)'].min():.2f} m/s")

            # Você pode adicionar mais análises aqui conforme necessário

        except Exception as e:
            print(f"Não foi possível analisar os dados: {e}")