from comandsClient import *
from enlace import *
import time
import numpy as np


# como fazer pra reconhecer comeco e final?
    # criar um negocio d bytes b'\x??' pra comeco e pra fim


#coloquei xfa como byte de espaco ja que o server vai receber tudo junto, n eh otimizado mas funciona
#ira ter byte de comeco e byte de final, pro server reconhecer (esta certo)

serialName = "COM3"

comeco = b'\x0a'
final = b'\x0f'


def main():
    try:
        contador = 0
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")

        head_inicio = bytes.fromhex("00 00 00 00"),bytes.fromhex("00 00 BB 00"),bytes.fromhex("BB 00 00 00")
        eop_inicio = bytes.fromhex("00 00 BB")
        handshake = head_inicio + eop_inicio


        # Byte de inicio
        time.sleep(.2)
        com1.sendData(handshake)
        time.sleep(2)

        # Recebendo o Byte de inicio
        print("esperando 1 byte de resposta")
        tamanho, nRx = com1.getData(1)

        com1.rx.clearBuffer()
        time.sleep(.1)
        
        #“Servidor inativo. Tentar novamente? S/N”
        timeout = time.time() + 5
        #time.sleep(6)
        if len(tamanho) != 0 and time.time()<timeout:
            print('a')
        else:
            questao = input(str("Servidor inativo. Tentar novamente? S/N : " ))
            if questao == "N":
                # Encerra comunicação
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                com1.disable()
            else:
                # Byte de inicio novamente
                time.sleep(.2)
                com1.sendData(b'\x00')
                time.sleep(1)

        
        
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