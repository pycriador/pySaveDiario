# 📱 Guia Rápido: Redes Sociais e Cupons

**Atualizado:** 3 de Dezembro, 2025

---

## 🎯 O que mudou?

Agora você pode:

1. ✅ **Configurar hashtags e textos** específicos para cada rede social
2. ✅ **Selecionar cupons ativos** ao compartilhar ofertas

---

## 🔧 1. Configurar Redes Sociais

### Acesso
```
Menu → Administração → Redes Sociais
```

### O que você encontra?
4 cards, um para cada rede social:
- 📷 **Instagram**
- 📘 **Facebook**  
- 💬 **WhatsApp**
- ✈️ **Telegram**

### O que configurar?

#### **Texto Inicial (Prefixo)**
Aparece **ANTES** do conteúdo do template.

**Exemplo para Facebook:**
```
🔥 OFERTA IMPERDÍVEL!

```
*Nota: As quebras de linha (`\n\n`) são importantes!*

#### **Texto Final / Hashtags (Sufixo)**
Aparece **DEPOIS** do conteúdo do template.

**Exemplo para Instagram:**
```
#ofertas #descontos #promoção #blackfriday
```

#### **Ativar/Desativar**
Use o switch para ativar ou desativar cada rede.

### Configurações Padrão

Já vêm pré-configuradas:

| Rede | Prefixo | Sufixo |
|------|---------|--------|
| Instagram | *(vazio)* | `#ofertas #descontos #promoção` |
| Facebook | `🔥 OFERTA IMPERDÍVEL!\n\n` | `\n\n👍 Curta nossa página!` |
| WhatsApp | `💰 *PROMOÇÃO*\n\n` | `\n\n_Compartilhe!_` |
| Telegram | `📢 NOVA OFERTA!\n\n` | `\n\n🔔 Ative as notificações!` |

---

## 🎟️ 2. Compartilhar com Cupons

### Passo a Passo

#### 1. Acesse uma oferta
```
/ofertas → Escolha uma oferta
```

#### 2. Clique no botão de rede social
Exemplo: Clique no botão **Instagram** (📷)

#### 3. Veja o modal com 2 seções:

**A) Cupons Ativos (Opcional)**
```
☑ PRIMEIRACOMPRA - Mercado Livre
☐ FRETE10 - Shopee
☐ BLACK50 - Magazine Luiza
```
*Marque os cupons que deseja incluir*

**B) Templates**
```
📄 Template Black Friday
📄 Template Promoção Relâmpago
```
*Clique no template desejado*

#### 4. Resultado
O texto será gerado assim:

```
[PREFIXO DA REDE]
[CONTEÚDO DO TEMPLATE COM VARIÁVEIS SUBSTITUÍDAS]
[CUPONS SELECIONADOS]
[SUFIXO DA REDE]
```

**Exemplo completo:**
```
Notebook Dell Inspiron por apenas R$ 2.499!

Estava R$ 3.499, agora com 29% de desconto!

Aproveite: https://mercadolivre.com.br/...

🎟️ CUPONS DISPONÍVEIS:
• PRIMEIRACOMPRA - Mercado Livre

#ofertas #descontos #promoção
```

---

## 💡 Dicas de Uso

### Hashtags Sazonais
Atualize as hashtags conforme a época:

**Black Friday:**
```
#blackfriday #blackfriday2025 #ofertas #descontos
```

**Natal:**
```
#natal #presentedenatal #ofertas #presentes
```

**Volta às Aulas:**
```
#voltaasaulas #papelaria #ofertas #escola
```

### Emojis Estratégicos
Use emojis para chamar atenção:

- 🔥 Oferta quente
- 💰 Economia
- 🎁 Presente
- ⚡ Relâmpago
- 🚀 Lançamento
- ⏰ Última chance

### Formatação WhatsApp
No WhatsApp, use Markdown:

```
💰 *PROMOÇÃO IMPERDÍVEL*

Notebook Dell por apenas *R$ 2.499*!

_Aproveite enquanto durar!_
```

### Chamadas para Ação (CTA)
No Facebook/Telegram, adicione CTAs no sufixo:

```

👍 Curta nossa página para não perder promoções!
🔔 Ative as notificações!
💬 Comente "EU QUERO"!
```

---

## 🎯 Casos de Uso

### Caso 1: Oferta Simples (sem cupom)
1. Clique em Instagram
2. **NÃO** marque nenhum cupom
3. Selecione template
4. Copie e cole no Instagram

**Resultado:**
```
[Template] + [Hashtags]
```

### Caso 2: Oferta com 1 Cupom
1. Clique em WhatsApp
2. Marque o cupom `FRETE10`
3. Selecione template
4. Copie e cole no WhatsApp

**Resultado:**
```
[Prefixo] + [Template] + [Cupom] + [Sufixo]
```

### Caso 3: Oferta com Múltiplos Cupons
1. Clique em Telegram
2. Marque 2 cupons: `PRIMEIRACOMPRA` e `FRETE10`
3. Selecione template
4. Copie e cole no Telegram

**Resultado:**
```
[Prefixo] + [Template] + 
🎟️ CUPONS DISPONÍVEIS:
• PRIMEIRACOMPRA - Mercado Livre
• FRETE10 - Mercado Livre
[Sufixo]
```

---

## ⚠️ Observações Importantes

### 1. Cupons Expirados
Apenas cupons **ativos** e **não expirados** aparecem na lista.

### 2. Ordem de Montagem
O texto SEMPRE segue esta ordem:
1. Prefixo da rede (se houver)
2. Conteúdo do template
3. Cupons selecionados (se houver)
4. Sufixo da rede (se houver)

### 3. Templates com Variáveis
As variáveis do template são substituídas automaticamente:
- `{product_name}` → Nome do produto
- `{price}` → Preço atual
- `{old_price}` → Preço antigo
- `{discount}` → Percentual de desconto
- `{vendor_name}` → Nome do vendedor
- `{offer_url}` → Link da oferta

### 4. Persistência
As configurações de redes sociais ficam salvas no banco de dados. Você só precisa configurar uma vez!

---

## 🔧 Solução de Problemas

### Problema: "Nenhum cupom aparece"
**Solução:** 
- Verifique se há cupons ativos em `/cupons`
- Certifique-se de que não expiraram
- Confirme que o campo "Ativo" está marcado

### Problema: "Hashtags não aparecem"
**Solução:**
- Acesse `/admin/social-networks`
- Verifique o campo "Texto Final / Hashtags"
- Clique em "Salvar"
- Tente compartilhar novamente

### Problema: "Texto Final quebrado"
**Solução:**
Use `\n\n` para quebras de linha:
```
Texto linha 1

Texto linha 2
```

### Problema: "Rede social desabilitada"
**Solução:**
- Acesse `/admin/social-networks`
- Ative o switch da rede
- Clique em "Salvar"

---

## 📊 Melhores Práticas

### Hashtags
- **Instagram:** 10-15 hashtags
- **Facebook:** 2-3 hashtags
- **Twitter/X:** 1-2 hashtags
- **LinkedIn:** 3-5 hashtags

### Emojis
- Use com moderação (2-3 por post)
- Escolha emojis relevantes ao produto
- Evite sequências longas de emojis

### Texto
- **Instagram:** Até 2.200 caracteres
- **Facebook:** Até 63.206 caracteres (mas idealmente < 500)
- **WhatsApp:** Até 65.536 caracteres
- **Telegram:** Até 4.096 caracteres

### Cupons
- Sempre teste os cupons antes
- Inclua a data de validade no texto
- Mencione restrições (se houver)

---

## ✅ Checklist para Compartilhamento Perfeito

Antes de compartilhar, verifique:

- [ ] Configurações de rede social atualizadas
- [ ] Hashtags relevantes e atualizadas
- [ ] Template selecionado contém todas variáveis necessárias
- [ ] Cupons selecionados estão válidos
- [ ] Texto gerado está completo e formatado
- [ ] Link da oferta funciona
- [ ] Preços estão corretos
- [ ] Nome do produto está certo

---

## 🎊 Pronto para Usar!

Agora você tem controle total sobre:
- 🎨 Personalização por rede social
- 🎟️ Inclusão automática de cupons
- 📝 Templates dinâmicos
- 📱 Compartilhamento profissional

**Comece agora:**
1. Configure suas redes em `/admin/social-networks`
2. Crie cupons em `/cupons/novo`
3. Compartilhe ofertas em `/ofertas`

---

**Dúvidas?** Consulte a documentação completa em `docs/SOCIAL_NETWORKS_AND_COUPONS_SHARE.md`

