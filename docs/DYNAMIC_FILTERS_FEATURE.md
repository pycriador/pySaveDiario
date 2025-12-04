# 🔍 Feature: Filtros Dinâmicos de Ofertas

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.0.0

---

## ✨ O Que Foi Implementado

### 1. **Sistema de Filtros Completo**
- ✅ **Busca geral:** Nome do produto, slug ou vendedor
- ✅ **Fabricante:** Dropdown com fabricantes cadastrados
- ✅ **Categoria:** Dropdown com categorias cadastradas
- ✅ **Vendedor:** Dropdown com vendedores cadastrados
- ✅ **Faixa de preço:** Preço mínimo e máximo
- ✅ **Ofertas ativas:** Checkbox para filtrar apenas ofertas não expiradas (marcado por padrão)

### 2. **Filtragem Dinâmica (Enquanto Digita)**
- ✅ Campos de texto atualizam com delay de 500ms
- ✅ Dropdowns atualizam imediatamente
- ✅ Checkbox de ofertas ativas atualiza imediatamente
- ✅ Contador de resultados em tempo real

### 3. **URL com Parâmetros**
- ✅ Todos os filtros são adicionados à URL
- ✅ URLs podem ser compartilhadas
- ✅ Histórico do navegador preservado
- ✅ Parâmetros limpos (sem valores vazios)

---

## 📋 Parâmetros da URL

### Parâmetros Disponíveis

| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `search` | string | Busca por nome, slug ou vendedor | `?search=ps5` |
| `manufacturer` | int | ID do fabricante | `?manufacturer=1` |
| `category` | int | ID da categoria | `?category=2` |
| `seller` | int | ID do vendedor | `?seller=3` |
| `min_price` | float | Preço mínimo | `?min_price=100.00` |
| `max_price` | float | Preço máximo | `?max_price=500.00` |
| `active_only` | boolean | Apenas ofertas ativas | `?active_only=true` |

### Exemplos de URLs

**Busca simples:**
```
/ofertas?search=playstation
```

**Filtro por categoria e preço:**
```
/ofertas?category=1&min_price=1000&max_price=3000
```

**Filtro completo:**
```
/ofertas?search=console&manufacturer=2&category=1&seller=3&min_price=2000&max_price=4000&active_only=true
```

**Apenas ofertas expiradas:**
```
/ofertas?active_only=false
```

---

## 🎨 Interface do Usuário

### Layout do Painel de Filtros

```
┌─────────────────────────────────────────────────────────┐
│ 🔽 Filtros                              [Limpar]        │
├─────────────────────────────────────────────────────────┤
│ 🔍 Busca geral                  ✓ Apenas ofertas ativas │
│ ┌─────────────────────────┐    ┌────────────────────┐  │
│ │ Nome, slug ou vendedor  │    │ [✓] Não expiradas  │  │
│ └─────────────────────────┘    └────────────────────┘  │
│                                                          │
│ ⚙️ Fabricante    🏷️ Categoria    🏪 Vendedor            │
│ ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│ │ Todos   │    │ Todas   │    │ Todos   │             │
│ └─────────┘    └─────────┘    └─────────┘             │
│                                                          │
│ 💰 Faixa de preço                                       │
│ ┌─────────┐ até ┌─────────┐                            │
│ │ Min     │     │ Max     │                            │
│ └─────────┘     └─────────┘                            │
├─────────────────────────────────────────────────────────┤
│ ✓ 15 oferta(s) encontrada(s)                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Lógica de Filtros

### Backend (Python/Flask)

**Busca geral:**
```python
if search:
    search_filter = db.or_(
        Product.name.ilike(f"%{search}%"),
        Product.slug.ilike(f"%{search}%"),
        Offer.vendor_name.ilike(f"%{search}%")
    )
    query = query.filter(search_filter)
```

**Filtro por fabricante:**
```python
if manufacturer_id:
    query = query.filter(Offer.manufacturer_id == manufacturer_id)
```

**Filtro por categoria:**
```python
if category_id:
    query = query.filter(Offer.category_id == category_id)
```

**Filtro por vendedor:**
```python
if seller_id:
    query = query.filter(Offer.seller_id == seller_id)
```

**Faixa de preço:**
```python
if min_price is not None:
    query = query.filter(Offer.price >= min_price)
if max_price is not None:
    query = query.filter(Offer.price <= max_price)
```

**Ofertas ativas (não expiradas):**
```python
if active_only:
    query = query.filter(
        db.or_(
            Offer.expires_at.is_(None),  # Sem data de expiração
            Offer.expires_at > datetime.utcnow()  # Não expirou ainda
        )
    )
```

---

## ⚡ JavaScript Dinâmico

### Delay para Campos de Texto
```javascript
let filterTimeout;

function updateFilters() {
  clearTimeout(filterTimeout);
  filterTimeout = setTimeout(() => {
    applyFilters();
  }, 500); // 500ms delay após parar de digitar
}
```

### Atualização Imediata para Dropdowns
```javascript
manufacturerSelect.addEventListener('change', applyFilters);
categorySelect.addEventListener('change', applyFilters);
sellerSelect.addEventListener('change', applyFilters);
```

### Construção da URL
```javascript
function applyFilters() {
  const form = document.getElementById('filterForm');
  const formData = new FormData(form);
  const params = new URLSearchParams();
  
  // Build URL parameters
  for (const [key, value] of formData.entries()) {
    if (value && value.trim() !== '') {
      params.append(key, value);
    }
  }
  
  // Handle checkbox separately
  const activeOnly = document.getElementById('active_only');
  if (activeOnly.checked) {
    params.set('active_only', 'true');
  } else {
    params.set('active_only', 'false');
  }
  
  // Update URL and reload
  const newUrl = `${window.location.pathname}?${params.toString()}`;
  window.location.href = newUrl;
}
```

---

## 🎯 Casos de Uso

### 1. Buscar Console Específico
```
Usuário digita: "ps5"
URL: /ofertas?search=ps5&active_only=true
Resultado: Todas as ofertas ativas com "ps5" no nome, slug ou vendedor
```

### 2. Produtos Nintendo na Faixa de R$200-500
```
Usuário seleciona:
- Fabricante: Nintendo
- Preço: 200 ~ 500

URL: /ofertas?manufacturer=1&min_price=200&max_price=500&active_only=true
Resultado: Produtos Nintendo entre R$200 e R$500
```

### 3. Ofertas da Amazon em Eletrônicos
```
Usuário seleciona:
- Categoria: Eletrônicos
- Vendedor: Amazon

URL: /ofertas?category=1&seller=2&active_only=true
Resultado: Eletrônicos vendidos pela Amazon
```

### 4. Ver Todas as Ofertas (Incluindo Expiradas)
```
Usuário desmarca: "Apenas ofertas ativas"

URL: /ofertas?active_only=false
Resultado: Todas as ofertas (ativas + expiradas)
```

---

## 🔄 Fluxo Completo

### Passo a Passo

1. **Usuário acessa `/ofertas`**
   - Por padrão: `active_only=true`
   - Mostra todas as ofertas ativas

2. **Usuário digita "playstation" no campo de busca**
   - JavaScript espera 500ms
   - Constrói URL: `/ofertas?search=playstation&active_only=true`
   - Página recarrega com resultados filtrados

3. **Usuário seleciona "Sony" no dropdown de Fabricante**
   - JavaScript executa imediatamente
   - URL: `/ofertas?search=playstation&manufacturer=2&active_only=true`
   - Resultados atualizados

4. **Usuário clica em "Limpar"**
   - Limpa todos os campos
   - Volta para: `/ofertas?active_only=true`
   - Mostra todas as ofertas novamente

---

## 💡 Funcionalidades Especiais

### 1. **Preservação de Estado**
- Valores dos filtros são mantidos ao recarregar
- URL pode ser copiada e compartilhada
- Filtros aparecem pré-preenchidos

### 2. **Contador de Resultados**
```html
✓ 15 oferta(s) encontrada(s)
```
- Atualiza automaticamente
- Feedback visual imediato

### 3. **Botão "Limpar"**
- Remove todos os filtros
- Mantém `active_only=true`
- Volta ao estado inicial

### 4. **Performance**
- Delay de 500ms para texto (evita requisições excessivas)
- Atualização imediata para dropdowns
- Parâmetros vazios não são incluídos na URL

---

## 🎨 CSS e Estilo

### Painel de Filtros
```css
.panel {
  background: var(--panel-bg);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}
```

### Switch do Checkbox
```html
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" ... >
  <label class="form-check-label">
    <i class="bi bi-check-circle"></i> Apenas ofertas ativas
  </label>
</div>
```

### Input Group (Faixa de Preço)
```html
<div class="input-group">
  <input ... placeholder="Min" />
  <span class="input-group-text">até</span>
  <input ... placeholder="Max" />
</div>
```

---

## 📊 Queries SQL Geradas

### Exemplo: Busca com Múltiplos Filtros

**Filtros aplicados:**
- search: "playstation"
- manufacturer: 2 (Sony)
- min_price: 2000
- active_only: true

**Query SQL:**
```sql
SELECT offers.*
FROM offers
JOIN products ON products.id = offers.product_id
WHERE (
    products.name ILIKE '%playstation%' OR
    products.slug ILIKE '%playstation%' OR
    offers.vendor_name ILIKE '%playstation%'
)
AND offers.manufacturer_id = 2
AND offers.price >= 2000.00
AND (
    offers.expires_at IS NULL OR
    offers.expires_at > NOW()
)
ORDER BY offers.created_at DESC;
```

---

## 🔐 Validação e Segurança

### Tipo de Dados
- ✅ `manufacturer`, `category`, `seller`: convertidos para `int`
- ✅ `min_price`, `max_price`: convertidos para `float`
- ✅ `search`: string com `.strip()`
- ✅ `active_only`: convertido para `boolean`

### Proteção SQL Injection
- ✅ SQLAlchemy ORM previne SQL injection
- ✅ Uso de `.ilike()` com parâmetros seguros
- ✅ Validação de tipos no backend

### Valores Padrão
```python
search = request.args.get("search", "").strip()
active_only = request.args.get("active_only", "true").lower() == "true"
```

---

## 🚀 Melhorias Futuras

### Curto Prazo
1. ✨ Adicionar ordenação (preço, data, nome)
2. ✨ Salvar filtros favoritos
3. ✨ Exportar resultados (CSV, JSON)

### Médio Prazo
1. 📊 Gráfico de distribuição de preços
2. 🔔 Alertas de preço (email quando filtro encontrar oferta)
3. 📈 Histórico de mudanças de preço

### Longo Prazo
1. 🤖 Sugestões de filtros baseadas em IA
2. 📱 Filtros salvos sincronizados entre dispositivos
3. 🌐 API para acesso aos filtros

---

## 📱 Responsividade

### Desktop
```
[Busca ────────────] [✓ Ativas]
[Fabricante] [Categoria] [Vendedor]
[Min] até [Max]
```

### Mobile
```
[Busca ─────────────]
[✓ Ativas ──────────]
[Fabricante ────────]
[Categoria ─────────]
[Vendedor ──────────]
[Min] até [Max]
```

---

## 🎓 Experiência do Usuário

### Antes ❌
- Filtros básicos (apenas vendor e product)
- Sem filtragem dinâmica
- Parâmetros confusos na URL
- Sem feedback de resultados

### Agora ✅
- Filtros completos e abrangentes
- Filtragem dinâmica enquanto digita
- URL limpa e compartilhável
- Contador de resultados
- Botão de limpar filtros
- Ofertas ativas por padrão
- Interface intuitiva

---

## 🏆 Resultado Final

### Funcionalidades
- ✅ 7 tipos de filtros diferentes
- ✅ Filtragem dinâmica com delay inteligente
- ✅ URL com parâmetros limpos
- ✅ Contador de resultados
- ✅ Botão limpar
- ✅ Estado preservado
- ✅ Compartilhável

### Performance
- ⚡ Delay de 500ms para texto (otimizado)
- ⚡ Atualização imediata para dropdowns
- ⚡ Queries SQL otimizadas com joins
- ⚡ Apenas valores preenchidos na URL

### UX
- 🎨 Interface limpa e intuitiva
- 🎨 Feedback visual (contador)
- 🎨 Ícones descritivos
- 🎨 Textos de ajuda
- 🎨 Tema claro e escuro

---

## ✅ Checklist de Implementação

- [x] Backend: rota `/ofertas` com parâmetros
- [x] Backend: lógica de filtros no SQLAlchemy
- [x] Backend: passar dados para template
- [x] Frontend: formulário de filtros
- [x] Frontend: JavaScript de filtragem dinâmica
- [x] Frontend: função `clearFilters()`
- [x] Frontend: contador de resultados
- [x] Frontend: checkbox "ofertas ativas" marcado por padrão
- [x] URL: parâmetros limpos
- [x] UX: delay para texto, imediato para dropdowns
- [x] Documentação completa

---

## 🎊 Status

**✅ IMPLEMENTADO COM SUCESSO!**

Sistema completo de filtros dinâmicos funcionando perfeitamente:
- Filtragem enquanto digita ✓
- Múltiplos critérios ✓
- URL com parâmetros ✓
- Performance otimizada ✓
- Interface intuitiva ✓

---

**Desenvolvido com ❤️ para melhor experiência de busca**

