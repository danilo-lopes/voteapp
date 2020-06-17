# Voting App

Aplicação simples distribuída em containeres. Todos as suas camadas desenvolvidas em Python.

O objetivo desta foi desenvolver habildades no processamento, armazenamento e entrega de dados, englobando serviços de
fila, banco de dados e serviços de WEB/API.

# Arquitetura

![Imgur](https://i.imgur.com/8EOieBU.png)

* Front-end web em [Python](https://www.python.org/download/releases/3.0/) responsável por registrar os votos dos 
usuários e deixar escolher entre duas opções de voto.

* Seviço de fila - AWS [Simple Queue Service(SQS)](https://aws.amazon.com/sqs/) que armazena os votos dos usuários.

* Backend em Python que processa os votos vindo do SQS e armazena no..

* Banco de dados relacional [MySQL](https://dev.mysql.com/doc/) onde é persistido os votos.

* Front-end API que retorna a quantidade de votos.

### Imagem Docker

Docker hub:

[vote](https://hub.docker.com/repository/docker/dansolo7/worker)

[worker](https://hub.docker.com/repository/docker/dansolo7/voting)

[front](https://hub.docker.com/repository/docker/dansolo7/front)


### Helm Chart para ambientes K8S

```
.voteapp-helm
├── Chart.yaml
├── templates
│   ├── front-deployment.yaml
│   ├── front-ingress.yaml
│   ├── front-service.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-service.yaml
│   ├── NOTES.txt
│   ├── secrets.yaml
│   ├── vote-deployment.yml
│   ├── vote-ingress.yml
│   ├── vote-service.yml
│   ├── worker-deployment.yaml
│   ├── worker-ingress.yaml
│   └── worker-service.yaml
└── values.yaml
```

Na utilização do chart, altere apenas o `values.yaml` informando as credenciais da AWS e senha do banco de dados.
A senha do banco de dados informada no chart sera a senha do usuario root, o qual a aplicação utiliza. 

# API

### Aplicação Vote
A aplicação vote disponibiliza um api para realizar os votos e checar se o serviço que o mesmo utiliza (SQS) está
operacional. 

Endpoints:

`/api/healthcheck` - Saude da fila SQS

return code:

```
{
    "sqsStatus": "OK"
}
```

`/api/postVotes` - enviar seu voto

formato json aceito no endpoint:

`{"userID": "id-xxxyyyzzz", "vote": "coca"}`

Ex:

`curl -H "Content-Type: application/json" -X POST -d '{"userID": "id-xxxyyyzzz", "vote": "coca"}' .../api/postVotes`

return code:

```
{
    "voteStatus": 200
}
```

Voce deve enviar um json passando as chaves "userID" e "vote".

Se passar campos inválidos:

Ex:

`curl -H "Content-Type: application/json" -X POST -d '{"foo": "id-xxxyyyzzz", "bar": "coca"}' .../api/postVotes`

return code:

```
{
    "badRequest": "Your json doesnt pass in the application creteria"
}
```

### Aplicação Worker

A aplicação worker também disponibiliza um api. A função dos endpoints é fornecer informações de operabilidade estável
dos serviços que a aplicação utiliza, no caso, a fila do SQS e o banco de dados.

Enpoints:

`/api/healthchecksqs` - Saude do sqs

return code:

```
{
    "sqsStatus": "OK"
}

```

`/api/healthcheckmysql` - Saude do banco de dados

return code:

```
{
    "mysqlStatus": "OK"
}
```

### Aplicação Front

A aplicação front disponibila um endpoint para checagem dos votos.

Endpoint:

`/api/votes`

return code:

```
{
    "votes": {
        "coca": "2",
        "pepsi": "1"
    }
}

```

## Setup em Docker Composer

[docker](https://docs.docker.com/get-docker/)

[docker-composer](https://docs.docker.com/compose/install/)

**Crie duas Docker network do tipo Overlay, uma chamada backend e a outra frontend.**

`docker network create --driver overlay --attachable voting_backend`

`docker network create --driver overlay --attachable voting_frontend`

**Nota:** Necessário iniciar o swarm no nó em que vai subir os containeres

`docker swarm init --advertise-addr "nome da sua interface de rede ou o endereço ip dela"`

**Crie um docker volume apontando para algum diretório da sua máquina para garantirmos os dados do banco**

```
docker volume create --driver local \
    --opt type=none \
    --opt device=/srv/voting_voteapp-data \
    --opt o=bind voting_voteapp-data
```

**Variaveis de ambiente necessárias:**

```
export AWS_ACCESS_KEY='BAR'
export AWS_SECRET_KEY='FOO'
export AWS_REGION='FOO'
export MYSQL_HOST='BAR'
export MYSQL_USER='FOO'
export MYSQL_DB='voteapp'
export MYSQL_PASSWORD='foo'
export COMPOSE_PROJECT_NAME=voting
```

> Não mude o nome da database.

---

Após o setup inicial:

```
docker-compose -f docker-compose.yml up
```

## Setup em K8S

Analise qual o cenário em que o seu cluster se encontra porque é necessário utilizar um ingress controller compatível
com o ambiente.

Recomendável que utilize um plugin de rede intra cluster para comunicação dos `PODS`. 
[Weave Net](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/)

Para ambiente On-Primeses recomendo utilizar o [Metallb](https://kubernetes.github.io/ingress-nginx/deploy/baremetal/)
como Ingress Controller.

Recomendação de projeto para subir um ambiente Kubernetes local: Github [k8-cluster](https://github.com/danilo-lopes/k8s-cluster)

---

```
helm install voteapp ./voteapp-helm/
```


`kubectl get po`

```
NAME                                                READY   STATUS    RESTARTS   AGE
ingress-controller-nginx-ingress-694bc4c49b-665mb   1/1     Running   0          13h
mysql-7b4747bdf6-rrvf6                              1/1     Running   0          12h
voteapp-front-server-7b6fcf96c-hgsn5                1/1     Running   0          12h
voteapp-vote-server-56ff6f5745-wzlxl                1/1     Running   0          12h
voteapp-worker-server-5ffc77b5bb-7wgwv              1/1     Running   0          12h

```

`kubectl get svc`

```
NAME                               TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)                      AGE
ingress-controller-nginx-ingress   LoadBalancer   10.103.81.22     192.168.1.60   80:30144/TCP,443:31651/TCP   13h
kubernetes                         ClusterIP      10.96.0.1        <none>         443/TCP                      13h
mysql-service                      ClusterIP      10.107.109.162   <none>         3306/TCP                     12h
voteapp-front-service              NodePort       10.106.181.130   <none>         80:31995/TCP                 12h
voteapp-vote-service               NodePort       10.102.222.15    <none>         80:30608/TCP                 12h
voteapp-worker-service             NodePort       10.111.88.41     <none>         80:30297/TCP                 12h
```

`kubectl get ingress`

```
NAME                     CLASS    HOSTS            ADDRESS        PORTS   AGE
voteapp-front-ingress    <none>   www.front.com    192.168.1.60   80      12h
voteapp-vote-ingress     <none>   www.vote.com     192.168.1.60   80      12h
voteapp-worker-ingress   <none>   www.worker.com   192.168.1.60   80      12h
```

`kubectl get secrets`

```
NAME                            TYPE                                  DATA   AGE
default-token-tcq9q             kubernetes.io/service-account-token   3      69m
sh.helm.release.v1.voteapp.v1   helm.sh/release.v1                    1      57m
voteapp-voteapp-secret          Opaque                                3      57m
```

# Nota

A aplicação só se baseia em ID único. Através do [COOKIE](https://www.allaboutcookies.org/cookies/) quando o voto é feito
via browser ou userID via API. É possível votar mais de uma vez via browser ou via API com o mesmo COOKIE ou userID,
porém o seu voto será atualizado e não quantificado.
