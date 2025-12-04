# 🎨 Formatação Automática para Redes Sociais

## 📋 Visão Geral

O sistema converte automaticamente a formatação HTML do editor Quill.js para o formato específico de cada rede social na hora de compartilhar ofertas e cupons.

**Editor → Rede Social**
```
HTML (Quill.js) → Conversão automática → Formato da rede social
```

---

## 🔄 Conversão de Formatação

### Tabela de Compatibilidade

| Formatação | HTML | WhatsApp | Telegram | Instagram | Facebook | Twitter/X | LinkedIn | TikTok |
|------------|------|----------|----------|-----------|----------|-----------|----------|--------|
| **Negrito** | `<strong>` `<b>` | `*texto*` | `**texto**` | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Itálico** | `<em>` `<i>` | `_texto_` | `__texto__` | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Riscado** | `<s>` `<del>` | `~texto~` | `~~texto~~` | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Sublinhado** | `<u>` | `*texto*` | `__texto__` | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Código** | `<code>` | ` ```texto``` ` | `` `texto` `` | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Link** | `<a>` | `texto (url)` | `[texto](url)` | `texto (url)` | `texto (url)` | `texto (url)` | `texto: url` | `texto (url)` |
| **Lista** | `<ul>` `<li>` | `• item` | `• item` | `• item` | `• item` | `• item` | `• item` | `• item` |
| **Título** | `<h1>` | `*TÍTULO*` | `**TÍTULO**` | `TÍTULO` | `TÍTULO` | `TÍTULO` | `TÍTULO` | `TÍTULO` |
| **Citação** | `<blockquote>` | `❝ texto ❞` | `> texto` | `"texto"` | `"texto"` | `"texto"` | `"texto"` | `"texto"` |
| **Linha** | `<hr>` | `━━━━━━━` | `━━━━━━━` | `━━━━━━━` | `━━━━━━━` | `━━━━━━━` | `━━━━━━━` | `━━━━━━━` |

---

## 📱 WhatsApp

### Formatações Suportadas

O WhatsApp usa formatação **Markdown simples**:

| Formato | Sintaxe | Exemplo |
|---------|---------|---------|
| Negrito | `*texto*` | *Oferta Imperdível* |
| Itálico | `_texto_` | _Não perca_ |
| Riscado | `~texto~` | ~R$ 100~ |
| Monospace | ` ```texto``` ` | ```DESC10``` |

### Exemplos de Conversão

**Editor HTML:**
```html
<p><strong>Oferta Especial!</strong></p>
<p>De <s>R$ 499</s> por apenas <strong>R$ 399</strong></p>
<p><em>Válido até amanhã</em></p>
```

**Resultado WhatsApp:**
```
*Oferta Especial!*

De ~R$ 499~ por apenas *R$ 399*

_Válido até amanhã_
```

### Recursos Adicionais

- **Títulos** (`<h1>`, `<h2>`, etc.) → Convertidos para `*TEXTO MAIÚSCULO*`
- **Listas** → Convertidas para bullet points `•`
- **Links** → Exibidos como `texto (url)`
- **Citações** → Convertidas para `❝ texto ❞`
- **Sublinhado** → Convertido para `*negrito*` (WhatsApp não suporta sublinhado)

---

## 📨 Telegram

### Formatações Suportadas

O Telegram usa **Markdown v2**:

| Formato | Sintaxe | Exemplo |
|---------|---------|---------|
| Negrito | `**texto**` | **Oferta Imperdível** |
| Itálico | `__texto__` | __Não perca__ |
| Riscado | `~~texto~~` | ~~R$ 100~~ |
| Monospace | `` `texto` `` | `DESC10` |
| Link | `[texto](url)` | [Clique aqui](https://...) |

### Exemplos de Conversão

**Editor HTML:**
```html
<p><strong>Controle PS5</strong></p>
<p>Preço: <s>R$ 499</s> → <strong>R$ 399</strong></p>
<p>Use o código: <code>GAME10</code></p>
<p><a href="https://link.com">Comprar agora</a></p>
```

**Resultado Telegram:**
```
**Controle PS5**

Preço: ~~R$ 499~~ → **R$ 399**

Use o código: `GAME10`

[Comprar agora](https://link.com)
```

### Recursos Adicionais

- **Títulos** → `**TEXTO MAIÚSCULO**`
- **Listas** → Bullet points `•`
- **Citações** → `> texto`
- **Código em bloco** → ` ```texto``` `

---

## 💼 LinkedIn

### Formatações Suportadas

O LinkedIn **não suporta formatação rica**, mas preserva a estrutura:

| Formato | Conversão |
|---------|-----------|
| Negrito, Itálico, etc. | Removido (texto puro) |
| Títulos | TEXTO MAIÚSCULO |
| Listas | • item |
| Links | texto: url |
| Citações | "texto" |

### Exemplo de Conversão

**Editor HTML:**
```html
<h2>Oferta Especial</h2>
<p><strong>Produto:</strong> Controle PS5</p>
<ul>
  <li>Wireless</li>
  <li>Bateria de longa duração</li>
</ul>
<p><a href="https://link.com">Mais informações</a></p>
```

**Resultado LinkedIn:**
```
OFERTA ESPECIAL

Produto: Controle PS5

• Wireless
• Bateria de longa duração

Mais informações: https://link.com
```

---

## 📷 Instagram / 📘 Facebook / 🐦 Twitter / 🎵 TikTok

### Formatações Suportadas

Essas plataformas **não suportam formatação de texto**, apenas:

| Recurso | Suporte |
|---------|---------|
| Negrito, Itálico, Riscado | ❌ Removido |
| Títulos | ✅ MAIÚSCULAS |
| Listas | ✅ Bullet points |
| Quebras de linha | ✅ Preservadas |
| Links | ✅ URL visível |
| Emojis | ✅ Funcionam normalmente |

### Exemplo de Conversão

**Editor HTML:**
```html
<h2>Oferta Imperdível!</h2>
<p><strong>Controle PS5</strong></p>
<p>De <s>R$ 499</s> por apenas R$ 399</p>
<ul>
  <li>Frete grátis</li>
  <li>12x sem juros</li>
</ul>
```

**Resultado Instagram/Facebook/Twitter/TikTok:**
```
OFERTA IMPERDÍVEL!

Controle PS5

De R$ 499 por apenas R$ 399

• Frete grátis
• 12x sem juros
```

**💡 Dica:** Como essas redes não suportam formatação, use:
- **MAIÚSCULAS** para destaque
- **Emojis** para visual (🔥, 💰, 🎁, ⚡, ✨)
- **Quebras de linha** para organização
- **Símbolos** (━━━, ══, ••, →, ★)

---

## 🎯 Exemplos Práticos

### Exemplo 1: Template de Oferta Completo

**No Editor (HTML):**
```html
<h1>🔥 OFERTA RELÂMPAGO!</h1>

<p><strong>Controle PS5 DualSense</strong></p>
<p>De <s>R$ 499,00</s> por apenas <strong>R$ 399,00</strong></p>

<p><em>Características:</em></p>
<ul>
  <li>Conexão wireless</li>
  <li>Feedback tátil</li>
  <li>Bateria de longa duração</li>
</ul>

<blockquote>Aproveite enquanto durar o estoque!</blockquote>

<p>Use o cupom: <code>GAME10</code></p>

<p><a href="https://link.com">🛒 Comprar agora</a></p>
```

**Resultado WhatsApp:**
```
*🔥 OFERTA RELÂMPAGO!*

*Controle PS5 DualSense*
De ~R$ 499,00~ por apenas *R$ 399,00*

_Características:_
• Conexão wireless
• Feedback tátil
• Bateria de longa duração

❝ Aproveite enquanto durar o estoque! ❞

Use o cupom: ```GAME10```

🛒 Comprar agora (https://link.com)
```

**Resultado Telegram:**
```
**🔥 OFERTA RELÂMPAGO!**

**Controle PS5 DualSense**
De ~~R$ 499,00~~ por apenas **R$ 399,00**

__Características:__
• Conexão wireless
• Feedback tátil
• Bateria de longa duração

> Aproveite enquanto durar o estoque!

Use o cupom: `GAME10`

[🛒 Comprar agora](https://link.com)
```

**Resultado Instagram/Facebook/Twitter/TikTok:**
```
🔥 OFERTA RELÂMPAGO!

Controle PS5 DualSense
De R$ 499,00 por apenas R$ 399,00

Características:
• Conexão wireless
• Feedback tátil
• Bateria de longa duração

"Aproveite enquanto durar o estoque!"

Use o cupom: GAME10

🛒 Comprar agora (https://link.com)
```

---

### Exemplo 2: Template com Cupons

**No Editor (HTML):**
```html
<h2>💰 CUPONS DISPONÍVEIS</h2>

<p><strong>Descontos especiais:</strong></p>
<ul>
  <li><code>DESC10</code> - 10% de desconto</li>
  <li><code>FRETE</code> - Frete grátis</li>
  <li><code>NATAL20</code> - R$ 20 OFF</li>
</ul>

<hr>

<p><em>Válido até 31/12/2025</em></p>
```

**Resultado WhatsApp:**
```
*💰 CUPONS DISPONÍVEIS*

*Descontos especiais:*
• ```DESC10``` - 10% de desconto
• ```FRETE``` - Frete grátis
• ```NATAL20``` - R$ 20 OFF

━━━━━━━━━━━━━━━━━━

_Válido até 31/12/2025_
```

**Resultado Telegram:**
```
**💰 CUPONS DISPONÍVEIS**

**Descontos especiais:**
• `DESC10` - 10% de desconto
• `FRETE` - Frete grátis
• `NATAL20` - R$ 20 OFF

━━━━━━━━━━━━━━━━━━

__Válido até 31/12/2025__
```

---

## 📝 Dicas de Uso

### ✅ Boas Práticas

1. **Use emojis** - Funcionam em todas as redes sociais
2. **Organize com quebras de linha** - Facilitam a leitura
3. **Destaque preços** - Use negrito no editor
4. **Separe seções** - Use `<hr>` ou linhas de separação
5. **Teste em múltiplas redes** - Veja a prévia antes de compartilhar

### ⚠️ Evite

1. **Excesso de formatação** - Pode poluir visualmente
2. **Formatação complexa** - Nem todas as redes suportam
3. **Links muito longos** - Use encurtadores quando necessário
4. **Muitas maiúsculas** - Pode parecer spam

---

## 🔧 Formatações do Quill.js

### Tags HTML Reconhecidas

| Elemento | Tag HTML | Descrição |
|----------|----------|-----------|
| Negrito | `<strong>`, `<b>` | Texto em negrito |
| Itálico | `<em>`, `<i>` | Texto em itálico |
| Sublinhado | `<u>` | Texto sublinhado |
| Riscado | `<s>`, `<del>`, `<strike>` | Texto tachado |
| Código | `<code>`, `<pre>` | Texto monoespaçado |
| Títulos | `<h1>` a `<h6>` | Cabeçalhos |
| Parágrafo | `<p>` | Parágrafo de texto |
| Lista | `<ul>`, `<ol>`, `<li>` | Listas com marcadores |
| Link | `<a href="...">` | Hiperlinks |
| Citação | `<blockquote>` | Bloco de citação |
| Linha horizontal | `<hr>` | Separador visual |
| Quebra | `<br>` | Quebra de linha |

---

## 🚀 Como Usar

### Passo a Passo

1. **Criar Template** (`/templates/novo`)
   - Use o editor Quill.js para formatar o texto
   - Aplique negrito, itálico, listas, etc.
   - Insira namespaces (`{product_name}`, `{price}`, etc.)

2. **Criar Oferta** (`/ofertas/nova`)
   - Preencha os dados do produto
   - Use o editor HTML para a descrição

3. **Compartilhar** (`/ofertas/<id>/compartilhar`)
   - Selecione a rede social
   - Selecione o template
   - **Veja a prévia** com formatação convertida
   - Copie e cole na rede social

### Exemplo de Uso

```javascript
// O sistema converte automaticamente:

// Entrada (HTML do editor):
"<strong>Oferta</strong> <em>especial</em>!"

// WhatsApp:
"*Oferta* _especial_!"

// Telegram:
"**Oferta** __especial__!"

// Instagram/Facebook/Twitter/TikTok:
"Oferta especial!"
```

---

## 📊 Compatibilidade

| Rede Social | Formatação Rica | Markdown | HTML | Links Clicáveis |
|-------------|-----------------|----------|------|-----------------|
| WhatsApp | ✅ Limitada | ✅ Sim | ❌ Não | ✅ Sim |
| Telegram | ✅ Completa | ✅ Sim | ✅ Parcial | ✅ Sim |
| Instagram | ❌ Não | ❌ Não | ❌ Não | ⚠️ Bio apenas |
| Facebook | ❌ Não | ❌ Não | ❌ Não | ✅ Sim |
| Twitter/X | ❌ Não | ❌ Não | ❌ Não | ✅ Sim |
| LinkedIn | ❌ Não | ❌ Não | ❌ Não | ✅ Sim |
| TikTok | ❌ Não | ❌ Não | ❌ Não | ⚠️ Bio apenas |

---

## 🔍 Referências

### WhatsApp
- Formatação oficial: https://faq.whatsapp.com/539178204879377/
- Suporte: Negrito, Itálico, Riscado, Monospace

### Telegram
- Formatação oficial: https://core.telegram.org/bots/api#formatting-options
- Suporte: Markdown v2, HTML limitado

### Outras Redes
- Instagram, Facebook, Twitter, TikTok, LinkedIn: Texto puro apenas
- Use emojis e estrutura para destaque visual

---

**Última Atualização:** 04/12/2025  
**Versão:** 2.0  
**Status:** ✅ Completo e Testado

