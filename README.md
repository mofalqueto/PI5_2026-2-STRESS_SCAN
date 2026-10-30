# 🧠 Stress Scan

**Aplicativo de classificação experimental dos níveis de estresse em estudantes universitários**

## Sobre o projeto

O **Stress Scan** é um aplicativo desenvolvido como Projeto Integrador do curso de Desenvolvimento de Software Multiplataforma da FATEC Franca.

A solução utiliza técnicas de **Machine Learning** para classificar o nível de estresse de estudantes universitários a partir das respostas a um questionário.

O projeto tem como motivação a atenção à saúde emocional no ambiente acadêmico, especialmente às experiências de estudantes pretos e pardos, considerando os desafios sociais e acadêmicos enfrentados por essa população.

A classificação é experimental e não constitui diagnóstico psicológico ou médico.

## Objetivo

Desenvolver uma aplicação que permita ao estudante:

- Responder a um questionário sobre fatores relacionados ao estresse.
- Receber uma classificação estimada do seu nível de estresse.
- Consultar o histórico das avaliações realizadas.
- Acompanhar seus resultados ao longo do tempo.

O modelo utiliza três classes:

| Classe | Classificação |
|---|---|
| 0 | Estresse baixo |
| 1 | Estresse moderado |
| 2 | Estresse alto |

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Flutter / Dart | Desenvolvimento do aplicativo |
| Python | Processamento e Machine Learning |
| Scikit-learn | Treinamento e execução do modelo |
| Regressão Logística | Algoritmo de classificação |
| FastAPI | Desenvolvimento da API REST |
| MongoDB Atlas | Armazenamento dos usuários e avaliações |
| JWT | Autenticação e proteção das rotas |
| Argon2 | Proteção das senhas |
| Joblib | Serialização do modelo treinado |
| Swagger / OpenAPI | Documentação e testes da API |

## Machine Learning

O projeto utiliza o dataset **Student Stress Monitoring Datasets**, disponibilizado no Kaggle.

Dataset: https://www.kaggle.com/datasets/mdsultanulislamovi/student-stress-monitoring-datasets

O conjunto possui **1.100 registros**, com informações relacionadas a fatores psicológicos, fisiológicos, ambientais, acadêmicos e sociais.

Após a análise e seleção de atributos, foram utilizadas **17 variáveis preditoras**.

O algoritmo selecionado foi a **Regressão Logística**, considerando seu desempenho e interpretabilidade.

### Resultados experimentais do modelo

| Métrica | Resultado |
|---|---|
| Acurácia no conjunto de teste | 90,45% |
| Validação cruzada (10 folds) | 87,50% |
| Recall da classe de estresse alto | 94,59% |

Essas métricas correspondem à avaliação do modelo no dataset utilizado. A conversão das respostas qualitativas do aplicativo para os valores numéricos esperados pelo modelo ainda não foi validada com usuários reais.

O dataset também não permite avaliar especificamente o desempenho do modelo por grupo étnico-racial.

## Arquitetura

O sistema está organizado em duas partes principais:

**Aplicativo Flutter:** responsável pela interface, autenticação, questionário e visualização das avaliações.

**API FastAPI:** responsável pelo cadastro, login, validação dos tokens JWT, execução do modelo de Machine Learning e comunicação com o MongoDB Atlas.

Fluxo previsto:

**Flutter → FastAPI → Modelo de Machine Learning → MongoDB Atlas → Flutter**

## Estrutura do projeto

```text
stress_scan/
├── api/
│   ├── main.py
│   ├── database.py
│   ├── setup_db.py
│   ├── cadastro.py
│   ├── login.py
│   ├── auth.py
│   ├── historico.py
│   ├── modelo_estresse_LR.joblib
│   ├── requirements.txt
│   └── .env
│
└── mobile/
    ├── assets/
    │   └── images/
    │       ├── logo.png
    │       ├── bemvindo.png
    │       ├── questionario.png
    │       └── resultado.png
    ├── lib/
    │   └── main.dart
    └── pubspec.yaml
```

O arquivo `.env` contém configurações sensíveis e não deve ser enviado ao repositório Git.

## Autenticação e banco de dados

A API utiliza autenticação com tokens JWT e armazenamento seguro das senhas por meio do Argon2.

O MongoDB Atlas possui duas coleções principais:

- **usuarios:** registros de identificação e credenciais protegidas.
- **avaliacoes:** resultados das classificações, associados ao usuário autenticado.

Cada avaliação armazena o identificador do estudante, o nível de estresse classificado e a data de realização.

As 17 respostas individuais do questionário não são armazenadas na implementação atual.

## Endpoints da API

| Método | Endpoint | Funcionalidade |
|---|---|---|
| GET | `/` | Verificação básica da API |
| GET | `/modelo` | Informações do modelo |
| POST | `/cadastro` | Cadastro de usuários |
| POST | `/login` | Autenticação e geração de JWT |
| GET | `/me` | Identificação do usuário autenticado |
| POST | `/prever` | Classificação e registro da avaliação |
| GET | `/historico` | Consulta ao histórico individual |

As rotas `/me`, `/prever` e `/historico` exigem autenticação.

A documentação interativa está disponível em:

`http://127.0.0.1:8000/docs`

## Como executar

### Backend — FastAPI

Na pasta `api`, configure um ambiente virtual Python e instale as dependências:

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Configure o arquivo `.env` com suas próprias credenciais:

```dotenv
MONGODB_URI=STRING_DE_CONEXAO
MONGODB_DATABASE=stress_scan
JWT_SECRET_KEY=CHAVE_SECRETA_SEGURA
```

As configurações do banco devem estar prontas antes de iniciar a API.

Execute:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### Aplicativo — Flutter

Em outro terminal:

```powershell
cd mobile
flutter pub get
flutter run -d chrome
```

O projeto poderá ser executado no Chrome para testes iniciais.

## Funcionalidades implementadas

- Cadastro de usuários com validação de e-mail.
- Login com geração de token JWT.
- Validação de autenticação em rotas protegidas.
- Integração com MongoDB Atlas.
- Classificação experimental com Regressão Logística.
- Registro das avaliações no banco de dados.
- Consulta ao histórico individual.
- Estrutura inicial do projeto Flutter.
- Tela de boas-vindas com identidade visual personalizada.
- Navegação inicial para telas provisórias de login e cadastro.

## Próximas etapas

- Desenvolver as telas de cadastro e login no Flutter.
- Integrar o aplicativo à API.
- Implementar o questionário com as 17 perguntas.
- Desenvolver a tela de resultado.
- Implementar a visualização do histórico.
- Realizar testes de integração e segurança.
- Configurar a hospedagem da API na Azure.
- Avaliar a qualidade e as limitações das classificações com entradas do questionário real.

## Limitações

O Stress Scan é uma ferramenta acadêmica e experimental de classificação.

Seus resultados não substituem acompanhamento psicológico, avaliação médica ou instrumentos clínicos validados.

O modelo foi treinado com dados públicos e ainda não passou por validação específica com a população-alvo do aplicativo.

## Informações acadêmicas

**Instituição:** FATEC Franca

**Curso:** Desenvolvimento de Software Multiplataforma

**Projeto:** Stress Scan — Projeto Integrador

**Área:** Desenvolvimento Mobile, Inteligência Artificial e Machine Learning