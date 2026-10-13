# --------------------------- #
# SISTEMA DE CAIXA ELETRÔNICO #
# --------------------------- #

import random
import string
import emoji
from datetime import datetime
import time
import pwinput

print('---------------------------------------------------------------------------------')
print('                          BEM VINDO AO CAIXA ELETRÔNICO                          ')
print('---------------------------------------------------------------------------------')

time.sleep(1)

saldo = 5000.0 # --------- Saldo do Banco
senha = '123456' # -------- Senha

nome = str.upper(input('Por favor, digite seu nome completo: '))


# 1° WHILE (INDEPENDENTE) - Validação da Senha
def validar_senha(): # --------------------------- Cria um bloco de código reutilizável
    while True:
        s = pwinput.pwinput(prompt= 'Digite sua senha: ', mask='*').strip()
        if s == senha:
            return True # -------------------- Encerra a função e avisa o 'if' que a senha está certa
        else:
            print ('Senha incorreta. \nTente novamente.')


# 2° WHILE (INDEPENDENTE) - Validação do Banco

while True:
    banco = int(input('Selecione o banco desejado: \n1. Itaú \n2. Santander \n3. Inter \n4. Mercado Pago \n5. Outro \nOpção: '))
    if banco > 5:
        print('Digite um número de 1 a 5. \nTente novamente.')
    elif banco == 5:
        str(input('Nome do banco: '))
        break
    else:
        break

# 3° WHILE (INDEPENDENTE) - Validação da Agência

while True:
    agencia = input('Digite o código da agência: ')
    if len(agencia) == 4 and agencia.isdigit():
        break
    else: 
        print ('Erro')
        time.sleep(1)
        print ('Tente novamente.')

# 4° WHILE (INDEPENDENTE) - Validação da Conta

while True:
    conta = input('Digite o número da conta: ')
    if len(conta) == 5 and len(conta) < 11 and conta.isdigit():
        break
    else:
        print ('Erro')
        time.sleep(1)
        print ('Tente novamente.')

# --------------------- #
# AQUI TEMOS AS OPÇÕES: #
# --------------------- #

# 5° WHILE (PRINCIPAL) - Loop do Menu

while True:
    opções = int( input('Olá {} Selecine a opção desejada: \n1. Ver saldo \n2. Fazer depósito \n3. Fazer saque \n4. Sair \nOpção: ' .format(nome)))

    # VER SALDO

    if opções == 1:
        print ('Seu saldo é: R${}' .format(saldo))

    # FAZER DEPÓSITO

    elif opções == 2:
        banco = float(input('Selecione o valor do depósito: '))

        print ('Depósito realizado com sucesso!')
        agora = datetime.now() # -------------------------------------------------------------- AQUI REGISTRA A HORA E DATA EXATOS EM QUE FOI FEITO O DEPÓSITO
        datahora = agora.strftime('%d/%m/%Y às %H:%M:%S') # ----------------------------------- AQUI FORMATA PARA O PADRÃO BRASILEIRO DE HORA DE DATA

        # Gera o código ANTES de usar no comprovante
        caracteres = string.ascii_uppercase + string.digits
        codigo = "".join(random.choices(caracteres, k=5))

# 1° SUB-WHILE (ANINHADO) - Confirmação do Comprovante

        while True:
            comprovante = str(input('Deseja imprimir seu comprovante? '))
            if comprovante == 'sim':
                print ('Só um instante...')
                time.sleep(2)
                print ('----------- COMPROVANTE DE DEPÓSITO -----------')
                print ('Emitido em: {}' .format(datahora))
                print ('Por: {}' .format(nome))
                print ('Valor: R${:.2f}' .format(banco))
                print ('                                               ')
                print ('Código: {}' .format(codigo))
                print ('_______________________________________________')
                break
            elif comprovante == 'não' or comprovante == 'nao':
                print(emoji.emojize('Obrigado pela preferência! :smiling_face:'))
                exit()
            else:
                print('Responda apenas com sim ou não.')

    # FAZER SAQUE

    elif opções == 3:
        print(emoji.emojize('Notas disponíveis: | :money_with_wings: R$50 | :money_with_wings: R$100 | :money_with_wings: R$200 |'))
        agora2 = datetime.now() # -------------------------------------------------------------- AQUI REGISTRA A HORA E DATA EXATOS EM QUE FOI FEITO O SAQUE
        datahora2 = agora2.strftime('%d/%m/%Y às %H:%M:%S') # ----------------------------------- AQUI FORMATA PARA O PADRÃO BRASILEIRO DE HORA DE DATA

        # Gera o código ANTES de usar no comprovante
        caracteres = string.ascii_uppercase + string.digits
        codigo_s = "".join(random.choices(caracteres, k=5))

# 2° SUB-WHILE (ANINHADO) - Confirmação do Comprovante
        while True:
            saque = float(input('Valor do saque: '))

            # Trás a senha para a confirmação do Saque
            if validar_senha():

                print ('Só um instante...')
                time.sleep(2)
                print ('Saque realizado com sucesso!')
                comprovante2 = input('Deseja imprimir seu comprovante? ')
                if comprovante2 == 'sim':
                    print('Só um instante...')
                    time.sleep(2)
                    print ('----------- COMPROVANTE DE SAQUE -----------')
                    print ('Emitido em: {}' .format(datahora2))
                    print ('Por: {}' .format(nome))
                    print ('Valor: R${:.2f}' .format(saque))
                    print ('                                            ')
                    print ('Código: {}' .format(codigo_s))
                    print ('____________________________________________')
                    break
                elif comprovante2 == 'não' or comprovante2 == 'nao':
                    print (emoji.emojize('Obrigado pela preferência! :smiling_face:'))
                    exit()
                else:
                    print ('Responda apenas com sim ou  não.')
                    break
            else:
                print ('O valor mínimo para saque é de R$50,00. \nTente novamente.')

    #SAIR

    else: 
        print ('Encerrando sessão...')
        exit()

    # ----------------------------------- #
    # PERGUNTA ÚNICA PARA TODAS AS OPÇÕES #
    # ----------------------------------- #

    ação = int(input('\nDigite: \n1. Sair \n2. Voltar ao menu principal\nOpção: '))
    if ação == 1:
        break
    elif ação == 2:
        pass

# saber da quantia por notas, quando tirar um valor diminuir o valor total
# entrar na conta, mexer no saldo e etc