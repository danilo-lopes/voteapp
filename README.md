# Voting App

Simples aplicação distribuída em containeres. Todos as suas camadas desenvolvidas em Python.

O objetivo desta foi desenvolver habildades no processamento, armazenamento e entrega de dados, englobando serviços de
fila, banco de dados e serviços de WEB/API.

## Respositório

[voting](https://github.com/danilo-lopes/vote)

[worker](https://github.com/danilo-lopes/worker)

[front](https://github.com/danilo-lopes/front)

# Arquitetura

![Imgur](https://i.imgur.com/8EOieBU.png)

* Front-end web em [Python](https://www.python.org/download/releases/3.0/) responsável por registrar os votos dos 
usuários e deixar escolher entre duas opções de voto.

* Seviço de fila - AWS [Simple Queue Service(SQS)](https://aws.amazon.com/sqs/) que armazena os votos dos usuários.

* Backend em Python que processa os votos vindo do SQS e armazena no..

* Banco de dados relacional [MySQL](https://dev.mysql.com/doc/) onde é persistido os votos.

* Front-end API que retorna a quantidade de votos.

## Repositório das imagens docker

[voting](https://hub.docker.com/repository/docker/dansolo7/worker)

[worker](https://hub.docker.com/repository/docker/dansolo7/voting)

[front](https://hub.docker.com/repository/docker/dansolo7/front)

# API

### Aplicação Vote
A aplicação vote disponibiliza um api para realizar os votos e checar se o serviço que o mesmo utiliza (SQS) está
operacional. 

## Endpoints:

### Disponibilidade da fila no SQS

`/api/healthcheck`

return code:

```
{
    "sqsStatus": "OK"
}
```

## Post de um voto

`/api/postVotes`

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

O return code será:

```
{
    "badRequest": "Your json doesnt pass in the application creteria"
}
```

### Aplicação Worker

A aplicação worker também disponibiliza um api. A função dos endpoints é fornecer informações de operabilidade estável
dos serviços que a aplicação utiliza, no caso, a fila do SQS e o banco de dados.

## Enpoints:

### Disponibilidade da fila SQS

`/api/healthchecksqs`

return code:

```
{
    "sqsStatus": "OK"
}

```

### Disponibilidade do banco MySQL

`/api/healthcheckmysql`

return code:

```
{
    "mysqlStatus": "OK"
}
```

### Aplicação Front

A aplicação front disponibila um endpoint para checagem dos votos.

## Endpoint:

### Votos realizados

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

## Setup para Docker Composer

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

## Setup para Kubernetes

Recomendável que utilize um plugin de rede intra cluster para comunicação dos `PODS`. 
[Weave Net](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/)

Para ambiente On-Primeses recomendo utilizar o [Metallb](https://kubernetes.github.io/ingress-nginx/deploy/baremetal/)
como Ingress Controller.

Recomendação de projeto para subir um ambiente Kubernetes local: [k8-cluster](https://github.com/danilo-lopes/k8s-cluster)

Foi desenvolvido um helm chart para deploy da stack inteira no cluster, criando o banco de dados MySQL, secrets, ingress e etc.

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

# CICD

Foi utilizado o [Gitlab](https://docs.gitlab.com/) como CICD, ferramenta bem fácil de utilização, possui bastente documentação na internet e possui versão free [Gitlab CE](https://about.gitlab.com/install/?version=ce).

É interessante fazer um fork dos projetos das aplicações e subir no próprio gitlab e fazer o CICD direto nele, mais perto de uma simulação real.

Você pode usar o gitlab direto no Kubernetes (via helm chart) ou instalar em um servidor dedicado, no meu projeto achei melhor em utilizá-lo em um servidor dedicado, por estar fazendo o versionamento do código nele.

Com base na arquitetura da aplicação que foi mostrado acima, o desenho lógico da pipeline segue a seguinte:

![Imgur](https://i.imgur.com/zpFbIaI.png)

### Gilab setup

Vou falar de algumas questões chaves que são necessárias para a configuração do gitlab.

O gitlab utiliza um `agent` para fazer deploy do projeto no cluster, quando você faz a integração dele com cluster o gitlab "instancia" dois PODs, um `tiller-deploy`(responsável pela instação de outros plugins do gitlab no cluster) e um `runner-gitlab` (responsável pelo CICD das suas aplicações).

Você precisa de dois permissionamentos. Um para o tiller e o outro para o runner 

Para o tiller é necessário:

A criação de uma `serviceaccount` com permissão de `cluster-admin` no `namespace` kube-system:

`kubectl create serviceaccount -n kube-system gitlab`

`kubectl create clusterrolebinding admin-gitlab --serviceaccount kube-system:gitlab --clusterrole cluster-admin`

Antes da permissão para o Runner, instale o `GitLab Runner` no painel de integração do gitlab, assim ele vai criar o POD do mesmo. Quando você instala o plugin Gitlab Runner no painel ele cria uma serviceaccount chamada `default`, com isso, devemos dar permissão para essa serviceaccount, que no meu caso, dei permissão de admin em todo o cluster, assim ela consegue fazer deploy em qualquer namespace:

`kubectl create clusterrolebinding gitlab-deploy-user --serviceaccount gitlab-managed-apps:default --clusterrole admin`

Com todo esse permissionamento o gitlab consegue instalar qualquer plugin que você desejar utilizando a serviceaccount gitab, lembrando que a mesma possui permissão de clusterrole, o tiller só tem a função de instalação de plugins, e consegue fazer deploy das pipelines em qualquer namespace por a serviceaccount do runner, default, ter permissão de admin no cluster.

**build**

```
Running with gitlab-runner 13.0.1 (21cb397c)
   on runner-gitlab-runner-7467f44f8-qjb5w ssJeKW2u
Preparing the "kubernetes" executor
00:00
 Using Kubernetes namespace: gitlab-managed-apps
 Using Kubernetes executor with image docker:dind ...
Preparing environment
00:03
 Waiting for pod gitlab-managed-apps/runner-ssjekw2u-project-1-concurrent-0n9p7l to be running, status is Pending
 Running on runner-ssjekw2u-project-1-concurrent-0n9p7l via runner-gitlab-runner-7467f44f8-qjb5w...
Getting source from Git repository
00:00
 Fetching changes with git depth set to 50...
 Initialized empty Git repository in /builds/gitlab/voting/.git/
 Created fresh repository.
 From https://gitlab.biqueirabr.com.br/gitlab/voting
  * [new ref]         refs/pipelines/1 -> refs/pipelines/1
  * [new branch]      master           -> origin/master
 Checking out 3c79c303 as master...
 Skipping Git submodules setup
Restoring cache
00:00
Downloading artifacts
00:01
Running before_script and script
00:11
 $ docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD"
 WARNING! Using --password via the CLI is insecure. Use --password-stdin.
 WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
 Configure a credential helper to remove this warning. See
 https://docs.docker.com/engine/reference/commandline/login/#credentials-store
 Login Succeeded
 $ docker build -t "$CI_REGISTRY_IMAGE":"$CI_COMMIT_SHA" .
 Step 1/5 : FROM dansolo7/voteapp-image:1.0
 1.0: Pulling from dansolo7/voteapp-image
 8559a31e96f4: Pulling fs layer
 62e60f3ef11e: Pulling fs layer
 002bcbc97d49: Pulling fs layer
 ba21c0b7837a: Pulling fs layer
 b3463869e7af: Pulling fs layer
 f536a7750ecd: Pulling fs layer
 6bdf1961c0ae: Pulling fs layer
 b3463869e7af: Waiting
 ba21c0b7837a: Waiting
 f536a7750ecd: Waiting
 6bdf1961c0ae: Waiting
 62e60f3ef11e: Verifying Checksum
 62e60f3ef11e: Download complete
 ba21c0b7837a: Verifying Checksum
 ba21c0b7837a: Download complete
 8559a31e96f4: Verifying Checksum
 8559a31e96f4: Download complete
 002bcbc97d49: Verifying Checksum
 002bcbc97d49: Download complete
 b3463869e7af: Verifying Checksum
 b3463869e7af: Download complete
 f536a7750ecd: Verifying Checksum
 f536a7750ecd: Download complete
 6bdf1961c0ae: Verifying Checksum
 6bdf1961c0ae: Download complete
 8559a31e96f4: Pull complete
 62e60f3ef11e: Pull complete
 002bcbc97d49: Pull complete
 ba21c0b7837a: Pull complete
 b3463869e7af: Pull complete
 f536a7750ecd: Pull complete
 6bdf1961c0ae: Pull complete
 Digest: sha256:29171c0f295e0c2dece547a65e1683d02ea8eb760f29220f7cbe022226a2df61
 Status: Downloaded newer image for dansolo7/voteapp-image:1.0
  ---> 9ef2937d1053
 Step 2/5 : WORKDIR /app
  ---> Running in 1e782b0b8ac7
 Removing intermediate container 1e782b0b8ac7
  ---> 1c1986f0bccd
 Step 3/5 : COPY app docker-entrypoint.sh ./
  ---> c07e61db9208
 Step 4/5 : EXPOSE 80
  ---> Running in 1c0e7e69a4bc
 Removing intermediate container 1c0e7e69a4bc
  ---> 160e1c2cf989
 Step 5/5 : ENTRYPOINT bash docker-entrypoint.sh
  ---> Running in a1d90ebc19b1
 Removing intermediate container a1d90ebc19b1
  ---> 7ea6b0b76a65
 Successfully built 7ea6b0b76a65
 Successfully tagged [MASKED]:3c79c303bbd2195d43614a818787130da3b56838
 $ docker push "$CI_REGISTRY_IMAGE"
 The push refers to repository [docker.io/[MASKED]]
 2b685e59c43a: Preparing
 94c290b5debc: Preparing
 4aff098e489e: Preparing
 966e83c481bc: Preparing
 0c6163f2d025: Preparing
 361df01300cf: Preparing
 8f9ba0be9040: Preparing
 0bd71a837902: Preparing
 13cb14c2acd3: Preparing
 361df01300cf: Waiting
 8f9ba0be9040: Waiting
 0bd71a837902: Waiting
 13cb14c2acd3: Waiting
 0c6163f2d025: Layer already exists
 4aff098e489e: Mounted from dansolo7/voteapp-image
 8f9ba0be9040: Layer already exists
 966e83c481bc: Mounted from dansolo7/voteapp-image
 361df01300cf: Layer already exists
 13cb14c2acd3: Layer already exists
 0bd71a837902: Layer already exists
 2b685e59c43a: Pushed
 94c290b5debc: Pushed
 3c79c303bbd2195d43614a818787130da3b56838: digest: sha256:fa0d2fb22cb96a376689d49b67bd4ab5cba3cab59a358542824519f451982e39 size: 2204
Running after_script
00:00
Saving cache
00:00
Uploading artifacts for successful job
00:00
 Job succeeded

```

**deploy**

```
Running with gitlab-runner 13.0.1 (21cb397c)
   on runner-gitlab-runner-7467f44f8-qjb5w ssJeKW2u
Preparing the "kubernetes" executor
00:00
 Using Kubernetes namespace: gitlab-managed-apps
 Using Kubernetes executor with image bitnami/kubectl ...
Preparing environment
00:06
 Waiting for pod gitlab-managed-apps/runner-ssjekw2u-project-1-concurrent-0hcnkk to be running, status is Pending
 Waiting for pod gitlab-managed-apps/runner-ssjekw2u-project-1-concurrent-0hcnkk to be running, status is Pending
 Running on runner-ssjekw2u-project-1-concurrent-0hcnkk via runner-gitlab-runner-7467f44f8-qjb5w...
Getting source from Git repository
00:00
 Fetching changes with git depth set to 50...
 Initialized empty Git repository in /builds/gitlab/voting/.git/
 Created fresh repository.
 From https://gitlab.biqueirabr.com.br/gitlab/voting
  * [new ref]         refs/pipelines/1 -> refs/pipelines/1
  * [new branch]      master           -> origin/master
 Checking out 3c79c303 as master...
 Skipping Git submodules setup
Restoring cache
00:01
Downloading artifacts
00:00
Running before_script and script
00:00
 $ sed 's/__VERSION__/'"$CI_COMMIT_SHA"'/g; s/__NAMESPACE__/voteapp/g' vote-k8s.yaml > vote-kubernetes.yaml;
 $ kubectl apply -f vote-kubernetes.yaml
 deployment.apps/vote-server created
 service/vote-service created
 ingress.extensions/vote-ingress created
Running after_script
00:00
Saving cache
00:00
Uploading artifacts for successful job
00:01
 Job succeeded
```

---

```
root@ip-192-168-2-250:~# kubectl get po -n voteapp
NAME                            READY   STATUS    RESTARTS   AGE
front-server-56874f5ff6-kvx5j   1/1     Running   0          83m
mysql-8dfb77fcf-t7mxl           1/1     Running   0          91m
vote-server-76d9c76d4f-r98hb    1/1     Running   0          88m
worker-server-6b4c54568-fxz8l   1/1     Running   0          86m
```

```
NAMESPACE   NAME             CLASS    HOSTS                      ADDRESS                                                                  PORTS   AGE
voteapp     front-ingress    <none>   front.biqueirabr.com.br    a3c8f2e5e74f94363b78927d99dd26bb-191501161.us-east-1.elb.amazonaws.com   80      85m
voteapp     vote-ingress     <none>   vote.biqueirabr.com.br     a3c8f2e5e74f94363b78927d99dd26bb-191501161.us-east-1.elb.amazonaws.com   80      88m
voteapp     worker-ingress   <none>   worker.biqueirabr.com.br   a3c8f2e5e74f94363b78927d99dd26bb-191501161.us-east-1.elb.amazonaws.com   80      87m
```

---

`10:21:34 danilo@moria github_pessoal → curl http://vote.biqueirabr.com.br/api/healthcheck`

```
{
    "sqsStatus": "OK"
}
```

`11:10:20 danilo@moria github_pessoal → curl -H "Content-Type: application/json" -X POST -d '{"userID": "id-xxxyyyzzz", "vote": "coca"}' http://vote.biqueirabr.com.br/api/postVotes`

```
{
    "voteStatus": 200
}
```

`11:10:27 danilo@moria github_pessoal → curl -H "Content-Type: application/json" -X POST -d '{"foo": "id-xxxyyyzzz", "bar": "coca"}' http://vote.biqueirabr.com.br/api/postVotes`

```
{
    "badRequest": "Your json doesnt pass in the application creteria"
}
```

`11:10:32 danilo@moria github_pessoal → curl http://worker.biqueirabr.com.br/api/healthchecksqs`

```
{
    "sqsStatus": "OK"
}
```

`11:10:51 danilo@moria github_pessoal → curl http://worker.biqueirabr.com.br/api/healthcheckmysql`

```
{
    "mysqlStatus": "OK"
}
```

`11:11:06 danilo@moria github_pessoal → curl http://front.biqueirabr.com.br/api/votes`

```
{
    "votes": {
        "coca": "1",
        "pepsi": "0"
    }
}
```

# Nota

A aplicação só se baseia em ID único. Através do [COOKIE](https://www.allaboutcookies.org/cookies/) quando o voto é feito
via browser ou userID via API. É possível votar mais de uma vez via browser ou via API com o mesmo COOKIE ou userID,
porém o seu voto será atualizado e não quantificado.
