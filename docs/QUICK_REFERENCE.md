# 🚀 Referência Rápida - pySave Diário

## 📋 Comandos Git Essenciais

### Ver status do repositório
```bash
git status
```

### Adicionar arquivos
```bash
# Adicionar todos os arquivos modificados
git add .

# Adicionar arquivo específico
git add arquivo.py

# Adicionar apenas os templates
git add app/templates/
```

### Fazer commit
```bash
# Commit das melhorias visuais
git commit -m "feat: add modern UI with Bootstrap Icons and modals"

# Commit do .gitignore
git commit -m "chore: add .gitignore and remove sensitive files"
```

### Enviar para o repositório
```bash
git push origin main
```

---

## 🔒 Arquivos Protegidos pelo .gitignore

### ✅ O que NÃO será commitado:
- `.env` - Variáveis de ambiente (senhas, tokens)
- `instance/app.db` - Banco de dados local
- `__pycache__/` - Cache do Python
- `.venv/` - Ambiente virtual
- `*.pyc` - Arquivos compilados Python
- `.DS_Store` - Arquivos do macOS
- `.vscode/` - Configurações do editor

### ✅ O que PODE ser commitado:
- `env.example` - Template de configuração
- `.gitignore` - Regras de exclusão
- `requirements.txt` - Lista de dependências
- Todo o código fonte
- Templates HTML, CSS, JavaScript
- Migrations (estrutura do banco)
- README e documentação

---

## 🛠️ Comandos Python/Flask

### Criar ambiente virtual
```bash
python -m venv .venv
```

### Ativar ambiente virtual
```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Atualizar dependências
```bash
pip freeze > requirements.txt
```

### Rodar a aplicação
```bash
python run.py
```

### Criar admin (se necessário)
```bash
python scripts/create_admin.py
```

---

## 🎨 Estrutura do Projeto

```
pySaveDiario/
├── .env                    # ❌ NÃO commitado (ignorado)
├── .gitignore             # ✅ Commitado
├── env.example            # ✅ Commitado (template)
├── requirements.txt       # ✅ Commitado
├── run.py                 # ✅ Commitado
├── GITIGNORE.md          # ✅ Documentação
├── QUICK_REFERENCE.md    # ✅ Este arquivo
│
├── instance/
│   └── app.db            # ❌ NÃO commitado (ignorado)
│
├── app/
│   ├── __pycache__/      # ❌ NÃO commitado (ignorado)
│   ├── __init__.py       # ✅ Commitado
│   ├── models.py         # ✅ Commitado
│   ├── routes/           # ✅ Commitado
│   ├── templates/        # ✅ Commitado
│   └── static/           # ✅ Commitado
│
├── migrations/
│   ├── __pycache__/      # ❌ NÃO commitado (ignorado)
│   └── versions/         # ✅ Commitado
│
└── scripts/
    ├── __pycache__/      # ❌ NÃO commitado (ignorado)
    └── create_admin.py   # ✅ Commitado
```

---

## 🔐 Segurança

### ⚠️ NUNCA commite:
- Senhas
- Tokens de API
- Chaves secretas (SECRET_KEY)
- Credenciais de banco de dados
- Arquivos .env
- Banco de dados com dados reais

### ✅ Use variáveis de ambiente:
```python
# ❌ ERRADO - Senha no código
DATABASE_URL = "postgresql://user:senha123@localhost/db"

# ✅ CORRETO - Senha em variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
```

### ✅ Use env.example como template:
```bash
# env.example (pode commitar)
SECRET_KEY=change-me
DATABASE_URL=sqlite:///instance/app.db

# .env (NÃO commitar)
SECRET_KEY=chave-secreta-real-aqui
DATABASE_URL=postgresql://user:senha@localhost/pysave
```

---

## 🚨 Problemas Comuns

### 1. Arquivo sensível foi commitado

**Solução:**
```bash
# Remover do Git (mantém local)
git rm --cached arquivo_sensivel.env

# Commitar a remoção
git commit -m "chore: remove sensitive file"

# IMPORTANTE: Troque a senha/token imediatamente!
```

### 2. .gitignore não está funcionando

**Solução:**
```bash
# Limpar cache do Git
git rm -r --cached .
git add .
git commit -m "chore: fix .gitignore"
```

### 3. Como recriar o banco de dados

```bash
# Deletar banco antigo
rm instance/app.db

# Recriar com migrations
flask db upgrade

# Criar admin novamente
python scripts/create_admin.py
```

### 4. Dependências não instaladas

```bash
# Ativar ambiente virtual primeiro
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 📦 Workflow Recomendado

### 1. Começar a trabalhar
```bash
# Atualizar código
git pull

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar dependências
pip install -r requirements.txt

# Rodar aplicação
python run.py
```

### 2. Durante o desenvolvimento
```bash
# Ver mudanças
git status

# Testar a aplicação
python run.py
```

### 3. Finalizar trabalho
```bash
# Adicionar mudanças
git add .

# Fazer commit
git commit -m "feat: add new feature"

# Enviar para repositório
git push origin main

# Desativar ambiente virtual
deactivate
```

---

## 🎯 Checklist Antes de Commitar

- [ ] Código está funcionando?
- [ ] Não há senhas ou tokens no código?
- [ ] `.env` está no `.gitignore`?
- [ ] `app.db` não está sendo commitado?
- [ ] `requirements.txt` está atualizado?
- [ ] Mensagem de commit é clara?
- [ ] Testei localmente?

---

## 📚 Links Úteis

### Documentação do Projeto
- `README.md` - Visão geral do projeto
- `GITIGNORE.md` - Guia completo do .gitignore
- `QUICK_REFERENCE.md` - Este arquivo

### Tecnologias
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Bootstrap 5](https://getbootstrap.com/) - Framework CSS
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Ícones
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

### Git
- [Git Docs](https://git-scm.com/doc)
- [GitHub .gitignore templates](https://github.com/github/gitignore)

---

## 💡 Dicas

### Gerar SECRET_KEY segura
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Ver tamanho do repositório
```bash
git count-objects -vH
```

### Ver histórico de commits
```bash
git log --oneline
```

### Desfazer último commit (mantém mudanças)
```bash
git reset --soft HEAD~1
```

### Ver diferenças antes de commitar
```bash
git diff
```

---

## ✅ Status Atual do Projeto

- ✅ `.gitignore` configurado
- ✅ Arquivos sensíveis protegidos
- ✅ UI moderna implementada
- ✅ Bootstrap Icons integrado
- ✅ Modals funcionando
- ✅ Tema claro/escuro
- ✅ Responsivo

---

## 🆘 Suporte

Se encontrar problemas:

1. Consulte `GITIGNORE.md` para problemas com Git
2. Consulte documentação do Flask
3. Verifique se `.env` está configurado
4. Verifique se ambiente virtual está ativado
5. Verifique se dependências estão instaladas

---

**Última atualização**: 19 de Novembro de 2025
**Versão**: 2.0

