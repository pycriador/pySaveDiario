# 🔍 Sistema de Filtros para Usuários

## 📝 Descrição

Implementação de sistema de filtros avançados para a página `/usuarios`, permitindo busca e filtragem detalhada por múltiplos critérios.

**Data de Implementação:** 04/12/2025

---

## ✨ Funcionalidades

### 1. **Busca por Texto** 🔎
Busca em múltiplos campos simultaneamente:
- ✅ **Email** - `user@example.com`
- ✅ **Nome** - `João Silva`
- ✅ **Telefone** - `(11) 98765-4321`
- ✅ **Endereço** - `São Paulo, SP`
- ✅ **Website** - `https://site.com`
- ✅ **Instagram** - `@usuario`
- ✅ **Facebook** - `facebook.com/usuario`
- ✅ **Twitter/X** - `@usuario`
- ✅ **LinkedIn** - `linkedin.com/in/usuario`
- ✅ **YouTube** - `youtube.com/@usuario`
- ✅ **TikTok** - `@usuario`

**Tipo de busca:** Case-insensitive (ignora maiúsculas/minúsculas)  
**Operador:** `ILIKE` (SQL) - busca parcial

**Exemplos:**
```
Busca: "gmail"
Resultado: Encontra todos os emails @gmail.com

Busca: "@usuario"
Resultado: Encontra redes sociais com @usuario

Busca: "São Paulo"
Resultado: Encontra endereços em São Paulo
```

---

### 2. **Filtro por Papel** 👥
Filtra usuários por papel no sistema:
- 🌟 **Administrador** (`admin`)
- ✏️ **Editor** (`editor`)
- 👤 **Membro** (`member`)
- 📋 **Todos** (sem filtro)

---

### 3. **Filtro de Status** ⚡
Toggle para exibir apenas usuários ativos:
- ✅ **Ativos** - `is_active = True` (padrão)
- 🔴 **Todos** - Inclui inativos

---

## 🎨 Interface

### Painel de Filtros
```
┌─────────────────────────────────────────────────────┐
│ 🔍 Filtros                         [Limpar Filtros] │
├─────────────────────────────────────────────────────┤
│                                                       │
│ 🔎 Buscar:          🛡️ Papel:       ⚡ Status:      │
│ [_____________]    [Todos▼]       [✓] Apenas ativos │
│ Busca em email,                                      │
│ nome, telefone...                                    │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Implementação Técnica

### Backend (Python/Flask)

**Arquivo:** `app/routes/web.py`

```python
@web_bp.route("/usuarios", methods=["GET", "POST"])
def users():
    # Get filter parameters from URL
    search = request.args.get("search", "").strip()
    role_filter = request.args.get("role", "")
    active_only = request.args.get("active_only", "true").lower() == "true"
    
    # Build query
    query = User.query
    
    # Apply search filter (email, name, social media)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                User.email.ilike(search_pattern),
                User.display_name.ilike(search_pattern),
                User.phone.ilike(search_pattern),
                User.address.ilike(search_pattern),
                User.website.ilike(search_pattern),
                User.instagram.ilike(search_pattern),
                User.facebook.ilike(search_pattern),
                User.twitter.ilike(search_pattern),
                User.linkedin.ilike(search_pattern),
                User.youtube.ilike(search_pattern),
                User.tiktok.ilike(search_pattern),
            )
        )
    
    # Apply role filter
    if role_filter:
        try:
            query = query.filter_by(role=RoleEnum(role_filter))
        except ValueError:
            role_filter = ""
    
    # Apply active filter
    if active_only:
        query = query.filter_by(is_active=True)
    
    # Get results
    users = query.order_by(User.created_at.desc()).all()
```

**Características:**
- ✅ Busca case-insensitive (`ilike`)
- ✅ Busca parcial (wildcard `%`)
- ✅ Múltiplos campos com `db.or_()`
- ✅ Validação de enum para papel
- ✅ Filtro de ativos como padrão

---

### Frontend (JavaScript)

**Arquivo:** `app/templates/users.html`

```javascript
// Update filters dynamically
function updateFilters() {
  const form = document.getElementById('filterForm');
  const params = new URLSearchParams();
  
  // Get search value
  const search = document.getElementById('search').value.trim();
  if (search) {
    params.set('search', search);
  }
  
  // Get role value
  const role = document.getElementById('role').value;
  if (role) {
    params.set('role', role);
  }
  
  // Get active_only value
  const activeOnly = document.getElementById('active_only').checked;
  params.set('active_only', activeOnly ? 'true' : 'false');
  
  // Update URL
  const newUrl = window.location.pathname + '?' + params.toString();
  window.location.href = newUrl;
}

// Clear all filters
function clearFilters() {
  window.location.href = window.location.pathname;
}

// Debounce search input
let searchTimeout;
const searchInput = document.getElementById('search');
if (searchInput) {
  searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(function() {
      updateFilters();
    }, 500); // Wait 500ms after user stops typing
  });
}
```

**Características:**
- ✅ Debounce de 500ms na busca (evita requisições excessivas)
- ✅ Atualização automática da URL
- ✅ Preservação de filtros ao navegar/recarregar
- ✅ Botão de limpar filtros

---

## 📊 Exemplos de URL

### URL Base
```
/usuarios
```

### Busca por Gmail
```
/usuarios?search=gmail&active_only=true
```

### Apenas Administradores
```
/usuarios?role=admin&active_only=true
```

### Usuários com Instagram
```
/usuarios?search=instagram.com&active_only=true
```

### Todos os Usuários (incluindo inativos)
```
/usuarios?active_only=false
```

### Busca Complexa
```
/usuarios?search=são+paulo&role=editor&active_only=true
```

---

## 🎯 Casos de Uso

### 1. Encontrar Usuário por Email
```
1. Digite parte do email: "gmail"
2. Ver todos os usuários @gmail.com
```

### 2. Listar Administradores
```
1. Selecione "Administrador" no filtro de papel
2. Ver apenas admins
```

### 3. Encontrar Usuários de São Paulo
```
1. Digite "São Paulo" na busca
2. Ver usuários com SP no endereço
```

### 4. Ver Usuários com Instagram
```
1. Digite "@" ou "instagram" na busca
2. Ver usuários com Instagram cadastrado
```

### 5. Auditoria de Usuários Inativos
```
1. Desmarque "Apenas usuários ativos"
2. Ver todos (incluindo inativos)
```

---

## 🔍 Lógica de Busca

### Operador OR
Todos os campos são buscados com `OR`:
```sql
WHERE 
  email ILIKE '%search%' OR
  display_name ILIKE '%search%' OR
  phone ILIKE '%search%' OR
  ...
```

**Resultado:** Retorna usuário se **qualquer** campo contiver o texto buscado.

### Combinação de Filtros
Os filtros são aplicados com `AND`:
```sql
WHERE 
  (email ILIKE '%search%' OR display_name ILIKE '%search%') AND
  role = 'admin' AND
  is_active = true
```

**Resultado:** Retorna usuário que atenda **todos** os critérios selecionados.

---

## 📈 Performance

### Otimizações
1. ✅ **Debounce** - Aguarda 500ms após digitação
2. ✅ **Índices** - Campos principais indexados no banco
3. ✅ **Case-insensitive** - Usa `ILIKE` nativamente
4. ✅ **Lazy loading** - Dados carregados sob demanda

### Recomendações Futuras
- [ ] Adicionar paginação (se > 100 usuários)
- [ ] Implementar cache de resultados
- [ ] Adicionar busca por data de criação
- [ ] Implementar busca por grupos

---

## 🎨 Tema Escuro/Claro

O painel de filtros é totalmente compatível com ambos os temas:

```css
.panel .form-control {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

.panel .form-control:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
}
```

---

## ✅ Testes

### Teste 1: Busca por Email
```
Input: "gmail"
Expected: Lista todos @gmail.com
Status: ✅ Pass
```

### Teste 2: Busca por Nome
```
Input: "João"
Expected: Lista usuários com "João" no nome
Status: ✅ Pass
```

### Teste 3: Filtro de Papel
```
Select: "Administrador"
Expected: Apenas admins
Status: ✅ Pass
```

### Teste 4: Busca + Papel
```
Input: "gmail" + Select: "Editor"
Expected: Editores com @gmail.com
Status: ✅ Pass
```

### Teste 5: Toggle Ativos
```
Uncheck: "Apenas usuários ativos"
Expected: Todos os usuários
Status: ✅ Pass
```

### Teste 6: Limpar Filtros
```
Action: Clicar em "Limpar"
Expected: Remove todos os filtros
Status: ✅ Pass
```

### Teste 7: URL Manual
```
Navigate: /usuarios?search=teste&role=admin
Expected: Filtros aplicados automaticamente
Status: ✅ Pass
```

---

## 📝 Checklist de Implementação

- [x] Backend: Rota com parâmetros de filtro
- [x] Backend: Query com `db.or_()` para múltiplos campos
- [x] Backend: Validação de enum de papel
- [x] Backend: Filtro de ativos/inativos
- [x] Frontend: Formulário de filtros
- [x] Frontend: JavaScript para atualização dinâmica
- [x] Frontend: Debounce na busca
- [x] Frontend: Botão de limpar filtros
- [x] Frontend: CSS para tema claro/escuro
- [x] Frontend: Contador de resultados
- [x] Documentação: Criada
- [x] Testes: Aprovados

---

## 🔗 Padrão Utilizado

Este sistema de filtros segue o mesmo padrão implementado em:
- ✅ `/ofertas` - Filtros de ofertas
- ✅ `/cupons` - Filtros de cupons
- ✅ `/templates` - Filtros de templates

**Benefício:** Consistência na experiência do usuário em todo o sistema.

---

## 🚀 Como Usar

### Para Usuários

1. **Acesse** `/usuarios`
2. **Digite** no campo de busca ou selecione filtros
3. **Aguarde** 500ms (busca automática)
4. **Ou clique** nos dropdowns para filtrar
5. **Use** o botão "Limpar" para resetar

### Para Desenvolvedores

```python
# Buscar usuários com filtros
from app.models import User

# Por email
users = User.query.filter(User.email.ilike('%gmail%')).all()

# Por papel
from app.models import RoleEnum
admins = User.query.filter_by(role=RoleEnum.ADMIN).all()

# Ativos apenas
active_users = User.query.filter_by(is_active=True).all()

# Combinado
results = User.query.filter(
    User.email.ilike('%search%'),
    User.role == RoleEnum.ADMIN,
    User.is_active == True
).all()
```

---

**Status:** ✅ **Implementado e Testado**  
**Versão:** 1.0  
**Última Atualização:** 04/12/2025

