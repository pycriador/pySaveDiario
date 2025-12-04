# 🐛 BUGFIX: Edição de Usuário Removendo Permissões ADMIN

## 📝 Relatório do Bug

**Reportado por:** Usuário  
**Data:** 04/12/2025  
**Severidade:** 🔴 **CRÍTICA** (Segurança)

### Descrição
Ao editar as configurações do próprio perfil em `/usuarios/<id>/editar`, o sistema estava permitindo que o usuário modificasse seu próprio papel (role), resultando na perda de privilégios ADMIN.

### Sintoma
```
Usuário ADMIN edita o próprio perfil
   ↓
Salva as informações (telefone, redes sociais, etc.)
   ↓
Sistema muda papel de ADMIN para MEMBER
   ↓
Perde acesso administrativo 
```

---

## 🔍 Causa Raiz

### Problema no Código

**Arquivo:** `app/routes/web.py` - função `edit_user()`

```python
# ❌ CÓDIGO PROBLEMÁTICO
@web_bp.route("/usuarios/<int:user_id>/editar", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    
    if form.validate_on_submit():
        # ... outras atualizações ...
        
        # Only admin can change role
        if current_user.role == RoleEnum.ADMIN:
            user.role = RoleEnum(form.role.data)  # ⚠️  PERIGO!
        
        db.session.commit()
```

**Problemas identificados:**

1. **Sem verificação de auto-edição:**
   - O código permitia que admin mudasse o papel de `user`
   - Não verificava se `user == current_user`
   - Quando admin edita próprio perfil, muda o próprio papel!

2. **Campo de papel visível no formulário:**
   - Template mostrava campo `role` quando admin edita qualquer perfil
   - Incluindo o próprio perfil
   - Permitia modificação acidental

3. **Sem proteção no commit:**
   - `db.session.commit()` persistia qualquer mudança
   - Não verificava se `current_user.role` foi alterado
   - Sem rollback em caso de mudança não autorizada

---

## ✅ Correções Implementadas

### Correção #1: Proteção Contra Auto-Edição

**Arquivo:** `app/routes/web.py`

```python
# ✅ CÓDIGO CORRIGIDO
@web_bp.route("/usuarios/<int:user_id>/editar", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # CRITICAL: Check if user is editing themselves
    is_editing_self = (current_user.id == user.id)
    
    # CRITICAL: Store original role to prevent accidental changes
    original_user_role = user.role
    original_current_user_role = current_user.role
    
    from ..forms import UserEditForm
    form = UserEditForm(obj=user)
    
    # If user is editing own profile, remove role and is_active fields
    if is_editing_self:
        if hasattr(form, 'role'):
            delattr(form, 'role')
        if hasattr(form, 'is_active'):
            delattr(form, 'is_active')
    
    if form.validate_on_submit():
        # ... outras atualizações ...
        
        # CRITICAL: Only admin can change role, but NEVER allow changing own role
        if current_user.role == RoleEnum.ADMIN and not is_editing_self:
            # Admin editing another user - allow role change
            user.role = RoleEnum(form.role.data)
        elif is_editing_self:
            # User editing own profile - NEVER change role
            user.role = original_user_role
            print(f"🔒 PROTECTION: Prevented self role change for {user.email}")
        
        # ... outras atualizações ...
        
        # CRITICAL: Flush and verify current_user wasn't modified
        db.session.flush()
        
        if current_user.role != original_current_user_role:
            print(f"⚠️  WARNING: current_user.role changed! Reverting...")
            current_user.role = original_current_user_role
        
        db.session.commit()
```

**Proteções adicionadas:**
1. ✅ Detecta se está editando próprio perfil (`is_editing_self`)
2. ✅ Armazena papel original antes de qualquer mudança
3. ✅ Remove campos `role` e `is_active` do formulário quando auto-edição
4. ✅ Bloqueia mudança de papel quando `is_editing_self`
5. ✅ Usa `flush()` + verificação antes de `commit()`
6. ✅ Reverte automaticamente mudanças não autorizadas

---

### Correção #2: Campo de Papel Condicional no Template

**Arquivo:** `app/templates/user_edit.html`

**Antes:**
```html
<!-- ❌ Sempre mostra campo de papel -->
<div class="col-md-6">
  <label>Papel</label>
  {{ form.role(class="form-select", disabled=current_user.role.value != 'admin') }}
</div>
```

**Depois:**
```html
<!-- ✅ Mostra campo APENAS se admin editando OUTRO usuário -->
{% if current_user.id != user.id and current_user.role.value == 'admin' %}
<div class="col-md-6">
  <label>Papel</label>
  {{ form.role(class="form-select") }}
  <small class="text-muted">Papel do usuário no sistema</small>
</div>
{% else %}
<!-- Mostra badge read-only -->
<div class="col-md-6">
  <label>Papel Atual</label>
  <div>
    {% if user.role.value == 'admin' %}
    <span class="badge bg-danger" style="font-size: 1rem;">
      <i class="bi bi-star-fill"></i> Administrador
    </span>
    {% elif user.role.value == 'editor' %}
    <span class="badge bg-primary" style="font-size: 1rem;">
      <i class="bi bi-pencil-fill"></i> Editor
    </span>
    {% else %}
    <span class="badge bg-secondary" style="font-size: 1rem;">
      <i class="bi bi-person-fill"></i> Membro
    </span>
    {% endif %}
  </div>
  <small class="text-muted">
    <i class="bi bi-lock"></i> Você não pode alterar seu próprio papel
  </small>
</div>
{% endif %}
```

**Benefícios:**
1. ✅ Campo de papel **não aparece** quando usuário edita próprio perfil
2. ✅ Mostra papel atual como **badge read-only**
3. ✅ Mensagem clara: "Você não pode alterar seu próprio papel"
4. ✅ Admin ainda pode editar papel de **outros** usuários

---

### Correção #3: Remoção Programática de Campos

**Arquivo:** `app/routes/web.py`

```python
# If user is editing own profile, remove role and is_active fields
if is_editing_self:
    if hasattr(form, 'role'):
        delattr(form, 'role')
    if hasattr(form, 'is_active'):
        delattr(form, 'is_active')
```

**Benefício:**
- Remove campos do objeto `form` programaticamente
- Previne validação e processamento desses campos
- Proteção adicional mesmo se HTML for manipulado

---

## 🔒 Matriz de Permissões

| Cenário | Pode Mudar Papel? | Pode Mudar is_active? | Campos Visíveis? |
|---------|-------------------|----------------------|------------------|
| Admin editando outro usuário | ✅ Sim | ✅ Sim | ✅ Sim |
| Admin editando próprio perfil | ❌ Não | ❌ Não | ❌ Não (badge apenas) |
| Editor editando próprio perfil | ❌ Não | ❌ Não | ❌ Não (badge apenas) |
| Membro editando próprio perfil | ❌ Não | ❌ Não | ❌ Não (badge apenas) |

---

## 🧪 Testes Realizados

### ✅ Teste 1: Admin Edita Próprio Perfil

```
1. Login como willian.o.jesus@gmail.com (ADMIN)
2. Clicar em "Editar Meu Perfil"
3. Verificar que campo "Papel" NÃO aparece
4. Ver badge "Administrador" read-only
5. Mudar telefone, redes sociais, etc.
6. Clicar em "Salvar"
7. Verificar papel continua ADMIN ✅
```

**Resultado:** ✅ Papel mantido como ADMIN

### ✅ Teste 2: Admin Edita Outro Usuário

```
1. Login como willian.o.jesus@gmail.com (ADMIN)
2. Ir para /usuarios
3. Clicar em "Editar" em outro usuário
4. Verificar que campo "Papel" APARECE
5. Mudar papel de MEMBER para EDITOR
6. Clicar em "Salvar"
7. Verificar que outro usuário virou EDITOR ✅
8. Verificar que admin continua ADMIN ✅
```

**Resultado:** ✅ Outro usuário mudou, admin mantido

### ✅ Teste 3: Tentativa de Manipulação HTML

```
1. Login como admin
2. Editar próprio perfil
3. Abrir DevTools
4. Tentar adicionar campo <select name="role">
5. Mudar valor para "member"
6. Submit
7. Verificar papel continua ADMIN ✅
```

**Resultado:** ✅ Proteção backend impediu mudança

---

## 🛡️ Camadas de Proteção

| Camada | Proteção | Implementação |
|--------|----------|---------------|
| 1️⃣ UI | Campo não aparece | Template condicional |
| 2️⃣ Form | Campo removido do form | `delattr(form, 'role')` |
| 3️⃣ Backend | Verificação `is_editing_self` | Código Python |
| 4️⃣ Commit | Flush + verificação | `db.session.flush()` + check |

**Resultado:** 🔐 **4 camadas de proteção** contra mudança acidental de papel

---

## 📊 Arquivos Modificados

| Arquivo | Modificação | Linhas |
|---------|-------------|--------|
| `app/routes/web.py` | Proteção anti auto-edição | 210-275 |
| `app/templates/user_edit.html` | Campo condicional de papel | 42-72 |
| `scripts/make_admin.py` | Script para restaurar admin | Todo |
| `docs/BUGFIX_USER_EDIT_ROLE.md` | Documentação | Este arquivo |

---

## 🚀 Como Aplicar

### 1. Backup
```bash
cp instance/app.db instance/app.db.backup
```

### 2. Restaurar Admin (se necessário)
```bash
python scripts/make_admin.py SEU_EMAIL@gmail.com
```

### 3. Testar
```bash
# 1. Fazer login como admin
# 2. Editar próprio perfil
# 3. Verificar que campo "Papel" não aparece
# 4. Salvar e verificar que continua admin
```

---

## 📈 Status

| Item | Status |
|------|--------|
| Bug identificado | ✅ |
| Causa raiz encontrada | ✅ |
| Proteção UI implementada | ✅ |
| Proteção Form implementada | ✅ |
| Proteção Backend implementada | ✅ |
| Proteção Commit implementada | ✅ |
| Testes aprovados | ✅ |
| Documentação criada | ✅ |
| Usuário restaurado | ✅ |

**Status Geral:** ✅ **RESOLVIDO**

---

## 🎯 Prevenção Futura

### Regra de Ouro
> **"Usuários NUNCA devem poder mudar o próprio papel (role), mesmo que sejam admin."**

### Checklist para Novos Recursos
- [ ] Verificar se usuário está editando próprio perfil
- [ ] Remover campos sensíveis do formulário quando auto-edição
- [ ] Adicionar proteção backend contra mudanças não autorizadas
- [ ] Usar `flush()` antes de `commit()` para verificações
- [ ] Armazenar valores originais antes de modificar
- [ ] Adicionar logs de segurança
- [ ] Testar com manipulação HTML/DevTools

---

## 🔗 Relacionado

- `docs/USER_ROLE_PROTECTION.md` - Proteção em rotas admin
- `docs/BUGFIX_ADMIN_ROLE.md` - Bug em `/admin/social-networks`
- `scripts/make_admin.py` - Script para promover usuários

---

**Corrigido por:** IA Assistant  
**Data:** 04/12/2025 23:58  
**Tempo:** ~30 minutos  
**Prioridade:** 🔴 CRÍTICA  
**Status:** ✅ **FECHADO E TESTADO**

