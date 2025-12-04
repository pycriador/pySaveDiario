# 🚀 pySaveDiário API

## Acesso Rápido

### 🌐 Documentação Interativa (Recomendado)
```
http://localhost:5000/api-docs
```

**Interface moderna com:**
- Dark mode
- Navegação lateral
- Tabs para Python, Node.js, PHP, cURL
- Syntax highlighting
- Exemplos prontos para copiar

---

## 📡 Base URL
```
http://localhost:5000/api
```

---

## 🔐 Autenticação

```bash
curl -X POST http://localhost:5000/api/auth/token \
  -u "email:password"
```

---

## 🎯 Endpoints Principais

| Recurso | Endpoint | GET | POST | PUT | DELETE |
|---------|----------|-----|------|-----|--------|
| **Sellers** | `/api/sellers` | ✅ | ✅ | ✅ | ✅ |
| **Categories** | `/api/categories` | ✅ | ✅ | ✅ | ✅ |
| **Manufacturers** | `/api/manufacturers` | ✅ | ✅ | ✅ | ✅ |
| **Templates** | `/api/templates` | ✅ | ✅ | - | - |
| **Offers** | `/api/offers` | ✅ | ✅ | - | - |
| **Users** | `/api/users` | ✅ | ✅ | - | - |

---

## 💡 Exemplo Rápido

```python
import requests

# 1. Obter token
response = requests.post(
    'http://localhost:5000/api/auth/token',
    auth=('admin@example.com', 'password')
)
token = response.json()['token']

# 2. Listar vendedores
response = requests.get('http://localhost:5000/api/sellers')
sellers = response.json()

# 3. Criar vendedor
headers = {'Authorization': f'Bearer {token}'}
data = {'name': 'Novo Vendedor', 'slug': 'novo-vendedor'}

response = requests.post(
    'http://localhost:5000/api/sellers',
    headers=headers,
    json=data
)
```

---

## 📚 Documentação Completa

### Formatos Disponíveis

1. **HTML Interativa (Melhor):**
   - URL: http://localhost:5000/api-docs
   - Recursos: Dark mode, tabs, syntax highlight

2. **Markdown Detalhada:**
   - Guia Completo: `../API_COMPLETE_GUIDE.md`
   - Quick Start: `../API_QUICK_START.md`
   - Documentação Full: `./API_DOCUMENTATION.md`

---

## 🧪 Testing

```bash
# Testar todos os endpoints
python scripts/test_api.py

# Popular dados iniciais
python scripts/seed_admin_data.py
```

---

## 📦 Setup

```bash
# 1. Aplicar migrations
flask db upgrade

# 2. Popular dados
python scripts/seed_admin_data.py

# 3. Criar usuário admin
python scripts/create_user.py

# 4. Iniciar servidor
python run.py

# 5. Acessar documentação
open http://localhost:5000/api-docs
```

---

## 🎨 Exemplos em Outras Linguagens

### Node.js
```javascript
const axios = require('axios');

const response = await axios.get('http://localhost:5000/api/sellers');
console.log(response.data);
```

### PHP
```php
$ch = curl_init('http://localhost:5000/api/sellers');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$sellers = json_decode($response, true);
```

### cURL
```bash
curl http://localhost:5000/api/sellers | jq
```

---

## ⚡ Features

- ✅ CRUD completo para todos os recursos
- ✅ Autenticação token-based
- ✅ Controle de permissões (Admin, Editor, Viewer)
- ✅ Validação de dados
- ✅ Mensagens de erro claras
- ✅ Documentação interativa
- ✅ Exemplos em 4 linguagens
- ✅ Scripts de teste automatizados

---

## 🔗 Links Úteis

- **Documentação HTML:** http://localhost:5000/api-docs
- **App Web:** http://localhost:5000
- **Guia Completo:** `../API_COMPLETE_GUIDE.md`
- **Quick Start:** `../API_QUICK_START.md`

---

**Versão:** 1.0  
**Última Atualização:** 19/11/2025

