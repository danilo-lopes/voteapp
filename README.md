# Voting App

Aplicação simples distribuída em containeres. Todos as suas camadas desenvolvidas em Python.

O objetivo desta foi desenvolver habildades no processamento, armazenamento e entrega de dados, englobando serviços de
fila, banco de dados e serviços de WEB/API.

## Setup

[docker](https://docs.docker.com/get-docker/)

[docker-composer](https://docs.docker.com/compose/install/)

**Criar duas Docker network do tipo Overlay, uma chamada backend e a outra frontend.**

`docker network create -d overlay backend`

`docker network create -d overlay frontend`

**Nota:** Necessário iniciar o swarm no nó em que vai subir os containeres

Variaveis de ambiente:

```
export AWS_ACCESS_KEY='BAR'
export AWS_SECRET_KEY='FOO'
export AWS_REGION='FOO'
export MYSQL_HOST='BAR'
export MYSQL_USER='FOO'
export MYSQL_DB='voteapp'
export MYSQL_PASSWORD='foo'
```

> Não mude o nome da database.

---

```
docker-compose -f docker-compose.yml up
```

# Arquitetura

![Imgur](https://i.imgur.com/tWgVAlf.png)

* Front-end web em [Python](https://www.python.org/download/releases/3.0/) responsável por registrar os votos dos 
usuários e deixar escolher entre duas opções de voto.

* Seviço de fila - AWS [Simple Queue Service(SQS)](https://aws.amazon.com/sqs/) que armazena os votos dos usuários.

* Backend em Python que processa os votos vindo do SQS e armazena no..

* Banco de dados relacional [MySQL](https://dev.mysql.com/doc/) onde é persistido os votos.

* Front-end API que retorna a quantidade de votos.

# Nota

A aplicação só aceita um voto por cliente baseado no seu [COOKIE](https://www.allaboutcookies.org/cookies/).
É possível votar mais de uma vez, porém o seu voto será atualizado e não quantificado.
