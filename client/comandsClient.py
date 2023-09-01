from random import *


def sorteiaComando():
    comandos = [bytes.fromhex("00 00 00 00"),bytes.fromhex("00 00 BB 00"),bytes.fromhex("BB 00 00"),bytes.fromhex("00 BB 00"),bytes.fromhex("00 00 BB"),bytes.fromhex("00 AA"),bytes.fromhex("BB 00"),bytes.fromhex("00"),bytes.fromhex("BB")]
    txbuffer = []
    final = False
    tam = []
    n = randint(10,31)
    for i in range(n):
        escolha = choice(comandos)
        tam.append(len(escolha).to_bytes(1, byteorder='big'))
        txbuffer.append(escolha)
        tamn = int.from_bytes(tam[i], byteorder='big')
        #print(f'Comando {i+1}: {txbuffer[i]} ou {txbuffer[i].hex().upper()} // Tamanho: {tamn} ')

    return tam, txbuffer, n




# def sorteiaComando():
#     espaco = 'fa'
#     comeco = 'ac'
#     final = 'af'
#     contadorEspaco = 0

#     espaco = bytes.fromhex(espaco)
#     comeco = bytes.fromhex(comeco)
#     final = bytes.fromhex(final)

#     lista = []
#     comandos = [bytes.fromhex("00 00 00 00"),bytes.fromhex("00 00 BB 00"),bytes.fromhex("BB 00 00"),bytes.fromhex("00 BB 00"),bytes.fromhex("00 00 BB"),bytes.fromhex("00 AA"),bytes.fromhex("BB 00"),bytes.fromhex("00"),bytes.fromhex("BB")]
#     n = randint(10,31)
#     # lista.append(comeco)
#     for i in range(n):
#         lista.append(comandos[randint(0,8)])
#         # lista.append(espaco)
#         contadorEspaco += 1
#         print(f'Comando {i+1}: {lista[i]} ou {lista[i].hex().upper()} // Tamanho: {len(lista)} ')

#     # lista.append(final)

    
#     # return tamanho, txbuffer
#     return lista, len(lista), len(lista)-contadorEspaco-2, n

print(sorteiaComando())