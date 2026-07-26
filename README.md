# Xenoglossia Backend

Backend do projeto open source de tradução, desenvolvido com FastAPI.

## Pré-requisitos

- Python 3.13.2
- pip

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Gabrielmedeiros1999/xenoglossia_backend.git
cd seu-repositorio
```
2. Crie um ambiente virtual:

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
 ```bash
pip install -r requirements.txt
 ```

4. Criar um arquivo .env
```env
DATABASE_URL=...
JWT_SECRET=...
 ```

5.Executando a aplicação
 ```bash
uvicorn backend:app --reload
 ```
