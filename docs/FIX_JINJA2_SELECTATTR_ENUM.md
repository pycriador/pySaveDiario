# 🔧 Correção: Filtro selectattr do Jinja2 com Enum

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.7.2  
**Status:** ✅ CORRIGIDO

---

## 🐛 Problema

Após padronizar os scopes no banco de dados para minúsculas, **NENHUMA variável aparecia** nas páginas de criar/editar templates.

**Mensagem mostrada:**
```
Nenhuma variável cadastrada no momento
```

**Mas:**
- ✅ 19 namespaces existiam no banco de dados
- ✅ Query SQL retornava resultados
- ✅ A rota passava `namespaces` para o template
- ❌ O filtro Jinja2 não estava funcionando

---

## 🔍 Causa Raiz

**Problema com `selectattr` do Jinja2 e Enums do SQLAlchemy:**

### Código Original (NÃO FUNCIONAVA)
```jinja2
{% set offer_ns = namespaces|selectattr('scope.value', 'equalto', 'offer')|list %}
{% set coupon_ns = namespaces|selectattr('scope.value', 'equalto', 'coupon')|list %}
{% set global_ns = namespaces|selectattr('scope.value', 'equalto', 'global')|list %}
```

**Por que não funcionava:**
- `selectattr('scope.value', ...)` tenta acessar um atributo chamado `scope.value`
- Mas o correto seria acessar `scope` e então `.value`
- O filtro `selectattr` do Jinja2 não suporta acesso aninhado com ponto

**Analogia:**
```python
# Python consegue:
namespace.scope.value

# selectattr não consegue:
selectattr('scope.value', 'equalto', 'offer')  # ❌

# selectattr só consegue um nível:
selectattr('scope', 'equalto', NamespaceScope.OFFER)  # Funciona, mas...
# ...não podemos usar NamespaceScope.OFFER no template Jinja2
```

---

## ✅ Solução Aplicada

Substituí o filtro `selectattr` por um **loop explícito**:

### Código Novo (FUNCIONA)
```jinja2
{% set offer_ns = [] %}
{% set coupon_ns = [] %}
{% set global_ns = [] %}
{% for ns in namespaces %}
  {% if ns.scope.value == 'offer' %}
    {% set _ = offer_ns.append(ns) %}
  {% elif ns.scope.value == 'coupon' %}
    {% set _ = coupon_ns.append(ns) %}
  {% elif ns.scope.value == 'global' %}
    {% set _ = global_ns.append(ns) %}
  {% endif %}
{% endfor %}
```

**Por que funciona:**
- ✅ Acesso direto a `ns.scope.value` dentro do loop
- ✅ Comparação simples com string `'offer'`, `'coupon'`, `'global'`
- ✅ Append funciona com `{% set _ = lista.append(item) %}`

---

## 📊 Antes e Depois

### Antes (selectattr - não funcionava)

```jinja2
{% set offer_ns = namespaces|selectattr('scope.value', 'equalto', 'offer')|list %}
```

**Resultado:** `offer_ns = []` (lista vazia)

**Por quê:** `selectattr` não consegue acessar `scope.value` (dois níveis)

### Depois (loop explícito - funciona)

```jinja2
{% set offer_ns = [] %}
{% for ns in namespaces %}
  {% if ns.scope.value == 'offer' %}
    {% set _ = offer_ns.append(ns) %}
  {% endif %}
{% endfor %}
```

**Resultado:** `offer_ns = [Namespace(...), Namespace(...), ...]` (11 itens)

**Por quê:** Loop permite acesso completo a `ns.scope.value`

---

## 🔬 Detalhes Técnicos

### Model (SQLAlchemy)
```python
class NamespaceScope(str, Enum):
    OFFER = "offer"
    COUPON = "coupon"
    GLOBAL = "global"

class Namespace(db.Model):
    scope = db.Column(db.Enum(NamespaceScope), default=NamespaceScope.GLOBAL)
```

### Banco de Dados
```sql
SELECT scope FROM namespaces LIMIT 1;
-- Retorna: 'offer' (string)
```

### SQLAlchemy (carregamento)
```python
namespace = Namespace.query.first()
print(type(namespace.scope))  # <enum 'NamespaceScope'>
print(namespace.scope)         # NamespaceScope.OFFER
print(namespace.scope.value)   # 'offer' (string)
```

### Jinja2 (template)
```jinja2
{{ ns.scope }}        {# NamespaceScope.OFFER #}
{{ ns.scope.value }}  {# 'offer' #}
```

---

## 📂 Arquivos Modificados

```
app/templates/template_create.html
  ✅ Substituído selectattr por loop explícito

app/templates/template_edit.html
  ✅ Substituído selectattr por loop explícito
```

---

## 🧪 Teste de Verificação

### Antes da Correção
```
1. Acesse /templates/3/editar
2. Role até "Variáveis Disponíveis"
3. Veja: "Nenhuma variável cadastrada no momento" ❌
```

### Depois da Correção
```
1. Acesse /templates/3/editar
2. Role até "Variáveis Disponíveis"
3. Veja:
   🏷️ VARIÁVEIS DE OFERTAS (11 itens) ✅
   🎟️ VARIÁVEIS DE CUPONS (5 itens) ✅
   🌍 VARIÁVEIS GLOBAIS (3 itens) ✅
```

---

## 💡 Alternativas Consideradas

### Alternativa 1: Custom Filter (mais complexo)
```python
# app/__init__.py
@app.template_filter('by_scope')
def filter_by_scope(namespaces, scope_value):
    return [ns for ns in namespaces if ns.scope.value == scope_value]
```

```jinja2
{% set offer_ns = namespaces|by_scope('offer') %}
```

**Rejeita:** Mais código, necessita modificar `__init__.py`

### Alternativa 2: Passar listas separadas da rota (menos flexível)
```python
# app/routes/web.py
offer_ns = Namespace.query.filter_by(scope=NamespaceScope.OFFER).all()
coupon_ns = Namespace.query.filter_by(scope=NamespaceScope.COUPON).all()
global_ns = Namespace.query.filter_by(scope=NamespaceScope.GLOBAL).all()

return render_template('...', offer_ns=offer_ns, coupon_ns=coupon_ns, global_ns=global_ns)
```

**Rejeita:** 3 queries ao invés de 1, mais código no backend

### Alternativa 3: Loop explícito (ESCOLHIDA) ✅
```jinja2
{% for ns in namespaces %}
  {% if ns.scope.value == 'offer' %}
    {% set _ = offer_ns.append(ns) %}
  {% endif %}
{% endfor %}
```

**Vantagens:**
- ✅ Simples
- ✅ Sem mudanças no backend
- ✅ Sem dependências externas
- ✅ Fácil de entender

---

## 📚 Lições Aprendidas

### 1. Limitação do `selectattr`
O filtro `selectattr` do Jinja2 **não suporta acesso aninhado**:

```jinja2
{# ❌ NÃO FUNCIONA #}
{{ items|selectattr('parent.child', 'equalto', 'value') }}

{# ✅ FUNCIONA #}
{{ items|selectattr('parent', 'equalto', parent_object) }}
```

### 2. Enums do SQLAlchemy no Jinja2
Para acessar o valor de um Enum:

```jinja2
{# Objeto Enum #}
{{ namespace.scope }}  {# NamespaceScope.OFFER #}

{# Valor string do Enum #}
{{ namespace.scope.value }}  {# 'offer' #}
```

### 3. Append em Listas no Jinja2
Para adicionar a uma lista:

```jinja2
{# ✅ CORRETO - usa _ para descartar o None retornado #}
{% set _ = my_list.append(item) %}

{# ❌ ERRADO - append retorna None #}
{% set my_list = my_list.append(item) %}
```

---

## 🔍 Debug Process

### Como identifiquei o problema:

1. ✅ Verifiquei banco de dados: 19 namespaces existem
2. ✅ Testei query SQL: retorna resultados
3. ✅ Verifiquei rota Python: passa `namespaces` corretamente
4. ❌ Template mostrava "Nenhuma variável cadastrada"
5. 🔎 Conclusão: Problema no filtro Jinja2

### Como testei a correção:

```jinja2
{# Debug: Mostrar quantos namespaces existem #}
<p>Total: {{ namespaces|length }}</p>  {# 19 #}

{# Debug: Mostrar cada scope.value #}
{% for ns in namespaces %}
  <p>{{ ns.name }}: {{ ns.scope.value }}</p>
{% endfor %}

{# Debug: Testar selectattr #}
{% set test = namespaces|selectattr('scope.value', 'equalto', 'offer')|list %}
<p>selectattr result: {{ test|length }}</p>  {# 0 ← PROBLEMA! #}

{# Debug: Testar loop manual #}
{% set test2 = [] %}
{% for ns in namespaces %}
  {% if ns.scope.value == 'offer' %}
    {% set _ = test2.append(ns) %}
  {% endif %}
{% endfor %}
<p>manual loop result: {{ test2|length }}</p>  {# 11 ← FUNCIONA! #}
```

---

## ✅ Status Final

**✅ PROBLEMA RESOLVIDO!**

Agora todas as variáveis aparecem corretamente:
- ✅ 11 variáveis de Ofertas
- ✅ 5 variáveis de Cupons
- ✅ 3 variáveis Globais
- ✅ Total: 19 namespaces

---

## 📋 Checklist de Correção

- [x] Identificar que selectattr não funciona com acesso aninhado
- [x] Substituir por loop explícito em template_create.html
- [x] Substituir por loop explícito em template_edit.html
- [x] Testar página de criação de template
- [x] Testar página de edição de template
- [x] Verificar que 3 seções aparecem
- [x] Verificar contagem de variáveis
- [x] Documentar problema e solução

---

**Filtro Jinja2 corrigido - todas as variáveis agora aparecem! 🎉**

