# Criação de microserviços com IA, utilizando Python.

Este respositorio tem o proposito de servir como acompanhamento para o minicurso ministrado na SDC, que aborda a criação de microserviços com IA, utilizando Python.

## Overview

Primeiramente vamos tomar um tempo para definir como está estruturado o ReadMe. Isso tambem serve como um sumario para os principais topicos abordados no minicurso. Esse documento contem informações sobre:

- Requisitos e configurações de desenvolvimento.
- Configuração das imagens Docker.
- Desenvolvimento do microsserviço.
- Criação de testes.

A divisão nesses quatro topicos foi realizada com o objetivo de melhor diferenciar as diferentes etapas de desenvolvimento de um microsserviço.

## Requisitos e configurações de desenvolvimento.

Antes de começarmos a desenvolver o microsserviço é necessario ter alguns requisitos. Esses requisitos vão facilitar o processo de desenvolvimento. Essencialmente o basico necessario é:

- Um editor de texto.
- Um interpretador Python.

Entretanto, existem algumas ferramentas que vão tornar o processo de desenvolvimento bem menos complexo. Para esse minicurso, faremos uso de:

- Anaconda (Ou Miniconda).
- Docker.
- Visual Studio Code.

O proposito de cada uma delas vai ser expandido abaixo.

### Anaconda (Ou Miniconda)

[Anaconda](https://www.anaconda.com/) é uma distribuição da linguagem de programação Python. Essa distribuição ja conca com diversas bibliotecas de processamento de dados. Alem disso o Anaconda possui um sistema de gestão de pacotes que facilita divisão de ambientes especificos para cada projeto. Existe tambem uma versão "lite" do Anaconda, chamado Miniconda. Essa versão é recomdada para maquinas que possuem armazenamento limitado.

O Anaconda nos ajuda a separar um ambiente controlado, similar aos ambiente virtuais do proprio Python, mas de maneira mais simplificada. Essa distribuição python está disponivel [neste link](https://www.anaconda.com/products/individual).

Enquanto não recomendado, é possivel seguir com esse minicurso sem o Anaconda.

### Docker

O Docker é uma plataforma aberta, criada com o objetivo de facilitar o desenvolvimento, a implantação e a execução de aplicações em ambientes isolados. O Docker possui alta presença em diverças empresas do mundo, e conhecimento com a ferramenta é uma caracteristica desejavel na area de TI.

Para esse minicurso, faremos uso de imagens Docker para disponibilização do nosso microsserviço. Isso é feito pois assim garantimos que o microsserviço é executado de forma isolada num container, independente de qual servidor estamos utilizando.

O download do docker poder ser realizado clicando [neste link](https://www.docker.com/products/docker-desktop).

### Visual Studio Code

O Visual Studio Code é a ultima recomendação e requisito para esse minicurso. Alem de ser um editor de codigo o VS Code tambem possui diversas funcionalidade que fornecem uma melhor experiencia ao usuario.

Com a possibilidade de uso de extenções o Visual Studio Code vai ser utilizado nesse minicurso em todas as etapas do desenvolvimento. Com a extenção do Docker é possivel levantar imagens facilmente, e até mesmo ver conteudo dentro dos containers. O Visual Studio Code tambem possuiu uma otima integração com os testes em Python, e estes são essenciais no processo de desenvolvimento de microsserviços.

O Visual Studio Code pode ser obtido [aqui](https://code.visualstudio.com/).

###

Por fim, com todos os requisitos, vamos organizar nosso ambiente de desenvolvimento para o minicurso.



1. Faça o download do repositório [Microservice](https://github.com/SandovaNeto/Microservice).

        $ git clone https://github.com/SandovaNeto/Microservice.git

2. Crie um ambiente conda com o seguinte comando na linha de comando:
        
        $ conda create -n minicurso python==<3.7>

3. Ative o ambiente e instale os pacotes necessarios com o pip.

        $ conda activate minicurso
        $ pip install -r requirements.txt

4. Uma vez terminada a instalação dos requisitos, abra o Visual Studio Code. Navege na barra lateral para a aba de "Extensões" (Ctrl+Shitf+X).

5. Busque e intale as extenções: Docker, Python e Pylance. Todas fornecidas pela Microsoft. Caso necessario reinicie o Visual Studio Code.

6. Com o Visual Studio Code abra a pasta cat_dog_classification (Ctrl+K+O) do repositorio baixado.

Pronto, com isso o seu ambiente deve estar configurado e podemos prosseguir.

## Configurando as Imagens Docker.

Como foi mencionado anteriormente vamos utilizar imagens Docker como fundação para o nosso microsserviço. Isso garante que independendo de onde o serviço for hospedado nosso ambiente sempre será constante.

Para a implementação do nosso microsserviço que utiliza um modelo de redes neurais teremos duas imagens Docker. Uma delas fica responsavel unicamente para servir de container para nosso modelo. Para essa imagen faremos uso do TensorFlow Serving, ele é um sistema de serviço flexível e de alto desempenho para modelos de aprendizado de máquina, projetado para ambientes de produção. O TensorFlow Serving facilita a implantação de novos algoritmos e experimentos, mantendo a mesma arquitetura de servidor e APIs.

A outra imagem Docker é responsavel pelo proprio processamento do nosso serviço. É essa a imagem que onde o fluxo do microserviço vai ser desenvolvido. É nessa imagem tambem que as requições vão chegar e os retornos irão ocorrer.

As configurações das imagens Docker podem ser encontradas navegando para o diretorio "app" e em seguida para "model_service" ou "preprocess_service", nos arquivos nomeeados "Dockerfile". Vamos primeiro focar na configuração da imagem que vai hospedar nosso modelo.

***Inserir Imagem***

Uma descrição linha por linha do codigo seria:

1: Imagem Docker base fornecida pelo TensorFlow Serving.

3-4: Definição de variaveis de ambiente.

6: Copiar os arquivos da maquina local (prev_trained_models) para a imagem docker.

8-9: Expor portas.

11-14: Configurações de conexão.

Note que dentro do diretorio "prev_trained_models" temos o modelo de classificação treinado. O modelo precisa estar no formato ".pb", o formato utilizado no tensorflow.

Em seguida passamos para o Dockerfile da imagem do "preprocess_service".

***Inserir Imagem***

Novamente segue o passo a passo de cada linha:

1: Imagem Docker base fornecida pelo Criador da FastAPI.

3: Atualização do modulo de gestão de pacotes do Python (PIP).

5-6: Atualização do apt-get da imagem Docker, e instalação de algumas dependencias.

8: Definição do diretorio base dentro da imagem.

10-11: Copiar os pacotes Python necessarios da maquina local para a imagem, e realizar a instalação.

13: Copia da pasta app para a imagem.

15: Definir porta.

17: Executar microsserviço.


Por fim vamos configurar o arquivo docker-compose.yml que pode ser encontrado no diretorio "app". O arquivo de compose contem as configurações necessarias para a aexecução de um serviço com mais de um container. No nosso caso, como temos um container para o nosso modelo e um container para nosso serviço precisamos integrar os dois por meio deste arquivo.

***Inserir Imagem***

Nesse arquivo temos:

1: Versão do docker sendo utilizada.

4-11: Definição do serviço do modelo (Localização do Dockerfile, Nome do Container, Rede Interna, Portas).

13-22: Definição do serviço de preprocessamento (Localização do Dockerfile, Nome do Container, Nome do container do modelo, Rede Interna, Portas).

24-25: Declaração da rede interna.

Com os arquivos de configuração finalizados podemos então passar para a proxima etapa a de desenvolvimento.
