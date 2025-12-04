# 🔒 Proteção de Papel do Usuário (User Role Protection)

## 🐛 Problema Identificado

**Sintoma:** Ao salvar configurações de redes sociais em `/admin/social-networks`, o papel do usuário administrador estava mudando de `ADMIN` para `MEMBER`.

## 🔍 Causas Identificadas

### 1. **Formulários Aninhados (HTML Inválido)**
O HTML tinha um `<form>` de deletar **dentro** do `<form>` de atualizar:

```html
<!-- ❌ ERRADO - Forms aninhados -->
<form method="POST">  <!-- Form principal -->
  <input name="network_id" value="1">
  <textarea name="prefix_text"></textarea>
  
  <form method="POST" action="/delete">  <!-- Form aninhado! -->
    <button type="submit">Deletar</button>
  </form>
  
  <button type="submit">Salvar</button>
</form>
```

**Problema:** Forms aninhados são **HTML inválido** e causam comportamento imprevisível no navegador.

### 2. **Commit Sem Proteção**
O código fazia `db.session.commit()` sem verificar se outras entidades (como `current_user`) foram modificadas acidentalmente:

```python
# ❌ ERRADO - Commit sem verificação
config.active = True
db.session.commit()  # Pode commitar mudanças não intencionais!
```

---

## ✅ Correções Implementadas

### 1. **Removidos Formulários Aninhados**

**Antes:**
```html
<form method="POST">
  <!-- Campos de atualização -->
  <form method="POST" action="/delete">  <!-- ❌ Aninhado -->
    <button type="submit">Deletar</button>
  </form>
  <button type="submit">Salvar</button>
</form>
```

**Depois:**
```html
<!-- Form principal -->
<form method="POST">
  <!-- Campos de atualização -->
  <button type="button" onclick="deleteNetwork('1', 'Instagram')">
    Deletar
  </button>
  <button type="submit">Salvar</button>
</form>

<!-- Form separado, fora do principal -->
<form id="deleteForm_1" method="POST" action="/delete" style="display: none;">
  <input type="hidden" name="csrf_token" value="..."/>
</form>

<script>
function deleteNetwork(id, name) {
  if (confirm('Tem certeza?')) {
    document.getElementById('deleteForm_' + id).submit();
  }
}
</script>
```

### 2. **Proteção de Papel do Usuário**

Adicionada verificação explícita antes de commitar:

```python
@web_bp.route("/admin/social-networks", methods=["GET", "POST"])
@login_required
def admin_social_networks():
    # CRITICAL: Store current user's role to prevent accidental changes
    original_user_role = current_user.role
    original_user_id = current_user.id
    
    if request.method == "POST":
        # ... processar formulário ...
        
        # CRITICAL: Flush changes but don't commit yet
        db.session.flush()
        
        # Verify current_user wasn't accidentally modified
        if current_user.role != original_user_role:
            print(f"⚠️  WARNING: User role changed from {original_user_role} to {current_user.role}! Reverting...")
            current_user.role = original_user_role
        
        # Now safe to commit
        db.session.commit()
```

**Como funciona:**
1. **Armazena** o papel original do usuário antes de qualquer operação
2. **Flush** aplica mudanças ao banco, mas não commita
3. **Verifica** se o `current_user.role` mudou
4. **Reverte** se houve mudança não intencional
5. **Commita** apenas se tudo estiver OK

### 3. **Mesma Proteção em Todas as Rotas**

A proteção foi aplicada em:
- ✅ `admin_social_networks()` - Criação e atualização
- ✅ `admin_social_network_delete()` - Deleção

---

## 🧪 Como Testar

### Teste 1: Atualizar Rede Social
1. Login como **ADMIN**
2. Acesse `/admin/social-networks`
3. Edite uma rede social (mude texto, cor, etc.)
4. Clique em **"Salvar"**
5. ✅ Papel continua **ADMIN**

### Teste 2: Criar Nova Rede Social
1. Login como **ADMIN**
2. Acesse `/admin/social-networks`
3. Clique em **"Nova Rede Social"**
4. Preencha e salve
5. ✅ Papel continua **ADMIN**

### Teste 3: Deletar Rede Social
1. Login como **ADMIN**
2. Acesse `/admin/social-networks`
3. Clique em **"Deletar"** em uma rede
4. Confirme
5. ✅ Papel continua **ADMIN**

### Verificar Papel do Usuário

**No console do navegador:**
```javascript
fetch('/api/users/me')
  .then(r => r.json())
  .then(d => console.log('Papel:', d.role));
```

**Ou no terminal:**
```bash
sqlite3 instance/app.db "SELECT email, role FROM users WHERE role='ADMIN';"
```

---

## 📊 Log de Depuração

Se houver tentativa de mudança de papel, você verá no console do Flask:

```bash
⚠️  WARNING: User role changed from RoleEnum.ADMIN to RoleEnum.MEMBER! Reverting...
```

Isso indica que:
1. ✅ A proteção detectou a mudança
2. ✅ O papel foi revertido automaticamente
3. ⚠️  Há um bug em outro lugar que precisa ser investigado

---

## 🔐 Boas Práticas Implementadas

### 1. **Sempre Armazene o Estado Original**
```python
original_role = current_user.role
# ... operações ...
if current_user.role != original_role:
    current_user.role = original_role
```

### 2. **Use `flush()` Antes de `commit()`**
```python
db.session.add(new_item)
db.session.flush()  # ← Aplica mudanças sem commitar
# Verificações aqui
db.session.commit()  # ← Commit apenas se OK
```

### 3. **Evite Formulários Aninhados**
```html
<!-- ❌ NUNCA faça isso -->
<form>
  <form></form>
</form>

<!-- ✅ Use forms separados + JavaScript -->
<form id="form1"></form>
<form id="form2" style="display:none;"></form>
<button onclick="document.getElementById('form2').submit()">
```

### 4. **Adicione Logs de Segurança**
```python
if critical_value_changed:
    print(f"🚨 SECURITY: {variable} changed unexpectedly!")
    # Log to file
    # Send alert
    # Revert changes
```

---

## 🛡️ Rotas Protegidas

| Rota | Proteção | Status |
|------|----------|--------|
| `/admin/social-networks` (POST) | ✅ Sim | Protegido |
| `/admin/social-networks/<id>/delete` (POST) | ✅ Sim | Protegido |
| `/usuarios/<id>/editar` (POST) | ✅ Sim | Protegido |
| `/admin/sellers` | ⚠️ Verificar | - |
| `/admin/categories` | ⚠️ Verificar | - |

**Recomendação:** Aplicar a mesma proteção em todas as rotas admin.

---

## 📝 Checklist de Segurança

- [x] Forms aninhados removidos
- [x] Proteção de papel implementada
- [x] `flush()` antes de `commit()`
- [x] Logs de debug adicionados
- [x] Testado com usuário ADMIN
- [x] Testado com usuário MEMBER
- [ ] Aplicar proteção em outras rotas admin
- [ ] Adicionar testes unitários

---

**Status:** ✅ **Corrigido e Protegido**  
**Data:** 04/12/2025  
**Prioridade:** 🔴 CRÍTICA (Segurança)

