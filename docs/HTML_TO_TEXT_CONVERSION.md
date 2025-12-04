# 📱 Conversão HTML para Texto Formatado por Rede Social

## 📋 Visão Geral

Sistema inteligente que converte o HTML gerado pelo editor Quill.js em texto formatado específico para cada rede social, mantendo a formatação (negrito, itálico, listas, etc.) de forma nativa em cada plataforma.

---

## 🎯 Problema Resolvido

### Antes ❌
```
Texto compartilhado no WhatsApp:
<p>Produto <strong>incrível</strong></p>
<ul><li>Alta qualidade</li></ul>
```

### Depois ✅
```
Texto compartilhado no WhatsApp:
Produto *incrível*

• Alta qualidade
```

---

## 🌐 Sintaxe por Rede Social

### WhatsApp

| HTML | WhatsApp | Exemplo |
|------|----------|---------|
| `<strong>texto</strong>` | `*texto*` | *negrito* |
| `<em>texto</em>` | `_texto_` | _itálico_ |
| `<s>texto</s>` | `~texto~` | ~riscado~ |
| `<code>texto</code>` | ` ```texto``` ` | ```código``` |
| `<li>item</li>` | `• item` | • item |
| `<br>` | `\n` | quebra de linha |
| `<p>parágrafo</p>` | `parágrafo\n\n` | parágrafo duplo |
| `<a href="url">texto</a>` | `texto (url)` | texto (url) |

**Exemplo completo:**
```html
<h2>Oferta Especial</h2>
<p>Produto <strong>incrível</strong> com <em>desconto</em>!</p>
<ul>
  <li>Alta qualidade</li>
  <li>Frete grátis</li>
</ul>
```

**Resultado no WhatsApp:**
```
*Oferta Especial*

Produto *incrível* com _desconto_!

• Alta qualidade
• Frete grátis
```

---

### Telegram

| HTML | Telegram | Exemplo |
|------|----------|---------|
| `<strong>texto</strong>` | `**texto**` | **negrito** |
| `<em>texto</em>` | `__texto__` | __itálico__ |
| `<s>texto</s>` | `~~texto~~` | ~~riscado~~ |
| `<code>texto</code>` | `` `texto` `` | `código` |
| `<li>item</li>` | `• item` | • item |
| `<br>` | `\n` | quebra de linha |
| `<p>parágrafo</p>` | `parágrafo\n\n` | parágrafo duplo |
| `<a href="url">texto</a>` | `[texto](url)` | [texto](url) |

**Exemplo completo:**
```html
<p>Produto <strong>fantástico</strong> com <s>preço antigo</s></p>
<p>Novo preço: <strong>R$ 99,90</strong></p>
```

**Resultado no Telegram:**
```
Produto **fantástico** com ~~preço antigo~~

Novo preço: **R$ 99,90**
```

---

### Instagram / Facebook / Twitter

**Formatação:** Não suportam formatação de texto, apenas texto simples com quebras de linha.

| HTML | Resultado |
|------|-----------|
| `<strong>texto</strong>` | `texto` (sem formatação) |
| `<h1>Título</h1>` | `TÍTULO` (maiúsculas) |
| `<li>item</li>` | `• item` |
| `<br>` | `\n` (quebra de linha) |
| `<p>parágrafo</p>` | `parágrafo\n\n` |

**Exemplo completo:**
```html
<h2>Oferta Especial</h2>
<p>Produto <strong>incrível</strong> com desconto!</p>
<ul>
  <li>Alta qualidade</li>
  <li>Frete grátis</li>
</ul>
```

**Resultado no Instagram:**
```
OFERTA ESPECIAL

Produto incrível com desconto!

• Alta qualidade
• Frete grátis
```

---

## 💻 Implementação Técnica

### JavaScript - Função de Conversão

**Arquivo:** `app/templates/offer_share.html`

```javascript
/**
 * Convert HTML to formatted text based on social network
 * @param {string} html - HTML content from Quill editor
 * @param {string} network - Social network name (whatsapp, telegram, instagram, etc.)
 * @returns {string} - Formatted text for the specific network
 */
function htmlToFormattedText(html, network) {
  if (!html) return '';
  
  // Create a temporary div to parse HTML
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;
  
  // Recursive function to process nodes
  function processNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      return node.textContent;
    }
    
    if (node.nodeType === Node.ELEMENT_NODE) {
      const tagName = node.tagName.toLowerCase();
      let content = '';
      
      // Process child nodes
      for (let child of node.childNodes) {
        content += processNode(child);
      }
      
      // Apply formatting based on network and tag
      switch (network.toLowerCase()) {
        case 'whatsapp':
          if (tagName === 'strong' || tagName === 'b') {
            return `*${content}*`;
          } else if (tagName === 'em' || tagName === 'i') {
            return `_${content}_`;
          }
          // ... more rules
          break;
        
        case 'telegram':
          if (tagName === 'strong' || tagName === 'b') {
            return `**${content}**`;
          }
          // ... more rules
          break;
        
        // ... more networks
      }
      
      return content;
    }
    
    return '';
  }
  
  // Process all child nodes
  for (let child of tempDiv.childNodes) {
    text += processNode(child);
  }
  
  // Clean up extra whitespace
  text = text.replace(/\n{3,}/g, '\n\n'); // Max 2 consecutive line breaks
  text = text.trim();
  
  return text;
}
```

---

### Integração com generateText()

```javascript
function generateText() {
  // ... código existente ...
  
  // Convert HTML description to formatted text for the selected network
  const formattedDescription = htmlToFormattedText(
    offerData.product_description || '', 
    selectedChannel
  );
  
  text = text.replace(/{product_description}/gi, formattedDescription);
  text = text.replace(/{description}/gi, formattedDescription);
  text = text.replace(/{descricao}/gi, formattedDescription);
  
  // ... continua ...
}
```

---

## 📝 Namespaces Disponíveis

| Namespace | Descrição | Uso |
|-----------|-----------|-----|
| `{product_description}` | Descrição completa do produto | Template principal |
| `{description}` | Atalho para descrição | Template curto |
| `{descricao}` | Versão em português | Template PT-BR |

**Uso nos templates:**

```
🔥 PROMOÇÃO IMPERDÍVEL!

{product_name}

{product_description}

💰 De {old_price} por apenas {price}

🛒 Compre agora: {offer_url}
```

**Resultado com descrição HTML:**
```html
Descrição no editor:
<p>Produto <strong>premium</strong> com:</p>
<ul>
  <li>Garantia de 2 anos</li>
  <li>Frete grátis</li>
</ul>
```

**Texto final no WhatsApp:**
```
🔥 PROMOÇÃO IMPERDÍVEL!

iPhone 15 Pro Max

Produto *premium* com:

• Garantia de 2 anos
• Frete grátis

💰 De R$ 6.999,00 por apenas R$ 5.499,00

🛒 Compre agora: https://exemplo.com/iphone15
```

---

## 🎨 Tags HTML Suportadas

### Formatação de Texto
- `<strong>` / `<b>` - Negrito
- `<em>` / `<i>` - Itálico
- `<s>` / `<strike>` / `<del>` - Riscado
- `<code>` - Código
- `<u>` - Sublinhado (convertido para texto simples em algumas redes)

### Estrutura
- `<h1>` / `<h2>` / `<h3>` - Cabeçalhos (convertidos para negrito ou maiúsculas)
- `<p>` - Parágrafo (adiciona duas quebras de linha)
- `<br>` - Quebra de linha simples
- `<ul>` / `<ol>` - Listas (não ordenadas/ordenadas)
- `<li>` - Item de lista (prefixo `•`)

### Links
- `<a href="url">texto</a>` - Links (formato varia por rede)

### Cores e Backgrounds
- Removidos automaticamente (não suportados em texto)

---

## 🧪 Exemplos de Conversão

### Exemplo 1: Lista de Características

**HTML:**
```html
<p>Principais características:</p>
<ul>
  <li><strong>Câmera:</strong> 48MP</li>
  <li><strong>Bateria:</strong> 5000mAh</li>
  <li><strong>Tela:</strong> 6.7"</li>
</ul>
```

**WhatsApp:**
```
Principais características:

• *Câmera:* 48MP
• *Bateria:* 5000mAh
• *Tela:* 6.7"
```

**Instagram:**
```
Principais características:

• Câmera: 48MP
• Bateria: 5000mAh
• Tela: 6.7"
```

---

### Exemplo 2: Promoção com Destaque

**HTML:**
```html
<h2>OFERTA RELÂMPAGO</h2>
<p>Produto <em>exclusivo</em> com <strong>50% OFF</strong>!</p>
<p><s>R$ 200,00</s> → <strong>R$ 100,00</strong></p>
```

**WhatsApp:**
```
*OFERTA RELÂMPAGO*

Produto _exclusivo_ com *50% OFF*!

~R$ 200,00~ → *R$ 100,00*
```

**Telegram:**
```
**OFERTA RELÂMPAGO**

Produto __exclusivo__ com **50% OFF**!

~~R$ 200,00~~ → **R$ 100,00**
```

---

### Exemplo 3: Descrição Detalhada

**HTML:**
```html
<h3>iPhone 15 Pro Max</h3>
<p>O smartphone mais <strong>avançado</strong> do mercado!</p>
<p>Características:</p>
<ul>
  <li>Processador A17 Pro</li>
  <li>Câmera de 48MP</li>
  <li>Tela de 6.7" Super Retina</li>
  <li>Bateria de longa duração</li>
</ul>
<p><em>Disponível em 4 cores</em></p>
```

**WhatsApp:**
```
*iPhone 15 Pro Max*

O smartphone mais *avançado* do mercado!

Características:

• Processador A17 Pro
• Câmera de 48MP
• Tela de 6.7" Super Retina
• Bateria de longa duração

_Disponível em 4 cores_
```

**Instagram:**
```
IPHONE 15 PRO MAX

O smartphone mais avançado do mercado!

Características:

• Processador A17 Pro
• Câmera de 48MP
• Tela de 6.7" Super Retina
• Bateria de longa duração

Disponível em 4 cores
```

---

## 🔧 Como Usar

### 1. Criar Oferta com Descrição Formatada

```
1. Acesse: /ofertas/nova
2. No campo "Descrição do produto", use o editor HTML:
   - Clique em "B" para negrito
   - Clique em "I" para itálico
   - Clique em "•" para lista
3. Salve a oferta
```

---

### 2. Criar Template com Namespace de Descrição

```
1. Acesse: /templates/novo
2. No corpo do template, adicione:
   
   {product_name}
   
   {product_description}
   
   Preço: {price}
   
3. Salve o template
```

---

### 3. Gerar Texto para Compartilhamento

```
1. Acesse: /ofertas/1/compartilhar
2. Selecione uma rede social (ex: WhatsApp)
3. Selecione um template
4. Veja o texto gerado com formatação correta!
5. Clique em "Copiar texto"
6. Cole no WhatsApp → formatação aparece corretamente!
```

---

## ✅ Benefícios

### Para o Usuário
- ✅ Escreve uma vez no editor visual
- ✅ Funciona em todas as redes sociais
- ✅ Formatação automática e inteligente
- ✅ Não precisa saber sintaxe de cada rede

### Para as Mensagens
- ✅ Negrito e itálico nativos do WhatsApp
- ✅ Listas bem formatadas
- ✅ Quebras de linha corretas
- ✅ Remoção automática de código HTML

### Para o Sistema
- ✅ Conversão client-side (rápida)
- ✅ Suporta múltiplas redes
- ✅ Fácil adicionar novas redes
- ✅ Código limpo e modular

---

## 🚀 Redes Sociais Suportadas

| Rede Social | Status | Formatação Suportada |
|-------------|--------|----------------------|
| ✅ WhatsApp | Completo | Negrito, itálico, riscado, código, listas |
| ✅ Telegram | Completo | Negrito, itálico, riscado, código, links MD |
| ✅ Instagram | Básico | Texto simples, quebras de linha, listas |
| ✅ Facebook | Básico | Texto simples, quebras de linha, listas |
| ✅ Twitter/X | Básico | Texto simples, quebras de linha, listas |

---

## 📊 Antes vs Depois

### WhatsApp

**Antes (HTML cru):**
```
<p>Produto <strong>incrível</strong></p><ul><li>Item 1</li></ul>
```

**Depois (formatado):**
```
Produto *incrível*

• Item 1
```

---

### Telegram

**Antes:**
```
<h2>Título</h2><p>Texto <em>importante</em></p>
```

**Depois:**
```
**Título**

Texto __importante__
```

---

## 🎯 Casos de Uso

### 1. E-commerce
```html
Editor:
<h3>Notebook Gamer</h3>
<ul>
  <li><strong>Processador:</strong> Intel i7</li>
  <li><strong>RAM:</strong> 16GB</li>
  <li><strong>SSD:</strong> 512GB</li>
</ul>

WhatsApp:
*Notebook Gamer*

• *Processador:* Intel i7
• *RAM:* 16GB
• *SSD:* 512GB
```

---

### 2. Promoções
```html
Editor:
<h2>OFERTA EXCLUSIVA</h2>
<p><s>R$ 999</s> → <strong>R$ 699</strong></p>
<p><em>Apenas hoje!</em></p>

WhatsApp:
*OFERTA EXCLUSIVA*

~R$ 999~ → *R$ 699*

_Apenas hoje!_
```

---

## 🎉 Conclusão

Sistema completo de conversão HTML para texto formatado implementado com sucesso!

- ✅ **Função JavaScript** de conversão inteligente
- ✅ **5 redes sociais** suportadas
- ✅ **3 namespaces** disponíveis
- ✅ **Formatação automática** por rede
- ✅ **Editor HTML visual** integrado
- ✅ **Limpeza de código** automática

**Status:** 🟢 **COMPLETO E PRONTO PARA USO**

---

**Última atualização:** 04/12/2025

