# ==============================================================================
#            IMPORTAÇÃO DE BIBLIOTECAS (MÓDULOS EXTERNOS E INTERNOS)
# ==============================================================================
# csv: Permite criar, ler e gravar informações em arquivos de texto no formato CSV (planilhas).
import csv

# datetime: Usado para trabalhar com datas, horários e cálculos de idade.
from datetime import datetime

# Path: Forma moderna e segura de manipular caminhos de pastas e arquivos no computador.
from pathlib import Path

# sleep: Pausa a execução do programa por alguns segundos (útil para mensagens de alerta).
from time import sleep

# requests: Biblioteca usada para acessar a internet e consultar APIs externas (como a do ViaCEP).
import requests

# CPF: Ferramenta da biblioteca 'validate_docbr' que valida e formata CPFs matematicamente.
from validate_docbr import CPF
import random
import string

# ==============================================================================
#                  FUNÇÕES DE CONSULTA, TRATAMENTO E VALIDAÇÃO
# ==============================================================================

def consultar_cep(cep: str):
    '''
    Função responsável por consultar o CEP na internet via API do ViaCEP.
    
    O que ela faz:
    1. Remove traços, pontos ou espaços do CEP digitado, deixando apenas números.
    2. Valida se o CEP possui exatamente 8 dígitos.
    3. Conecta na API pública dos Correios (ViaCEP) via requisição HTTP GET.
    4. Converte a resposta recebida para o formato JSON (dicionário em Python).
    5. Formata o CEP com máscara (XXXXX-XXX), garantindo que o Excel/CSV não
       apague os zeros à esquerda (ex: 01001-000 em vez de 1001000).
    '''
    # filter(str.isdigit, cep): Filtra apenas os caracteres numéricos da string digitada
    cep_limpo = ''.join(filter(str.isdigit, cep))

    # Todo CEP brasileiro válido precisa ter exatamente 8 números
    if len(cep_limpo) != 8:
        print('Erro: O CEP deve conter exatamente 8 dígitos numéricos.')
        return None

    # Endereço da API do ViaCEP com o CEP do cliente
    url = f'https://viacep.com.br/ws/{cep_limpo}/json/'

    try:
        # requests.get(): Acessa a URL na internet; timeout=10 evita que o programa trave se a rede cair
        response = requests.get(url, timeout=10)
        dados = response.json()  # Transforma o retorno da internet em um dicionário Python

        # A API do ViaCEP retorna {"erro": "true"} caso o CEP não exista na base dos Correios
        if dados.get('erro'):
            print('CEP não encontrado na base dos Correios.')
            return None

        # Adiciona o hífen no CEP (ex: 01310-100) para garantir que seja interpretado como texto no CSV
        cep_formatado = f'{cep_limpo[:5]}-{cep_limpo[5:]}'

        # Retorna um dicionário com os campos organizados e limpos (.strip() remove espaços extras)
        return {
            'cep': cep_formatado,
            'rua': dados.get('logradouro', '').strip(),
            'bairro': dados.get('bairro', '').strip(),
            'cidade': dados.get('localidade', '').strip(),
            'uf': dados.get('uf', '').strip(),
        }
    except requests.exceptions.RequestException as e:
        # Captura erros de falta de internet, timeout ou problemas no servidor da API
        print(f'Erro de conexão com a API do ViaCEP: {e}')
        return None


def obter_endereco():
    '''
    Função que coordena todo o processo de endereço do cliente:
    - Pede o CEP e busca na API;
    - Se a API não encontrar a rua (cidades de CEP único), pede para o usuário digitar;
    - Solicita número e complemento da casa/apartamento;
    - Monta a linha de endereço completa e formatada.
    '''
    print('\n--- CADASTRO DE ENDEREÇO ---')
    while True:
        cep_digitado = input('Digite o CEP (ex: 01001-000 ou 01001000): ').strip()
        dados_endereco = consultar_cep(cep_digitado)

        # Se os dados foram retornados com sucesso pela API, sai do loop de CEP
        if dados_endereco:
            break

        # Se não deu certo, pergunta se o usuário quer tentar outro CEP ou preencher manualmente
        opcao = input('Deseja tentar outro CEP? (S/N): ').strip().upper()
        if opcao != 'S':
            # Caso a pessoa não tenha internet ou o CEP seja especial, permite preencher à mão
            cep_limpo = ''.join(filter(str.isdigit, cep_digitado))
            cep_formatado = f'{cep_limpo[:5]}-{cep_limpo[5:]}' if len(cep_limpo) == 8 else cep_digitado
            dados_endereco = {
                'cep': cep_formatado,
                'rua': input('Digite a rua/logradouro: ').strip(),
                'bairro': input('Digite o bairro: ').strip(),
                'cidade': input('Digite a cidade: ').strip(),
                'uf': input('Digite o Estado (UF): ').strip().upper(),
            }
            break

    # Em municípios pequenos com CEP único, a API não retorna a rua nem o bairro, então pedimos ao usuário:
    rua = dados_endereco['rua'] or input('Digite o nome da rua/logradouro: ').strip()
    bairro = dados_endereco['bairro'] or input('Digite o bairro: ').strip()
    cidade = dados_endereco['cidade']
    uf = dados_endereco['uf']

    # Mostra a localização encontrada
    print(f'Localizado: {rua} - {bairro}, {cidade}/{uf}')
    
    # Coleta os dados complementares do imóvel
    numero = input('Número da residência: ').strip()
    complemento = input('Complemento (Apto, Bloco, etc. - opcional): ').strip()

    # Formata o complemento somente se a pessoa tiver digitado algo
    comp_texto = f', {complemento}' if complemento else ''
    
    # Monta a frase final do endereço estruturado
    endereco_completo = f'{rua}, Nº {numero}{comp_texto} - {bairro}, {cidade} - {uf}'

    # Retorna o CEP formatado e o endereço completo para serem salvos
    return dados_endereco['cep'], endereco_completo


def salvar_no_csv(cliente: dict):
    '''
    Função responsável por gravar os dados do cliente no arquivo clientescadastrados.csv.
    
    Recursos importantes:
    - Path(__file__).resolve().parent: Garante que o CSV seja salvo na mesma pasta deste script Python.
    - encoding='utf-8-sig': Adiciona a marca UTF-8 (BOM) para que o Excel abra acentos (ex: São Paulo,
      Responsável, Órgão) perfeitamente sem caracteres corrompidos.
    - newline='': Evita que o Windows crie linhas em branco extras entre cada cadastro.
    - Cabeçalho automático: Escreve a linha de títulos apenas se o arquivo for novo ou estiver vazio.
    '''
    pasta_script = Path(__file__).resolve().parent
    arquivo_csv = pasta_script / 'clientescadastrados.csv'

    # Verifica se o arquivo precisa de cabeçalho:
    # Se ele não existir ou se não tiver nenhum texto real (ignora espaços, quebras de linha e o BOM invisível de 3 bytes do UTF-8)
    precisa_cabecalho = not arquivo_csv.exists() or not arquivo_csv.read_text(encoding='utf-8-sig').strip()

    # Nomes das colunas da tabela
    colunas = [
        'Conta',
        'Nome Completo',
        'Sexo',
        'Data de Nascimento',
        'Idade',
        'Responsável',
        'E-mail',
        'CPF',
        'Renda Mensal',
        'Profissão',
        'Estado Civil',
        'CEP',
        'Endereço',
    ]

    # Abre o arquivo em modo 'a' (append / acrescentar ao final)
    with open(arquivo_csv, mode='a', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.writer(arquivo)
        
        # Se for o primeiro cadastro, escreve a linha com os títulos das colunas
        if precisa_cabecalho:
            escritor.writerow(colunas)

        # Grava a linha contendo todas as informações do cliente cadastrado
        escritor.writerow([
            cliente['conta'],
            cliente['nome'],
            cliente['sexo'],
            cliente['nascimento'],
            cliente['idade'],
            cliente['responsavel'],
            cliente['email'],
            cliente['cpf'],
            '{:.2f}'.format(cliente['renda']),
            cliente['profissao'],
            cliente['estado_civil'],
            cliente['cep'],
            cliente['endereco'],
        ])
# ==============================================================================
#                           CRIAR NÚMERO DA CONTA
# ==============================================================================
def numero_conta():
    return "".join(random.choices(string.digits, k=10))

# ==============================================================================
#                    FLUXO PRINCIPAL DO PROGRAMA (MAIN)
# ==============================================================================

def main():
    '''
    Função principal que orquestra todo o fluxo do sistema bancário:
    apresentação visual, captura e validação de cada campo do cliente.
    '''
    print('=' * 50)
    print('           CADASTRO DE CLIENTE BANCÁRIO')
    print('=' * 50)

    # --------------------------------------------------
    # 1.                NOME COMPLETO
    # --------------------------------------------------
    # .strip() remove espaços acidentais no início/fim; .title() deixa as iniciais maiúsculas
    while True:
        nome_completo = input('\nNome Completo: ').strip().title()
        if nome_completo:
            break
        else:
            print('O nome não pode ficar em branco.')

    # --------------------------------------------------
    # 2.                   SEXO
    # --------------------------------------------------
    # Usamos um dicionário para mapear o número digitado para o texto por extenso
    opcoes_sexo = {'1': 'Feminino', '2': 'Masculino'}
    while True:
        opcao = input('\nSexo:\n1. Feminino\n2. Masculino\nOpção: ').strip()
        if opcao in opcoes_sexo:
            sexo = opcoes_sexo[opcao]
            break
        else:
            print('Opção inválida! Digite apenas 1 ou 2.')
        sleep(1)

    # --------------------------------------------------
    # 3.    DATA DE NASCIMENTO E CÁLCULO DE IDADE
    # --------------------------------------------------
    while True:
        nascimento = input('\nData de nascimento (DD/MM/AAAA): ').strip()
        try:
            # datetime.strptime: Converte o texto no formato dia/mês/ano em um objeto de data real
            nascimento_formatado = datetime.strptime(nascimento, '%d/%m/%Y')
            hoje = datetime.today()

            # Impede datas inválidas futuras (ninguém nasceu depois de hoje)
            if nascimento_formatado > hoje:
                print('A data de nascimento não pode ser no futuro.')
                continue

            # Cálculo exato de idade levando em consideração se o aniversário já ocorreu este ano
            # A comparação de tuplas ((hoje.month, hoje.day) < (nasc.month, nasc.day)) retorna True (1)
            # caso o aniversário ainda não tenha chegado, subtraindo 1 da diferença de anos.
            idade = (
                hoje.year
                - nascimento_formatado.year
                - ((hoje.month, hoje.day) < (nascimento_formatado.month, nascimento_formatado.day))
            )
            break
        except ValueError:
            print('Digite uma data válida no formato DD/MM/AAAA (ex: 15/08/2000).')

    # --------------------------------------------------
    # TRATAMENTO DO RESPONSÁVEL LEGAL (SE MENOR DE IDADE)
    # --------------------------------------------------
    responsavel = 'N/A'
    if idade <= 17:
        print(f'\nCliente menor de idade ({idade} anos).')
        while True:
            responsavel = input('Nome do responsável legal: ').strip().title()
            if responsavel:
                break
            else:
                print('O nome do responsável é obrigatório para menores de 18 anos.')

    # --------------------------------------------------
    # 4.                   E-MAIL
    # --------------------------------------------------
    # Validação simples verificando a presença de '@' e '.' no e-mail
    while True:
        email = input('\nDigite seu melhor e-mail: ').strip()
        if '@' in email and '.' in email:
            break
        else:
            print('Digite um e-mail válido (ex: usuario@email.com).')

    # --------------------------------------------------
    # 5. CPF (COM VALIDAÇÃO MATEMÁTICA E MÁSCARA)
    # --------------------------------------------------
    validador = CPF()
    while True:
        cpf_digitado = input('\nDigite o CPF: ').strip()
        # validate(): Realiza o cálculo dos dois dígitos verificadores do CPF oficial
        if validador.validate(cpf_digitado):
            # mask(): Formata o CPF no padrão visual clássico (XXX.XXX.XXX-XX)
            cpf_formatado = validador.mask(cpf_digitado)
            break
        else:
            print('CPF inválido! Verifique os números e tente novamente.')

    # --------------------------------------------------
    # 6. RENDA MENSAL
    # --------------------------------------------------
    while True:
        try:
            renda_texto = input('\nRenda mensal (R$): ').replace('R$', '').strip()
            # No Brasil usamos vírgula para centavos (ex: 2500,50); no Python usa-se ponto (2500.50)
            if ',' in renda_texto:
                renda_texto = renda_texto.replace('.', '').replace(',', '.')
            renda = float(renda_texto)
            if renda >= 0:
                break
            else:
                print('A renda não pode ser negativa.')
        except ValueError:
            print('Por favor, digite um valor numérico válido (ex: 2500,00).')

    # --------------------------------------------------
    # 7. PROFISSÃO
    # --------------------------------------------------
    profissao = input('\nQual é a sua profissão? ').strip().title()

    # --------------------------------------------------
    # 8. ESTADO CIVIL
    # --------------------------------------------------
    estadocivil_opcao = {
        '1': 'Solteiro(a)',
        '2': 'Casado(a)',
        '3': 'Separado(a)',
        '4': 'Divorciado(a)',
        '5': 'Viúvo(a)',
    }
    while True:
        ec = input(
            '\nEstado Civil:\n1. Solteiro\n2. Casado\n3. Separado\n4. Divorciado\n5. Viúvo\nOpção: '
        ).strip()
        if ec in estadocivil_opcao:
            estado_civil = estadocivil_opcao[ec]
            break
        else:
            print('Opção inválida! Digite um número de 1 a 5.')
        sleep(1)

    # --------------------------------------------------
    # 9 e 10. CEP E ENDEREÇO (CHAMANDO A FUNÇÃO DEDICADA)
    # --------------------------------------------------
    cep, endereco = obter_endereco()

    # --------------------------------------------------
    # ESTRUTURAÇÃO DOS DADOS E SALVAMENTO
    # --------------------------------------------------
    # Agrupamos todas as respostas coletadas em um dicionário organizado
    cliente = {
        'conta': numero_conta(),
        'nome': nome_completo,
        'sexo': sexo,
        'nascimento': nascimento,
        'idade': idade,
        'responsavel': responsavel,
        'email': email,
        'cpf': cpf_formatado,
        'renda': renda,
        'profissao': profissao,
        'estado_civil': estado_civil,
        'cep': cep,
        'endereco': endereco,
    }

    # Chama a função que grava o cliente no arquivo CSV
    salvar_no_csv(cliente)

    # Mensagem visual de conclusão com os dados cadastrados
    print('\n' + '=' * 50)
    print('CADASTRO REALIZADO COM SUCESSO!')
    print(f'Cliente: {nome_completo}')
    print(f'CPF: {cpf_formatado} | CEP: {cep}')
    print(f'Endereço: {endereco}')
    print('Os dados foram gravados em \'clientescadastrados.csv\'.')
    print('=' * 50)


# ==============================================================================
#                       PONTO DE ENTRADA DO PROGRAMA
# ==============================================================================
# if __name__ == '__main__': Garante que o código dentro dele só seja executado
# quando você rodar este arquivo diretamente (python cadastrobanco.py).
# Se outro arquivo importar este script, ele não começará a rodar sozinho.
if __name__ == '__main__':
    main()
