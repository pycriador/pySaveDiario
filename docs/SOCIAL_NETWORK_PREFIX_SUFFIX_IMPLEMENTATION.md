# 🎨 Implementação de Prefixos e Sufixos de Redes Sociais

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.6.1  
**Status:** ✅ IMPLEMENTADO

---

## 🎯 O que foi implementado?

Agora, ao compartilhar **ofertas** ou **cupons**, os textos configurados em `/admin/social-networks` são aplicados automaticamente:

- **Prefixo (Texto Inicial):** Aparece ANTES do conteúdo do template
- **Sufixo (Texto Final / Hashtags):** Aparece DEPOIS do conteúdo (incluindo cupons, se houver)

---

## 📊 Estrutura do Texto Final

### Para Ofertas
```
[PREFIXO DA REDE]
[CONTEÚDO DO TEMPLATE COM VARIÁVEIS SUBSTITUÍDAS]
[CUPONS SELECIONADOS - se houver]
[SUFIXO DA REDE]
```

### Para Cupons
```
[PREFIXO DA REDE]
[CONTEÚDO DO TEMPLATE COM VARIÁVEIS SUBSTITUÍDAS]
[SUFIXO DA REDE]
```

---

## 🔧 Como Funciona

### 1. Configuração (Admin)

**Acesse:** `/admin/social-networks`

**Configure cada rede:**

**Instagram:**
```
Prefixo: [vazio]
Sufixo: #ofertas #descontos #promoção
```

**Facebook:**
```
Prefixo: 🔥 OFERTA IMPERDÍVEL!

Sufixo: 

👍 Curta nossa página para não perder promoções!
```

**WhatsApp:**
```
Prefixo: 💰 *PROMOÇÃO*

Sufixo: 

_Compartilhe com quem precisa!_
```

**Telegram:**
```
Prefixo: 📢 NOVA OFERTA!

Sufixo: 

🔔 Ative as notificações do canal!
```

### 2. Compartilhamento (Ofertas)

**Exemplo passo a passo:**

1. Usuário acessa `/ofertas`
2. Clica no botão **Instagram** de uma oferta
3. Seleciona cupons (opcional)
4. Seleciona template: "Notebook Dell por {price}!"
5. Sistema gera o texto:

```
Notebook Dell por R$ 2.499!

🎟️ CUPONS DISPONÍVEIS:
• PRIMEIRACOMPRA - Mercado Livre

#ofertas #descontos #promoção
```

**Note:** 
- Prefixo do Instagram está vazio
- Cupom foi adicionado
- Sufixo (hashtags) foi adicionado ao final

### 3. Compartilhamento (Cupons)

**Exemplo passo a passo:**

1. Usuário acessa `/cupons`
2. Clica no botão **Facebook** de um cupom
3. Seleciona template: "Use o cupom {code} na {seller}!"
4. Sistema gera o texto:

```
🔥 OFERTA IMPERDÍVEL!

Use o cupom PRIMEIRACOMPRA na Mercado Livre!

👍 Curta nossa página para não perder promoções!
```

**Note:**
- Prefixo do Facebook foi adicionado
- Conteúdo do template com variáveis substituídas
- Sufixo do Facebook foi adicionado

---

## 💻 Implementação Técnica

### Backend (Python)

#### 1. Rota de Ofertas (`web.py`)
```python
# Get social network configurations
social_configs = SocialNetworkConfig.query.filter_by(active=True).all()

return render_template("offers_list.html", 
                     # ...
                     social_configs=social_configs)
```

#### 2. Rota de Cupons (`web.py`)
```python
# Get social network configurations
social_configs = SocialNetworkConfig.query.filter_by(active=True).all()

return render_template("coupons_list.html", 
                     # ...
                     social_configs=social_configs)
```

### Frontend (JavaScript)

#### 1. Objeto de Configurações (Jinja2 → JS)

**Em `offers_list.html` e `coupons_list.html`:**
```javascript
// Social network configurations
const socialNetworkConfigs = {
  {% if social_configs %}
  {% for config in social_configs %}
  '{{ config.network }}': {
    prefix: {{ (config.prefix_text or '')|tojson }},
    suffix: {{ (config.suffix_text or '')|tojson }}
  }{{ ',' if not loop.last else '' }}
  {% endfor %}
  {% endif %}
};
```

**Resultado no navegador:**
```javascript
const socialNetworkConfigs = {
  'instagram': {
    prefix: "",
    suffix: "#ofertas #descontos #promoção"
  },
  'facebook': {
    prefix: "🔥 OFERTA IMPERDÍVEL!\n\n",
    suffix: "\n\n👍 Curta nossa página!"
  },
  'whatsapp': {
    prefix: "💰 *PROMOÇÃO*\n\n",
    suffix: "\n\n_Compartilhe!_"
  },
  'telegram': {
    prefix: "📢 NOVA OFERTA!\n\n",
    suffix: "\n\n🔔 Ative as notificações!"
  }
};
```

#### 2. Aplicação no Texto (Ofertas)

**Função `selectOfferTemplate()` em `offers_list.html`:**
```javascript
// ... substituição de variáveis do template ...

// Append coupons if selected
if (selectedCoupons.length > 0) {
  text += '\n\n🎟️ CUPONS DISPONÍVEIS:\n';
  selectedCoupons.forEach(coupon => {
    text += `• ${coupon.code} - ${coupon.seller}\n`;
  });
}

// Apply social network prefix and suffix
const channel = currentOfferData.channel.toLowerCase();
if (socialNetworkConfigs[channel]) {
  const config = socialNetworkConfigs[channel];
  const prefix = config.prefix || '';
  const suffix = config.suffix || '';
  text = prefix + text + suffix;  // ← APLICAÇÃO AQUI
}

// Show in modal
document.getElementById('shareText').value = text;
```

#### 3. Aplicação no Texto (Cupons)

**Função `selectTemplate()` em `coupons_list.html`:**
```javascript
// ... substituição de variáveis do template ...

// Apply social network prefix and suffix
const channel = currentCouponData.channel.toLowerCase();
if (socialNetworkConfigs[channel]) {
  const config = socialNetworkConfigs[channel];
  const prefix = config.prefix || '';
  const suffix = config.suffix || '';
  text = prefix + text + suffix;  // ← APLICAÇÃO AQUI
}

// Show in modal
document.getElementById('shareText').value = text;
```

---

## 📂 Arquivos Modificados

### Backend
```
app/routes/web.py
  - Função offers(): Adicionado social_configs
  - Função coupons(): Adicionado social_configs
```

### Frontend
```
app/templates/offers_list.html
  - Adicionado objeto socialNetworkConfigs
  - Atualizada função selectOfferTemplate()

app/templates/coupons_list.html
  - Adicionado objeto socialNetworkConfigs
  - Atualizada função selectTemplate()
```

---

## 🧪 Testes

### Teste 1: Prefixo do Facebook em Oferta
```
1. Configure prefixo do Facebook: "🔥 OFERTA!\n\n"
2. Vá para /ofertas
3. Clique no botão Facebook de uma oferta
4. Selecione um template
5. Verifique que o texto começa com "🔥 OFERTA!"
✅ PASSOU
```

### Teste 2: Sufixo do Instagram em Cupom
```
1. Configure sufixo do Instagram: "#cupom #desconto"
2. Vá para /cupons
3. Clique no botão Instagram de um cupom
4. Selecione um template
5. Verifique que o texto termina com "#cupom #desconto"
✅ PASSOU
```

### Teste 3: Oferta com Cupom + Prefixo/Sufixo
```
1. Configure WhatsApp: Prefixo "💰 PROMO\n\n" + Sufixo "\n\nCompartilhe!"
2. Vá para /ofertas
3. Clique no botão WhatsApp
4. Marque 1 cupom
5. Selecione template
6. Verifique ordem:
   - "💰 PROMO" (prefixo)
   - Conteúdo do template
   - "🎟️ CUPONS DISPONÍVEIS:" (cupom)
   - "Compartilhe!" (sufixo)
✅ PASSOU
```

### Teste 4: Rede sem Prefixo/Sufixo
```
1. Configure Instagram: Prefixo vazio + Sufixo vazio
2. Vá para /ofertas
3. Clique no botão Instagram
4. Selecione template
5. Verifique que aparece apenas o conteúdo do template
✅ PASSOU
```

---

## 🎯 Exemplos Práticos

### Exemplo 1: Instagram - Oferta Simples
**Configuração:**
- Prefixo: *(vazio)*
- Sufixo: `#ofertas #descontos`

**Template:**
```
Notebook Dell por {price}!
Link: {url}
```

**Resultado:**
```
Notebook Dell por R$ 2.499!
Link: https://...

#ofertas #descontos
```

### Exemplo 2: Facebook - Oferta com Cupom
**Configuração:**
- Prefixo: `🔥 IMPERDÍVEL!\n\n`
- Sufixo: `\n\n👍 Curta!`

**Template:**
```
{product_name} por apenas {price}!
```

**Cupom selecionado:** FRETE10 - Mercado Livre

**Resultado:**
```
🔥 IMPERDÍVEL!

Notebook Dell por apenas R$ 2.499!

🎟️ CUPONS DISPONÍVEIS:
• FRETE10 - Mercado Livre

👍 Curta!
```

### Exemplo 3: WhatsApp - Cupom
**Configuração:**
- Prefixo: `💰 *CUPOM*\n\n`
- Sufixo: `\n\n_Aproveite!_`

**Template:**
```
Use {code} na {seller}!
```

**Resultado:**
```
💰 *CUPOM*

Use PRIMEIRACOMPRA na Mercado Livre!

_Aproveite!_
```

### Exemplo 4: Telegram - Oferta com Desconto
**Configuração:**
- Prefixo: `📢 NOVA OFERTA!\n\n`
- Sufixo: `\n\n🔔 Ative notificações!`

**Template:**
```
{product_name} - De {old_price} por {price}!
Desconto de {discount}!
```

**Resultado:**
```
📢 NOVA OFERTA!

Notebook Dell - De R$ 3.499 por R$ 2.499!
Desconto de 29%!

🔔 Ative notificações!
```

---

## 💡 Dicas de Uso

### Hashtags Estratégicas
- **Instagram:** Use 10-15 hashtags variadas
- **Facebook:** 2-3 hashtags específicas
- **Twitter:** 1-2 hashtags curtas
- **LinkedIn:** 3-5 hashtags profissionais

### Formatação
- **WhatsApp:** Use `*negrito*`, `_itálico_`, `~riscado~`
- **Telegram:** Suporta Markdown
- **Facebook/Instagram:** Texto simples + emojis

### Quebras de Linha
Use `\n\n` para criar parágrafos:
```
Linha 1

Linha 2 (com espaço entre)
```

### Emojis Efetivos
- 🔥 = Quente/Trending
- 💰 = Economia
- 🎁 = Presente
- ⚡ = Rápido
- 🚀 = Novo
- ⏰ = Urgente

---

## ✅ Checklist de Implementação

- [x] Adicionar `social_configs` na rota `offers()`
- [x] Adicionar `social_configs` na rota `coupons()`
- [x] Criar objeto `socialNetworkConfigs` em `offers_list.html`
- [x] Criar objeto `socialNetworkConfigs` em `coupons_list.html`
- [x] Atualizar `selectOfferTemplate()` para aplicar prefix/suffix
- [x] Atualizar `selectTemplate()` para aplicar prefix/suffix
- [x] Testar com todas as redes sociais
- [x] Testar com cupons
- [x] Testar prefixo vazio
- [x] Testar sufixo vazio
- [x] Documentar implementação

---

## 🎊 Status

**✅ IMPLEMENTADO E FUNCIONANDO!**

Agora as configurações de `/admin/social-networks` são aplicadas automaticamente em:
- ✅ Compartilhamento de ofertas
- ✅ Compartilhamento de cupons
- ✅ Todas as 4 redes sociais
- ✅ Com ou sem cupons selecionados

---

## 📚 Documentos Relacionados

- `docs/SOCIAL_NETWORKS_AND_COUPONS_SHARE.md` - Documentação técnica completa
- `docs/GUIA_USO_REDES_SOCIAIS.md` - Guia para usuários
- `docs/RESUMO_REDES_SOCIAIS_E_CUPONS.md` - Resumo da implementação

---

**Configurações de redes sociais agora funcionam em ofertas E cupons! 🎉**

