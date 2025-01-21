<div align="justify">

## Descrição

Esse projeto tem o intuito de utilizar ferramentas near real-time (quase tempo real) na nuvem da AWS para fazer a ingestão de dados com uma frequência alta, por isso utilizaremos nesse projeto uma stack específica (por exemplo Firehose) e também soluções específicas para que possamos adaptar as ferramentas às necessidades do projeto.
O projeto é um pipeline de dados de coleta, armazenagem e tratamento do valor do preço de bitcoin. Dividiremos em algumas etapas, como descrevemos a seguir:
* Na extração utilizaremos a API da Coinbase para consultar os valores do bitcoin, uma vez que ela tem um tier de uso grátis com até 15 mil requisições por dia, o que será mais que suficiente para nosso projeto;
* Na parte de ingestão destes dados utilizaremos o AWS Firehose, que irá nos ajudar a fazer a ingestão dos dados que irão ser coletados a cada 1s para podermos armazená-los num bucket S3 onde armazenaremos os arquivos "raw" ou onde seria a camada bronze.
* Na parte de tratamento/trasformação, a cada entrada de arquivo no bucket S3 raw, o próprio bucket S3 raw irá disparar uma mensagem no AWS SQS para uma fila específica de entrada destes arquivos. Esta fila, ao entrar uma quantidade de mensagens (ou arquivos recebidos no S3 raw), irá acionar uma função Lambda que irá acessar as mensagens e tratar para poder identificar as keys e buckets dos arquivos referenciados nas mensagens e, com issso, realizará a cópia destes arquivos para um segundo bucket S3 de backup.
* Por fim, na parte de Analytics, todos os dados ingeridos estão disponibilizados e visíveis no AWS Athena;

Este projeto é parte da entrega do Tech Challenge da FIAP do curso de pós-graduação em Machine Learning Engineering, feito pelo grupo composto pelos seguintes integrantes:
* Janis Silva
* Tatiana Haddad
* Victor Santos

## Objetivos

Este projeto tinha como objetivo a utilização de ferramentas da nuvem AWS como o Firehose, SQS, Lambda, S3 e Athena. Os principais entregáveis eram os seguintes:
* Realização de webscrapping;
* Utilização do AWS Firehose para ingestão de dados;
* Utilização de filas no AWS SQS;
* Utilização de funções Lambda para ler eventos registrados no AWS SQS e realizar processamento serverless;
* Utilização de buckets S3 e configurações de gatilhos para automação;
* Fornecer visualizações dos dados ingeridos no AWS Athena.

## Diretórios do projeto

A estrutura deste projeto é bem simples:

- app - pasta principal da aplicação;
  - extract - pasta da aplicação separada para o contexto de extração de dados;
    - extract.py - arquivo que irá fazer as requisições à API da Coinbase e que contém a lógica de extração e armazenagem dos arquivos em parquet;
  - load - pasta da aplicação separada para o contexto de load na nuvem AWS;
    - FireHose_load.py - arquivo que irá fazer o load dos arquivos gerados na extração para a nuvem AWS através do Firehose;
    - lambda_function.py - arquivo da função lambda que foi registrada na AWS para processar as mensagens do AWS SQS;
  - main.py - arquivo que irá rodar a aplicação como um todo;

## Pré-requisitos

- Python version
> Python 3.11.9

## Setup de Ambiente

1. Realize o clone do repositório:
  > git clone https://github.com/VictorJSSantos/Bitcoin-Stream-ETL.git

2. Recomendado:: Crie o ambiente virtual: 
  > python -m venv venv

3. Ativando o ambiente virtual: 
No Windows:
  > venv\Scripts\activate
No Linux:
  > source venv/bin/activate

4. Configure o interpretador python no ambiente virtual:
Ctrl + Shift + P para abrir a paleta de comandos.
  > Digite Python: Select Interpreter e escolha o Python dentro da pasta venv.

5. Atualize o pip para garantir a instalação devida das dependências:
  > python -m pip install --upgrade pip

5. Instale as dependências:
  > pip install -r requirements.txt

</div>
