from enlace import *
import time
import numpy as np
from PIL import Image
import io

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

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # MAIN
        payloads = []
        bandeira = True
        cont = 0
        while bandeira:
            bufferLen = com1.rx.getBufferLen()
            numero, _ = com1.getData(bufferLen)
            if numero != b'':
                #recebidos.ppend(numero)
                if len(numero)!=0:
                    cont +=1
                payload = numero
                com1.rx.clearBuffer()
                time.sleep(0.1)
                print(cont)
                if numero != b'':
                    payloads.append(payload)
                if cont==22:
                    print("ACABOU PORRA")
                    bandeira = False
        for i in payloads:
            if i == b'':
                payloads.remove(i)
        print(payloads)
        print(len(payloads))

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # IMAGEM
        print(1)
        image_data = b''.join(payloads)
        print(2)
        byte_stream = io.BytesIO(image_data)
        print(3)
        image = Image.open(byte_stream)
        print(4)
        image.save('final.jpeg')  # Save the image to a file
        print(5)

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
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