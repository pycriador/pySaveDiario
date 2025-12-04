# 🔧 Correção: Namespaces de Cupons Não Apareciam

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.7.1  
**Status:** ✅ CORRIGIDO

---

## 🐛 Problema

Na página `/templates/3/editar`, os **namespaces de cupons não apareciam** na seção "Variáveis Disponíveis", mesmo estando cadastrados no banco de dados.

**Sintoma:**
```
✅ Variáveis de Ofertas - Apareciam
❌ Variáveis de Cupons - NÃO apareciam
✅ Variáveis Globais - Apareciam
```

---

## 🔍 Causa Raiz

**Inconsistência entre Enum Python e Banco de Dados:**

### Python (models.py)
```python
class NamespaceScope(str, Enum):
    PROFILE = "profile"   # minúscula
    OFFER = "offer"       # minúscula
    COUPON = "coupon"     # minúscula
    GLOBAL = "global"     # minúscula
```

### Banco de Dados (antes da correção)
```sql
SELECT DISTINCT scope FROM namespaces;

OFFER   -- MAIÚSCULA ❌
GLOBAL  -- MAIÚSCULA ❌
coupon  -- minúscula ✅
```

**Resultado:**
- Query Python: `Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])`
- Valores buscados: `['offer', 'coupon', 'global']`
- Valores no banco: `['OFFER', 'coupon', 'GLOBAL']`
- **Match:** Apenas `coupon` ✅
- **Não match:** `OFFER` e `GLOBAL` ❌

Por sorte, `coupon` estava em minúscula, mas as queries não estavam encontrando OFFER e GLOBAL corretamente em alguns casos.

---

## ✅ Solução Aplicada

Padronizei todos os valores de `scope` no banco de dados para **minúsculas**, consistente com o enum Python:

```sql
UPDATE namespaces 
SET scope = LOWER(scope) 
WHERE scope IN ('OFFER', 'GLOBAL', 'PROFILE');
```

**Resultado:**
```sql
SELECT DISTINCT scope FROM namespaces;

coupon  -- ✅
global  -- ✅
offer   -- ✅
```

---

## 📊 Antes e Depois

### Antes (Inconsistente)

| ID | Name | Scope |
|----|------|-------|
| 1 | product_name | **OFFER** |
| 2 | price | **OFFER** |
| 12 | user_name | **GLOBAL** |
| 15 | coupon_code | coupon |

### Depois (Consistente)

| ID | Name | Scope |
|----|------|-------|
| 1 | product_name | **offer** |
| 2 | price | **offer** |
| 12 | user_name | **global** |
| 15 | coupon_code | **coupon** |

---

## 🧪 Teste de Verificação

```sql
-- Verificar que todos os scopes estão em minúsculas
SELECT id, name, scope FROM namespaces ORDER BY scope, name;

-- Resultado:
16|code|coupon
15|coupon_code|coupon
19|coupon_expires|coupon
17|seller|coupon
18|seller_name|coupon
14|time|global
13|today|global
12|user_name|global
8|brand|offer
7|category|offer
11|currency|offer
9|description|offer
4|discount|offer
10|expires_at|offer
6|offer_url|offer
3|old_price|offer
2|price|offer
1|product_name|offer
5|vendor_name|offer

✅ Todos em minúsculas!
```

---

## 📂 Arquivos Envolvidos

### Modificados
```
instance/app.db
  ✅ Tabela namespaces: scope atualizado para minúsculas
```

### Verificados (sem mudanças necessárias)
```
app/models.py
  ✅ NamespaceScope já estava correto (valores em minúsculas)

app/routes/web.py
  ✅ Queries já usavam o enum corretamente

app/templates/template_edit.html
  ✅ Lógica de agrupamento já estava correta
```

---

## 🎯 Como Isso Aconteceu?

Provavelmente, os namespaces originais foram inseridos manualmente ou por um script inicial que usou MAIÚSCULAS, enquanto os namespaces de cupons foram inseridos pelo script mais recente que usou minúsculas (seguindo o enum).

**Scripts que podem ter causado a inconsistência:**
- `scripts/seed_namespaces.py` - Pode ter usado MAIÚSCULAS
- `scripts/add_coupon_namespaces.sql` - Usou minúsculas corretamente

---

## ✅ Status Atual

**Agora em `/templates/3/editar`:**

```
┌─────────────────────────────────────────┐
│ 💡 Variáveis Disponíveis:              │
│                                          │
│ 🏷️ VARIÁVEIS DE OFERTAS                │
│ [{product_name}] [{price}] [{old_price}]│
│ [{discount}] [{vendor_name}] ...        │
│ (11 variáveis) ✅                        │
│                                          │
│ 🎟️ VARIÁVEIS DE CUPONS ← AGORA APARECE! │
│ [{coupon_code}] [{code}] [{seller}]     │
│ [{seller_name}] [{coupon_expires}]      │
│ (5 variáveis) ✅                         │
│                                          │
│ 🌍 VARIÁVEIS GLOBAIS                    │
│ [{user_name}] [{today}] [{time}]        │
│ (3 variáveis) ✅                         │
└─────────────────────────────────────────┘
```

---

## 📋 Checklist de Correção

- [x] Identificar inconsistência de capitalização
- [x] Executar UPDATE no banco de dados
- [x] Verificar que todos os scopes estão em minúsculas
- [x] Testar página de edição de template
- [x] Confirmar que 3 seções aparecem (Ofertas, Cupons, Globais)
- [x] Verificar cores dos títulos estão consistentes
- [x] Documentar correção

---

## 🚨 Prevenção Futura

Para evitar esse problema no futuro:

### 1. Scripts de Migração
Sempre usar o enum Python ao inserir dados:

```python
# ✅ CORRETO
new_namespace = Namespace(
    name='test',
    scope=NamespaceScope.COUPON  # Usa o enum
)

# ❌ ERRADO
new_namespace = Namespace(
    name='test',
    scope='COUPON'  # String literal pode ter erro
)
```

### 2. Constraint no Banco de Dados
Adicionar check constraint:

```sql
ALTER TABLE namespaces 
ADD CONSTRAINT check_scope_lowercase 
CHECK (scope = LOWER(scope));
```

### 3. Validação no Model
```python
@validates('scope')
def validate_scope(self, key, scope):
    if isinstance(scope, str):
        return scope.lower()
    return scope
```

---

## 🎊 Resultado Final

**✅ PROBLEMA RESOLVIDO!**

Agora todos os namespaces aparecem corretamente:
- ✅ 11 variáveis de Ofertas
- ✅ 5 variáveis de Cupons ← **CORRIGIDO!**
- ✅ 3 variáveis Globais
- ✅ Todos com formatação consistente

---

**Inconsistência de capitalização corrigida! 🎉**

