# 📸 Exibição de Imagens de Produtos

## 📋 Visão Geral

Sistema completo de exibição de imagens de produtos nas páginas de listagem e compartilhamento de ofertas.

---

## ✅ Onde as Imagens Aparecem

### 1. **Listagem de Ofertas** (`/ofertas`)

As imagens dos produtos aparecem como **destaque no topo de cada card** da grade de ofertas.

**Características:**
- Imagem em container de 200px de altura
- Object-fit: cover (preenche o container)
- Hover effect: zoom suave (scale 1.05)
- Bordas arredondadas (8px)
- Lazy loading para performance

**Placeholder (sem imagem):**
- Ícone de imagem centralizado
- Borda tracejada
- Cor de fundo do tema
- Altura consistente (200px)

---

### 2. **Página de Compartilhamento** (`/ofertas/{id}/compartilhar`)

A imagem aparece no **card de informações da oferta**, ao lado direito dos dados do produto.

**Características:**
- Container de 250px de altura máxima
- Object-fit: contain (mantém proporção)
- Padding interno (0.5rem)
- Sombra suave
- Bordas arredondadas (12px)

**Placeholder (sem imagem):**
- Ícone grande centralizado
- Borda tracejada
- Cor de fundo do tema
- Altura de 250px

---

## 🎨 Layout Visual

### Listagem de Ofertas

```
┌─────────────────────────────────┐
│ ┌───────────────────────────┐   │
│ │                           │   │
│ │    IMAGEM DO PRODUTO      │   │  ← 200px altura
│ │       (object-fit)        │   │
│ │                           │   │
│ └───────────────────────────┘   │
│                                 │
│ 📦 Nome do Produto              │
│                                 │
│ 💰 Preço: R$ 100,00             │
│ 🏪 Vendedor: Loja X             │
│                                 │
│ Descrição do produto...         │
│                                 │
│ [Compartilhar] [Editar]         │
└─────────────────────────────────┘
```

### Página de Compartilhamento

```
┌──────────────────────────────────────────────────┐
│  Informações da Oferta                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  Nome: iPhone 15        ┌────────────────┐      │
│  Preço: R$ 5.000       │                │      │
│  Categoria: Eletrônicos│     IMAGEM     │      │
│  Fabricante: Apple      │   DO PRODUTO   │      │
│  Vendedor: Loja X       │    (250px)     │      │
│                         │                │      │
│                         └────────────────┘      │
└──────────────────────────────────────────────────┘
```

---

## 💻 Implementação Técnica

### HTML - Listagem (`offers_list.html`)

```html
{% for offer in offers %}
<article class="panel card">
  <!-- Product Image -->
  {% if offer.product and offer.product.image_url %}
  <div class="product-image-container mb-3">
    <img src="{{ offer.product.image_url }}" 
         alt="{{ offer.product.name }}" 
         class="product-image img-fluid rounded"
         loading="lazy">
  </div>
  {% else %}
  <div class="product-image-placeholder mb-3">
    <i class="bi bi-image"></i>
  </div>
  {% endif %}
  
  <!-- Resto do card -->
  ...
</article>
{% endfor %}
```

### HTML - Compartilhamento (`offer_share.html`)

```html
<div class="col-md-4 text-center">
  {% if offer.product and offer.product.image_url %}
  <div class="product-image-container-share">
    <img src="{{ offer.product.image_url }}" 
         alt="{{ offer.product.name }}" 
         class="img-fluid rounded product-image-share"
         loading="lazy">
  </div>
  {% else %}
  <div class="product-image-placeholder-share rounded">
    <i class="bi bi-image fs-1"></i>
  </div>
  {% endif %}
</div>
```

---

## 🎨 CSS

### Listagem de Ofertas

```css
/* Container da imagem */
.product-image-container {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Imagem do produto */
.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* Hover effect */
.product-image:hover {
  transform: scale(1.05);
}

/* Placeholder (sem imagem) */
.product-image-placeholder {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 3rem;
  border: 2px dashed var(--border-color);
}
```

### Página de Compartilhamento

```css
/* Container da imagem */
.product-image-container-share {
  width: 100%;
  max-height: 250px;
  overflow: hidden;
  border-radius: 12px;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Imagem do produto */
.product-image-share {
  width: 100%;
  height: 100%;
  max-height: 250px;
  object-fit: contain;  /* Mantém proporção */
  padding: 0.5rem;
}

/* Placeholder (sem imagem) */
.product-image-placeholder-share {
  width: 100%;
  height: 250px;
  background: var(--bg-secondary);
  border: 2px dashed var(--border-color);
  color: var(--text-muted);
}

/* Dark theme adjustments */
body[data-theme="dark"] .product-image-placeholder-share {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}
```

---

## 🎯 Diferenças Entre as Páginas

| Aspecto | Listagem | Compartilhamento |
|---------|----------|------------------|
| **Altura** | 200px | 250px |
| **Object-fit** | `cover` (preenche) | `contain` (mantém proporção) |
| **Hover** | Zoom (1.05) | Sem efeito |
| **Padding** | Nenhum | 0.5rem |
| **Sombra** | Nenhuma | Suave (0 2px 8px) |
| **Bordas** | 8px | 12px |
| **Posição** | Topo do card | Lado direito |

---

## 🔍 Recursos de Performance

### Lazy Loading

```html
<img src="{{ offer.product.image_url }}" 
     loading="lazy">
```

**Benefícios:**
- Carrega imagens apenas quando visíveis
- Economiza banda inicial
- Melhora tempo de carregamento da página
- Especialmente útil com muitas ofertas

---

## 🌓 Tema Escuro

### Ajustes Específicos

```css
/* Placeholder no tema escuro */
body[data-theme="dark"] .product-image-placeholder-share {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

body[data-theme="dark"] .product-image-placeholder-share i {
  color: #6b7280 !important;
}
```

**Características:**
- Fundo semi-transparente
- Borda sutil
- Ícone em cinza médio
- Integração perfeita com o tema

---

## 📊 Fluxo de Dados

```
Upload da Imagem
      ↓
app/utils/upload.py
      ↓
save_image() → /static/uploads/products/a3f8d9e2...jpg
      ↓
Banco de Dados
product.image_url = "/static/uploads/products/a3f8d9e2...jpg"
      ↓
Template Jinja2
{% if offer.product.image_url %}
      ↓
HTML renderizado
<img src="/static/uploads/products/a3f8d9e2...jpg">
      ↓
Navegador carrega imagem
```

---

## 🎨 Exemplos Visuais

### Com Imagem (Listagem)

```
┌───────────────────────┐
│                       │
│   [FOTO DO IPHONE]    │  ← Imagem cover
│                       │
└───────────────────────┘
📦 iPhone 15 Pro Max
💰 R$ 5.000,00 (-15%)
🏪 Loja Tech
```

### Sem Imagem (Placeholder)

```
┌───────────────────────┐
│ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ │
│ ┈                 ┈ │
│ ┈     🖼️         ┈ │  ← Ícone de imagem
│ ┈                 ┈ │
│ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ │
└───────────────────────┘
📦 Produto Sem Foto
💰 R$ 100,00
```

---

## ✅ Checklist de Funcionalidades

### Listagem de Ofertas
- [x] Imagem aparece no topo do card
- [x] Container de 200px de altura
- [x] Object-fit: cover
- [x] Hover effect com zoom
- [x] Placeholder para produtos sem imagem
- [x] Lazy loading implementado
- [x] Responsivo (mobile-friendly)
- [x] Tema escuro suportado

### Página de Compartilhamento
- [x] Imagem ao lado das informações
- [x] Container de 250px de altura
- [x] Object-fit: contain (mantém proporção)
- [x] Sombra suave
- [x] Placeholder estilizado
- [x] Lazy loading implementado
- [x] Tema escuro suportado

---

## 🚀 Como Testar

### 1. Upload de Imagem

```bash
# Acesse
http://localhost:5000/ofertas/nova

# Faça upload de uma imagem
# Salve a oferta
```

### 2. Verificar na Listagem

```bash
# Acesse
http://localhost:5000/ofertas

# A imagem deve aparecer no topo do card
# Hover deve fazer zoom suave
```

### 3. Verificar no Compartilhamento

```bash
# Clique em "Compartilhar" em uma oferta
# Ou acesse diretamente
http://localhost:5000/ofertas/1/compartilhar

# A imagem deve aparecer ao lado direito
```

### 4. Testar Placeholder

```bash
# Crie uma oferta sem imagem
# Verifique que o placeholder aparece
# Ícone de imagem deve ser visível
```

---

## 📁 Arquivos Modificados

```
app/templates/
├── offers_list.html        ✅ Container + CSS para listagem
└── offer_share.html        ✅ Container + CSS para compartilhamento
```

---

## 🎯 Responsividade

### Mobile (< 768px)

```css
/* Imagens se ajustam automaticamente */
.product-image-container,
.product-image-container-share {
  width: 100%;  /* Largura total em mobile */
}
```

### Tablet (768px - 1024px)

```css
/* Grid de 2 colunas em tablets */
.grid.three {
  grid-template-columns: repeat(2, 1fr);
}
```

### Desktop (> 1024px)

```css
/* Grid de 3 colunas em desktop */
.grid.three {
  grid-template-columns: repeat(3, 1fr);
}
```

---

## 💡 Boas Práticas Implementadas

### 1. **Lazy Loading**
```html
loading="lazy"
```
Carrega imagens apenas quando necessário.

### 2. **Alt Text**
```html
alt="{{ offer.product.name }}"
```
Acessibilidade e SEO.

### 3. **Responsive Images**
```html
class="img-fluid"
```
Bootstrap class para imagens responsivas.

### 4. **Object-fit**
- `cover` na listagem: preenche o container
- `contain` no compartilhamento: mantém proporção

### 5. **Placeholder Consistente**
Mesmo estilo quando não há imagem.

### 6. **Tema Escuro**
Cores ajustadas para ambos os temas.

---

## 🎉 Resultado Final

### ✅ Listagem de Ofertas
- Imagens aparecem no topo de cada card
- Visual atraente e profissional
- Hover effect interativo
- Placeholder elegante

### ✅ Página de Compartilhamento
- Imagem destaca o produto
- Boa visualização ao lado das informações
- Mantém proporção da imagem
- Integração perfeita com o layout

---

## 🔗 Documentação Relacionada

- `SECURE_IMAGE_UPLOAD.md` - Sistema de upload seguro
- `UPLOAD_IMPLEMENTATION_SUMMARY.md` - Resumo da implementação
- `README.md` - Documentação geral do projeto

---

**Status:** ✅ **COMPLETO E TESTADO**

**Última atualização:** 04/12/2025

