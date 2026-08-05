# Xenoglossia

Aplicação **Open Source** de tradução desenvolvida para reduzir barreiras linguísticas por meio de Inteligência Artificial. O projeto permite traduzir **textos, imagens e voz**, oferecendo uma experiência simples, rápida e acessível.

---

# Problema

A comunicação entre diferentes idiomas ainda é uma barreira para milhões de pessoas.

Segundo estudos:

- Aproximadamente **50% da população mundial** fala apenas um idioma.
- No Brasil, cerca de **13%** da população afirma possuir algum conhecimento em inglês, enquanto apenas cerca de **1%** é considerada realmente fluente.
- A dificuldade em compreender outros idiomas limita o acesso à informação, estudos, oportunidades profissionais, viagens e comunicação internacional.

O Xenoglossia foi criado para tornar a tradução mais acessível, permitindo que qualquer pessoa consiga compreender conteúdos em outros idiomas de forma rápida.

---

# Público-alvo

- Pessoas que falam apenas seu idioma nativo.
- Estudantes de idiomas.
- Profissionais que precisam traduzir documentos ou textos.
- Turistas e viajantes.
- Pessoas que desejam consumir conteúdos em outros idiomas.

---

# Solução

O Xenoglossia reúne diferentes formas de tradução em uma única aplicação.

### Funcionalidades

- Tradução de texto
- Tradução de imagens (OCR + IA)
- Tradução por voz
- Conversão de texto em áudio (Text-to-Speech)
- Autenticação de usuários
- Histórico de traduções

---

# Ferramentas utilizadas

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

## Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Gemini API
- gTTS
- OCR

---

# Resultados

Atualmente o projeto conta com:

- ✅ Aplicação totalmente funcional
- ✅ Tradução de texto
- ✅ Tradução de imagens
- ✅ Tradução por voz
- ✅ API REST
- ✅ Código Open Source

## Resultados em números

- **3** modalidades de tradução (Texto, Voz e Imagem)
- **2** aplicações (Frontend e Backend)
- **1** banco de dados PostgreSQL
- **1** API REST desenvolvida em FastAPI

---

# Instalação

## Frontend

Clone o repositório.

```bash
git clone https://github.com/Gabrielmedeiros1999/frontend_xenoglossia
```

Entre na pasta.

```bash
cd frontend_xenoglossia
```

Instale as dependências.

```bash
npm install
```

Crie um arquivo `.env`.

```env
VITE_API_URL=http://localhost:8000
```

Execute a aplicação.

```bash
npm run dev
```

---

## Backend

Clone o repositório.

```bash
git clone https://github.com/Gabrielmedeiros1999/xenoglossia_backend.git
```

Entre na pasta.

```bash
cd xenoglossia_backend
```

Crie um ambiente virtual.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

Instale as dependências.

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env`.

```env
DATABASE_URL=...
JWT_SECRET=...
```

Execute a API.

```bash
uvicorn backend:app --reload
```

---

# Tecnologias

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

## Inteligência Artificial

- Gemini API
- OCR
- gTTS

---

# Licença

Este projeto é distribuído sob a licença MIT.

---

# Autores

**Gabriel Caldeira Medeiros e Vinicius Dobke**

Projeto desenvolvido como iniciativa Open Source para facilitar a comunicação entre pessoas de diferentes idiomas.
