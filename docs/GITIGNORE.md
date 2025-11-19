# 🔒 Arquivo .gitignore - pySave Diário

## 📝 O que é o .gitignore?

O arquivo `.gitignore` informa ao Git quais arquivos ou pastas devem ser **ignorados** e não enviados para o repositório. Isso é essencial para:

- 🔐 **Segurança**: Não commitar senhas, tokens e dados sensíveis
- 💾 **Tamanho**: Evitar arquivos grandes e desnecessários
- 🧹 **Limpeza**: Manter o repositório organizado
- 🤝 **Colaboração**: Evitar conflitos de arquivos locais

---

## 🛡️ Arquivos Sensíveis Protegidos

### 1. **Variáveis de Ambiente**
```
.env
.env.local
.env.*.local
*.env
```

**Por quê?** 
- Contém senhas, tokens de API, secret keys
- Cada desenvolvedor tem seu próprio `.env`
- Use `env.example` como template (este SIM pode ser commitado)

**Exemplo de .env:**
```bash
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost/db
MAIL_PASSWORD=senha-email
```

### 2. **Banco de Dados**
```
*.db
*.sqlite
*.sqlite3
app.db
instance/*.db
```

**Por quê?**
- Contém dados pessoais e sensíveis
- Pode ser muito grande
- Cada ambiente tem seu próprio banco
- Use migrations para sincronizar estrutura

**Localização:**
- `/instance/app.db` ✅ Ignorado

### 3. **Ambiente Virtual**
```
venv/
.venv/
ENV/
env/
```

**Por quê?**
- Pode ter centenas de MB
- Fácil de recriar com `pip install -r requirements.txt`
- Específico de cada máquina/SO

**Como recriar:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 📂 Arquivos de Cache e Temporários

### Python Cache
```
__pycache__/
*.pyc
*.pyo
*.pyd
```

**Por quê?**
- Gerados automaticamente pelo Python
- Específicos da versão do Python
- Recriados a cada execução

### Flask Cache
```
instance/
.webassets-cache
```

**Por quê?**
- Arquivos compilados e otimizados
- Regenerados automaticamente

---

## 💻 Arquivos de IDE

### VSCode
```
.vscode/
*.code-workspace
```

### PyCharm
```
.idea/
*.iml
```

### Sublime Text
```
*.sublime-project
*.sublime-workspace
```

**Por quê?**
- Configurações pessoais
- Cada dev usa seu próprio editor
- Evita conflitos de preferências

---

## 🖥️ Arquivos do Sistema Operacional

### macOS
```
.DS_Store
.AppleDouble
._*
```

### Windows
```
Thumbs.db
Desktop.ini
```

### Linux
```
*~
```

**Por quê?**
- Específicos do SO
- Não têm utilidade no repositório
- Poluem o histórico do Git

---

## 📊 Status Atual do Projeto

### ✅ Arquivos Ignorados Corretamente:
- `instance/app.db` (118 KB)
- `__pycache__/` (em todas as pastas)
- `.env` (variáveis de ambiente)
- `.venv/` (se existir)

### ✅ Arquivos Rastreados (commitados):
- `env.example` - Template de configuração
- `requirements.txt` - Dependências do projeto
- Todo o código fonte (`.py`, `.html`, `.css`, `.js`)
- Migrations (estrutura do banco)

---

## 🚀 Comandos Úteis

### Ver arquivos ignorados
```bash
git status --ignored
```

### Verificar se um arquivo está sendo ignorado
```bash
git check-ignore -v arquivo.ext
```

### Limpar cache do Git (se adicionou .gitignore depois)
```bash
git rm -r --cached .
git add .
git commit -m "chore: apply .gitignore rules"
```

### Ver tamanho do repositório
```bash
git count-objects -vH
```

---

## 📋 Checklist de Segurança

Antes de fazer commit, verifique:

- [ ] `.env` está no `.gitignore`?
- [ ] `app.db` não está sendo commitado?
- [ ] Não há senhas no código?
- [ ] Tokens e API keys estão em variáveis de ambiente?
- [ ] `.gitignore` está na raiz do projeto?

---

## 🔄 Boas Práticas

### 1. **Use env.example**
```bash
# env.example (commitado no Git)
SECRET_KEY=change-me
DATABASE_URL=sqlite:///instance/app.db
DEBUG=True
```

### 2. **Documente Variáveis**
```bash
# .env (NÃO commitado)
# Chave secreta do Flask (gere com: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=sua-chave-real-aqui

# URL do banco de dados
DATABASE_URL=postgresql://user:pass@localhost/pysave
```

### 3. **Mantenha requirements.txt atualizado**
```bash
pip freeze > requirements.txt
```

### 4. **Use .gitignore desde o início**
- Adicione `.gitignore` ANTES do primeiro commit
- Se esquecer, use `git rm --cached` para remover arquivos já commitados

---

## 🆘 Problemas Comuns

### Problema: Arquivo já foi commitado antes do .gitignore

**Solução:**
```bash
# Remover do Git (mantém o arquivo local)
git rm --cached arquivo.db

# Ou remover pasta inteira
git rm -r --cached __pycache__/

# Commitar a remoção
git commit -m "chore: remove sensitive files from git"
```

### Problema: .gitignore não está funcionando

**Solução:**
```bash
# Limpar cache do Git
git rm -r --cached .
git add .
git commit -m "chore: fix .gitignore"
```

### Problema: Arquivo sensível já foi para o GitHub

**Ação URGENTE:**
1. Revogue/troque as credenciais imediatamente
2. Use `git filter-branch` ou BFG Repo-Cleaner para remover do histórico
3. Force push (cuidado!)

---

## 📚 Referências

- [GitHub .gitignore templates](https://github.com/github/gitignore)
- [Python .gitignore oficial](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Flask security best practices](https://flask.palletsprojects.com/en/latest/security/)

---

## ✅ Status

- **Criado**: 19 de Novembro de 2025
- **Status**: ✅ Funcionando corretamente
- **Proteção**: 🔒 Dados sensíveis protegidos

**Última verificação:** Todos os arquivos sensíveis estão sendo ignorados corretamente.

---

**⚠️ IMPORTANTE**: Nunca commite arquivos `.env`, senhas, tokens ou dados sensíveis!

