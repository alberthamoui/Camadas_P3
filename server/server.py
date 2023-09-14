from enlace import *
import time
import numpy as np

# serialName = "COM3"
# serialName = "COM7"
serialName = "COM6"

recebidos = []
comeco = b'\x0a'
final = b'\x0f'


def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        
    
        com1.enable()
        print("Abriu a comunicação")
        
        # Recebendo o Byte de inicio
        print("esperando 1 byte de inicio")
        tamanho, nRx = com1.getData(1)

        com1.rx.clearBuffer()
        time.sleep(.1)

        head_inicio = b'\x00\x00\x00\x00' + b'\x00\x00\xBB\x00' + b'\xBB\x00\x00\x00'
        eop_inicio = b'\x00\x00\xBB'
        handshake = head_inicio + eop_inicio

        # Byte de inicio
        time.sleep(0.2)
        com1.sendData(handshake)
        time.sleep(2)

        contador = 0
        bandeira = True

        while bandeira:
            bufferLen = com1.rx.getBufferLen()
            numero, _ = com1.getData(bufferLen)
            com1.rx.clearBuffer()
            time.sleep(1)
            if len(numero) != 0:
                print("recebeu {}".format(numero))
                if numero != comeco and numero != final:
                    recebidos.append(numero)
                    contador+=1
            if numero == final:
                bandeira = False

        print("recebidos{}\n\n".format(recebidos))
        print("recebeu {} bytes".format(contador))

        contadorBytes = contador.to_bytes(1, byteorder='little')
        # time.sleep(6)
        com1.sendData(contadorBytes)
        print("enviou")












        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
    print(recebidos)
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()