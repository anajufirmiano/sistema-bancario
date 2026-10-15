# 🏦 Sistema Bancário em Python

Sistema bancário completo desenvolvido em Python com interface interativa no terminal. O projeto é composto por dois módulos principais: **Cadastro de Clientes** com integração a APIs externas e validação de documentos, e um simulador interativo de **Caixa Eletrônico**.

---

## 📌 Funcionalidades

### 1. Cadastro de Clientes Bancários (`cadastrobanco.py`)
- **Dados Pessoais:** Coleta e validação de nome completo, sexo, data de nascimento e e-mail.
- **Cálculo Exato de Idade:** Valida se a data de nascimento é válida (não permite datas futuras) e exige o cadastro de responsável legal para menores de 18 anos.
- **Validação de CPF:** Validação dos dígitos verificadores e formatação automática com máscara (`XXX.XXX.XXX-XX`) via biblioteca `validate-docbr`.
- **Renda e Estado Civil:** Coleta de dados socioeconômicos com tratamento para valores numéricos e decimais.
- **Integração com API ViaCEP:** Busca automática de endereço completo a partir do CEP informado, preenchendo rua, bairro, cidade e estado. O CEP é salvo com máscara (`XXXXX-XXX`) para preservar zeros à esquerda em planilhas.
- **Exportação para CSV:** Gravação automática dos clientes em `clientescadastrados.csv` utilizando codificação `utf-8-sig`, garantindo compatibilidade e acentuação correta no Microsoft Excel e Google Sheets.

### 2. Simulador de Caixa Eletrônico (`caixaeletronico.py`)
- **Autenticação Segura:** Entrada de senha com máscara de caracteres ocultos usando `pwinput`.
- **Seleção de Instituição Bancária:** Suporte a múltiplos bancos (Itaú, Santander, Inter, Mercado Pago e outros).
- **Validação de Agência e Conta:** Verificação de padrões bancários numéricos.
- **Operações Financeiras:** Consulta de saldo, saques, depósitos e emissão de comprovantes/extratos no terminal.

---

## 📁 Estrutura do Projeto

```text
sistema-bancario/
│
├── cadastrobanco.py          # Script de cadastro de novos clientes
├── caixaeletronico.py        # Script do simulador de caixa eletrônico
├── clientescadastrados.csv   # Base de dados em CSV dos clientes cadastrados
└── README.md                 # Documentação do projeto
```

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o **Python 3.8+** instalado em sua máquina.

### Instalação de Dependências
Instale os pacotes necessários via terminal:

```bash
pip install requests validate-docbr pwinput emoji
```

### Executando o Cadastro de Clientes
```bash
python cadastrobanco.py
```

### Executando o Caixa Eletrônico
```bash
python caixaeletronico.py
```

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/):** Linguagem base do projeto.
- **[ViaCEP API](https://viacep.com.br/):** Web service gratuito para consulta de CEPs brasileiros.
- **[validate-docbr](https://pypi.org/project/validate-docbr/):** Validação matemática oficial de documentos fiscais brasileiros (CPF).
- **[pwinput](https://pypi.org/project/pwinput/):** Captura segura de senhas no terminal com máscara de asteriscos.
- **[Requests](https://requests.readthedocs.io/):** Biblioteca para requisições HTTP REST.
- **CSV / UTF-8-SIG:** Persistência de dados compatível com planilhas e sistemas bancários legados.

---

## 👩‍💻 Autora

Desenvolvido por **[Ana Júlia Firmiano](https://github.com/anajufirmiano)**.
