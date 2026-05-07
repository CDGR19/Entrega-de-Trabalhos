# CR App — Demo

Demonstração completa do projeto CR App com MundoTêxtil e BP.

## Como executar

### Instalar dependências (uma vez)
```bash
pip install flask flask-sqlalchemy
```

### Iniciar tudo de uma vez
```bash
python iniciar.py
```

O browser abre automaticamente. Os dados reais são importados automaticamente ao iniciar.

### Acesso
- **CR App (Hub):** http://localhost:5000
- **MundoTêxtil:** http://localhost:5001
- **BP:** http://localhost:5002

## Estrutura

```
demo/
├── cr-app/           ← Hub principal (HTML estático)
│   ├── index.html    ← Ecrã de entrada + cards dos projetos
│   ├── bg.jpg        ← Fundo dos cards
│   ├── ribeiro.png   ← Fundo do login
│   └── cr-logo.png   ← Logo CR no ecrã de entrada
├── mundotextil/      ← Flask app porta 5001
│   ├── app.py
│   ├── dados.json    ← Dados reais importados automaticamente
│   └── templates/
│       ├── index.html
│       └── MDT.png
├── bp/               ← Flask app porta 5002
│   ├── app.py
│   ├── dados.json    ← Dados reais importados automaticamente
│   └── templates/
│       ├── index.html
│       └── BP.png
└── iniciar.py        ← Lança tudo de uma vez
```

## Funcionalidades

- Ecrã de entrada com "Olá Carlos" e botão **Entrar** (sem password)
- **MundoTêxtil:** banco de horas, filtros, exportação JSON/Excel
- **BP:** registo entradas/saídas, taxa/hora configurável, exportação JSON/Excel
- Botão **Sair** em cada app volta ao CR App
