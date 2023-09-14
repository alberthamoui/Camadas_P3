from comandsClient import *
from enlace import *
import time
import numpy as np
import random
import binascii



# A SER FEITO
# - Fragmentar img
# - Enviar o numero do pacote e o numero total de pacotes
# - Verificar o numero do pacote (+1) e o EOP(tudo em bytes)
# - Server mandar o OK para o Client
#   - Proximo pacote
#   - ou pedir o reenvio do pacote
# - Ao acabar o Server deve agrupar tudo e confirmar o envio
#  

# EXTRA
# 5 segundos, envia pergunta (S/N)


# como fazer pra reconhecer comeco e final?
    # criar um negocio d bytes b'\x??' pra comeco e pra fim


#coloquei xfa como byte de espaco ja que o server vai receber tudo junto, n eh otimizado mas funciona
#ira ter byte de comeco e byte de final, pro server reconhecer (esta certo)

serialName = "COM4"
# serialName = "COM7"
# serialName = "COM6"


comeco = b'\x0a'
final = b'\x0f'


def main():
    try:
        contador = 0
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")


        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # head_inicio = bytes.fromhex("00 00 00 00"),bytes.fromhex("00 00 BB 00"),bytes.fromhex("BB 00 00 00")
        # eop_inicio = bytes.fromhex("00 00 BB")
        # handshake = head_inicio + eop_inicio

        # # Byte de inicio
        # time.sleep(.2)
        # com1.sendData(bytes.fromhex(handshake))
        # time.sleep(2)

        head_inicio = b'\x00\x00\x00\x00' + b'\x00\x00\xBB\x00' + b'\xBB\x00\x00\x00'
        eop_inicio = b'\x00\x00\xBB'
        handshake = head_inicio + eop_inicio

        # Byte de inicio
        time.sleep(0.2)
        com1.sendData(handshake)
        time.sleep(2)

        # Recebendo o Byte de inicio
        print("esperando 1 byte de resposta")
        tamanho, nRx = com1.getData(1)

        com1.rx.clearBuffer()
        time.sleep(.1)



        teste = "client\inicial.jpeg"
        # txBuffer = open(teste, 'rb').read()
        # pacotes = None # O QUE EH ISSO??
        # tamPacotes = len(txBuffer)
        # tamPacotesBytes = (tamPacotes).to_bytes(1, byteorder='big')
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        txBuffer = open(teste, 'rb').read()

        tamPacotes = len(txBuffer)
        tamPacotesBytes = tamPacotes.to_bytes(4, byteorder='big')  # Use 4 bytes para representar o tamanho total

        # Tamanho de cada pacote (50 bytes)
        tam_pacote = 50

        pacotes = []
        # Dividir os bytes da imagem em pacotes de 50 bytes
        for i in range(0, len(txBuffer), tam_pacote):
            pacote = txBuffer[i:i + tam_pacote]
            pacotes.append(pacote)


        hs = 0
        envio = 1
        ESTADO = hs
        
        timeout = time.time() + 5
        if len(tamanho) == 0 or time.time()>timeout:
            quest = input(str("Servidor inativo. Tentar novamente? s/n : "))
        
        tamanho_pacotes = len(pacotes)
        tamanho_pacotes_bytes = tamanho_pacotes.to_bytes(1, byteorder='big')  # Use 4 bytes para representar o tamanho
        print(tamPacotesBytes)

        print('aaaaaaaaaaaaaaaaaaaaaaa')
        ki = 0
        for pacote in range(len(pacotes)-1):
            envio = tamPacotesBytes + b'\x00\x00\xBB\x00' + b'\xBB\x00\x00\x00' + pacotes[pacote] + eop_inicio
            print(envio)
            time.sleep(0.2)
            com1.sendData(envio)
            time.sleep(2)
            ki+1
            print(ki)
    
        envio = tamPacotesBytes + b'\xAA\xAA\xAA\xAA' + b'\xBB\x00\x00\x00' + pacotes[-1] + eop_inicio
        time.sleep(0.2)
        com1.sendData(envio)
        time.sleep(2)




        # while ESTADO == hs:
        #     timeout = time.time() + 5
        #     if len(tamanho) == 0 or time.time()>timeout:
        #         quest = input(str("Servidor inativo. Tentar novamente? s/n : "))
        #         if quest == 's':
        #             com1.sendData(handshake)
        #             time.sleep(0.1)
        #             tamanho, nRx = com1.getData(1)
        #             print(tamanho==tamPacotesBytes)
        #         elif quest == 'n':
        #             print("Comunicação encerrada")
        #             com1.disable()

        #     elif tamanho == tamPacotesBytes and time.time()<timeout:
        #         print("Tamanho do arquivo recebido com sucesso")
        #         ESTADO = envio
        #         break

        # while ESTADO == envio:
        #     for pacote in range(len(pacotes)):
        #         print(pacote)
        #         # ENVIAR PACOTE
        #         com1.sendData(pacote)



        # # Byte de inicio
        # time.sleep(.2)
        # com1.sendData(handshake)
        # time.sleep(2)

        # # Recebendo o Byte de inicio
        # print("esperando 1 byte de resposta")
        # tamanho, nRx = com1.getData(1)

        # com1.rx.clearBuffer()
        # time.sleep(.1)
        



        # def checar():
        #     #“Servidor inativo. Tentar novamente? S/N”
        #     timeout = time.time() + 5
        #     #time.sleep(6)
        #     if len(tamanho) != 0 and time.time()<timeout:
        #         print('a')
        #     else:
        #         questao = input(str("Servidor inativo. Tentar novamente? S/N : " ))
        #         if questao == "N":
        #             # Encerra comunicação
        #             print("-------------------------")
        #             print("Comunicação encerrada")
        #             print("-------------------------")
        #             com1.disable()
        #         else:
        #             # Byte de inicio novamente
        #             time.sleep(.2)
        #             com1.sendData(b'\x00')
        #             time.sleep(1)



        
        # # Encerra comunicação
        # print("-------------------------")
        # print("Comunicação encerrada")
        # print("-------------------------")
        # com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()