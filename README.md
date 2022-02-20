# Criação de microserviços com IA, utilizando Python.

Este respositorio tem o proposito de servir como acompanhamento para o minicurso ministrado na SDC, que aborda a criação de microserviços com IA, utilizando Python. O tema do minicurso vai ser o desenvolvimento de um microserviço capaz de classificar corretamente uma imagem em duas classes, Gato ou Cachorro. Seram utilizados alguns pacotes como tensorflow, grpc. A API sera criada utilizando FastAPI. Esse ReadMe tem a função de servir tambem como um guia de acompanhamento para o minicurso e vai ficar disponivel para o futuro, caso você queira rever algo quando desejar estudar novamente.

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

### Organizando o ambiente

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

7. Pressione Ctrl + Shit + P, e selecione a opção "Select Interpreter", em seguida selecione o ambiente "minicurso".

Pronto, com isso o seu ambiente deve estar configurado e podemos prosseguir.

## Configurando as Imagens Docker.

Como foi mencionado anteriormente vamos utilizar imagens Docker como fundação para o nosso microsserviço. Isso garante que independendo de onde o serviço for hospedado nosso ambiente sempre será constante.

Para a implementação do nosso microsserviço que utiliza um modelo de redes neurais teremos duas imagens Docker. Uma delas fica responsavel unicamente para servir de container para nosso modelo. Para essa imagen faremos uso do TensorFlow Serving, ele é um sistema de serviço flexível e de alto desempenho para modelos de aprendizado de máquina, projetado para ambientes de produção. O TensorFlow Serving facilita a implantação de novos algoritmos e experimentos, mantendo a mesma arquitetura de servidor e APIs.

A outra imagem Docker é responsavel pelo proprio processamento do nosso serviço. É essa a imagem que onde o fluxo do microserviço vai ser desenvolvido. É nessa imagem tambem que as requições vão chegar e os retornos irão ocorrer.

As configurações das imagens Docker podem ser encontradas navegando para o diretorio "app" e em seguida para "model_service" ou "preprocess_service", nos arquivos nomeeados "Dockerfile". Vamos primeiro focar na configuração da imagem que vai hospedar nosso modelo.

![Docekrfile_model_service](/images/model_service_dockerfile.png "Arquivo Dockerfile do model_service.")

Uma descrição linha por linha do codigo seria:

1: Imagem Docker base fornecida pelo TensorFlow Serving.

3-4: Definição de variaveis de ambiente.

6: Copiar os arquivos da maquina local (prev_trained_models) para a imagem docker.

8-9: Expor portas.

11-14: Configurações de conexão.

Note que dentro do diretorio "prev_trained_models" temos o modelo de classificação treinado. O modelo precisa estar no formato ".pb", o formato utilizado no tensorflow.

Em seguida passamos para o Dockerfile da imagem do "preprocess_service".

![Docekrfile_preprocess_service](/images/preprocess_service_dockerfile.png "Arquivo Dockerfile do preprocess_service.")

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

![Docekrfile_compose](/images/docker-compose-yml.png "Arquivo docker-compose dos microserviços.")

Nesse arquivo temos:

1: Versão do docker sendo utilizada.

4-11: Definição do serviço do modelo (Localização do Dockerfile, Nome do Container, Rede Interna, Portas).

13-22: Definição do serviço de preprocessamento (Localização do Dockerfile, Nome do Container, Nome do container do modelo, Rede Interna, Portas).

24-25: Declaração da rede interna.

Com os arquivos de configuração finalizados podemos então passar para a proxima etapa a de desenvolvimento.


## Desenvolvimento do microsserviço.

Como mencionado anteriormente a parte de preprocessamento do nosso microserviço vai ser executado num container docker exclusivo. Nos configuramos esse arquivo Dockerfile no passo anterior. Agora é o momento de desenvolver nosso microsserviço. Para isso navegue até o diretorio "app->preprocess_service->app". Aqui você vai ver os seguintes arquivos:

1. app_server.py: É aqui que vamos definir o nosso microsserviço, o que acontece quando uma nova requisição é recebida e qual o retorno deve ser dado no fim.
2. model_runner.py: Aqui estão os metodos referentes a integração com o container do modelo. Neste arquivo que são definidas as funções que fazem a classificação com o modelo de inteligencia artificial.
3. utils.py: O arquivo de utils tem algumas funções de preprocessamento. A fim de melhorar a legibilidade do codigo, essas funções foram separadas em um arquivo diferente do aoo_server.py

Vamos falar um pouco mais sobre cada um desses arquivos separamente, a começar com o app_server.py, o nucleo principal do nosso microserviço. Primeiramente vamos começar com os imports, e a definiçaõ de algumas classes e Enums.

![App_server1.py](/images/app_server1.png "Primeira parte do arquivo app_server.py.")

Uma descrição do codigo linha por linha é:

1-8: Import das bibliotecas utilizadas.

10-28: Definição de diversas Classses e Enums que são uteis no processo de desenvolvimento.

31: Instanciação de um objeto da classe ModelRunner, responsavel por realizar a comunicação com o modelo de IA.

Em seguida vamos propriamente definir a nossa API e o fluxo a ser executado uma vez que um request for recebido.

![App_server2.py](/images/app_server2.png "Segunda parte do arquivo app_server.py.")

34: Criando a API com FastAPI.

37-38: Definindo o Endpoint.

40-45: Confirmando que a imagem é uma imagem valida, caso contrario retornamos um erro.

47-50: Caso seja uma imagem valida realizamos a classificação e retornamos o resultado.

53-54: Executar a nossa API.

Com isso temos a nosa API de preprocessamento definida. Vamos agora partir para o arquivo model_runner.py onde é definida a comunicação entre o container de preprocessamento e o container do modelo. Ja podemos notar algumas diferenças em relação ao arquivo anterior ja na parte de imports

![Model_Runner1.py](/images/model_service1.png "Imports do arquivo model_runner.py.")

Em adição a alguns novos pacotes que vão ser utilizados para preprocessamento e utilidades como os, yaml, pprint, base64, numpy e PIL, temos tambem a presença de alguns pacotes ja vistos anteriormente como fastAPI e pydantic. Tambem temos agora alguns pacotes provenientes do tensorflow, estes vãos er utilizados para realizar a comunicação entre o os dois serviços (model_service e preprocess_service). Seguindo é possivel notar que todo este arquivo é a definição da classe ModelRunner e seus metodos.

![Model_Runner2.py](/images/model_service2.png "Primeira parte do arquivo model_runner.py.")

19-25: Definiçaõd o Init da classe.

27-35: Metodo de definição das configuraçoes do modelo.

37-43: Metodo de criação do stub.

45-50: Metodo de criação do request GRPC.

Esses metodos são referentes a comunicação com o nosso outro serviço, o "model_service". Primeiramente nós definimos algumas propriedades do nosso modelo como nome (experiment_id), e qual a camada de entrada e de saida do modelo. Fazemos isso pois essa informação é necessaria ao realizar um request para a imagem do tenserflow serving. Em seguida criamos o stub, isso é o canal de comunicação entre nosso serviço de pre-processamento e o serviço de modelo. Por fim definimos o request GRPC, passando as informações do modelo e a imagem a ser classificada.

![Model_Runner3.py](/images/model_service3.png "Segunda parte do arquivo model_runner.py.")

52-63: Preprocessamento da imagem utilizando o pacote PIL.

65-82: Fluxo completo de uma requisição para o model_service, com processamento do resultado.

Esses dois ultimos metodos focam em processar a entrada e saida do nosso request. Primeiramente fazemos o preprocessamento necessario na imagem em base64, como resize e normalização. Em seguida definimos o fluxo completo, instanciando o preprocessamento da imagem, criação do grpc request e processando o resultado do nosso classificador.

Por fim, vamos partir par o arquivo utils.py, aqui são definidas funções auxiliares utilizadas ao longo dos nossos serviços.

![Utils.py](/images/utils.png "Arquivo utils.py")

1-4: Importando os pacotes.

7-12: Metodo que verifica se um base64 é valido.

15-20: Metodo que converte uma imagem para o formato base64.

23-28: Metodo que converte um base64 para uma imagem.

Uma vez desenvolvido nosso modelo, podemos subir as imagens docker com os serviços. Para fazer isso clique com o botão direito no arquivo "docker-compose.yml" e selecione a opção "Compose Up". Apos um tempo as imagens devem ser levantadas com sucesso. O "Compose Up" faz o equivalente ao comando docker:

        $ docker-compose -f "app\docker-compose.yml" up -d --build
        
Vamos passar para o ultimo estagio no ciclo de criação de um micorsserviço, os testes, uma vez criados poderemos ver nosso serviço em ação.

## Criação de testes.



Testar o microserviço é uma etapa importante no ciclo de produção. Os testes não só nos ajudam a identificar erros quanto servem para manter o microserviço funcionando a medida que novas verções vão surgindo. Para criarmos os testes em python vamos fazer uso do pacote unittest.

Os testes devem estar contidos no diretorio "unit_test", aqui temos dois arquivos, o "utils.py" e o "localhost_test.py". O primeiro assim como no serviço contem algumas funções auxiliares. Enquanto o segundo define os testes. Vamos começar vendo o arquivo "utils.py".

![Test_utils.py](/images/test_utils.png "Arquivo utils.py dos testes.")

Uma descrição a cada linha pode ser dada por:

1-5: Imports de pacotes.

7-8: Definição do endpoint para realização dos testes.

11-22: Definição do metodo que realiza o request.

Neste arqui você pode definir quaisquer outros metodos que seus testes utilizem. Agora vamos passar para o arquivo "localhost_test.py"

![localhost_test.py](/images/localhost1.png "Arquivo localhost_test.")
![localhost_test.py](/images/localhost2.png "Arquivo localhost_test.")

Vendo cada linha de codigo temos:

1-4 Imports dos pacotes.

6: Definição da classe de teste.

8-38: Definição dos casos de teste individuais.

41-42: Executar os testes.

Com os testes definidos podemos executa-los direto do Visual Studio Code. Para executar os testes realize os seguintes passos:

1. Primeiramente no Visual Studio Code abra o diretorio "cat_dog_classification" (Ctrl+K+O). 
2. Pressione Ctrl + Shit + P, e selecione a opção "Python:Select Interpreter", em seguida selecione o ambiente "minicurso".
3. Pressione Ctrl + Shit + P novamente e agora selecione a opção "Python:Configure Tests", em seguida selecione "unittest", "unittest" novamente e por fim "* test *.py".
4. Navege na barra lateral esquerda para a aba de Testing abaixo da aba de extensões.

Voce deve ver algo como:

![testes](/images/tests.png "Testes encontrados.")

Para executar os testes basta clicar no icone triangular que aparece ao lado do nome de cada teste uma vez que você aproxima o cursor.

## Considerações Finais

Este é o fim da aprensentação, note que ainda existem muitas coisas abstraidas e que podem ser melhoradas nesse microserviço. Enquanto muitos dos assuntos abordados podem ser complexos é recomendado que você tire um tempo para estudar a documentação dos pacotes utilizados. Este documento e o repositorio permaneceção aqui para servir de material de estudo futuro caso seja de interesse.

Obrigado pela participação de todos!
