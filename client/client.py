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


        # Sacrifício
        time.sleep(.2)
        com1.sendData(b'\x00')
        time.sleep(1)

        tam, txBuffer, n_sorteado = sorteiaComando() 
        print("O array de bytes len de {}" .format(txBuffer))


        
        com1.sendData(np.asarray(comeco))  
        for i in range(len(txBuffer)):
            # com1.sendData(np.asarray(tam[i]))
            # time.sleep(0.5)
            # print(tam[i])
            # time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer[i]))
            time.sleep(1)
            #print(txBuffer[i])
        com1.sendData(np.asarray(final))
        #time.sleep(1)
        print("enviou {}".format(n_sorteado))
        #print('np.asarray(txBuffer)\n\n\n{}\n\n\n'.format(np.asarray(txBuffer)))


        # ERROS
        flagTimeOut = True
        timeout = time.time() + 5
        while time.time()<timeout:
            # print(timeout-time.time())
            if com1.rx.getBufferLen()>0:
                rxBuffer, _ = com1.getData(1)
                esperado = int.from_bytes(rxBuffer, byteorder='big')

                if esperado == n_sorteado:
                    print("recebeu {}, acabou a transmissão".format(esperado))
                    flagTimeOut = False
                    break
                else:
                    if esperado != n_sorteado:
                        print("ERRO: NAO RECEBEU O QUE ESPERAVA")
                        print("esperava {} e recebeu {}" .format(n_sorteado, esperado))
                        flagTimeOut = False

        if flagTimeOut:
            print("ERRO: PASSOU 5 SEGUNDO")






        # print("\n\n\n\n\n\n\nRECEBA tx:\n{}\n\nrx:\n{}\n\n" .format(txBuffer,rxBuffer))

        #print("recebeu {} bytes" .format(len(rxBuffer)))
        
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()