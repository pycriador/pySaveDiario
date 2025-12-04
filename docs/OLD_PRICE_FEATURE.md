# 💰 Feature: Preço Antigo e Cálculo de Desconto

**Data:** 3 de Dezembro, 2025  
**Versão:** 2.9.0

---

## ✨ O Que Foi Implementado

### 1. **Novo Campo: `old_price`**
- ✅ Adicionado campo `old_price` no modelo `Offer`
- ✅ Campo opcional (nullable=True)
- ✅ Tipo: `Numeric(10, 2)` - suporta valores decimais
- ✅ Migração criada e aplicada automaticamente

### 2. **Formulário Atualizado**
- ✅ Novo campo "Preço Antigo" no formulário de criação de ofertas
- ✅ Campo opcional com placeholder "0.00"
- ✅ Ícone: `bi-cash-stack` (pilha de dinheiro)
- ✅ Texto de ajuda: "Opcional - Para mostrar desconto"
- ✅ Validação: apenas valores positivos

### 3. **Visualização com Desconto**
- ✅ Exibe preço antigo riscado (text-decoration-line-through)
- ✅ Calcula e mostra percentual de desconto
- ✅ Badge verde com "-XX%" quando há desconto
- ✅ Layout bonito e intuitivo

### 4. **Melhorias de Legibilidade (Tema Escuro)**
- ✅ Textos de ajuda (`text-muted`) agora em branco/cinza claro
- ✅ Cor: `#cbd5e1` (var(--text-secondary))
- ✅ Opacidade: 0.9 para suavidade
- ✅ Tema claro mantém cor padrão do Bootstrap

---

## 📋 Arquivos Modificados

### Backend
1. **`app/models.py`**
   - Adicionado campo `old_price` no modelo `Offer`

2. **`app/forms.py`**
   - Adicionado `DecimalField` para `old_price`
   - Validação: Optional, NumberRange(min=0)

3. **`app/routes/web.py`**
   - Atualizado `create_offer` para salvar `old_price`

### Frontend
4. **`app/templates/offer_create.html`**
   - Adicionado campo de input para preço antigo
   - Reorganizado layout: Preço Atual | Preço Antigo | Moeda

5. **`app/templates/offers_list.html`**
   - Exibe preço antigo riscado (se existir)
   - Calcula e exibe badge com percentual de desconto
   - Layout condicional baseado em `offer.old_price`

6. **`app/static/css/style.css`**
   - Melhorada legibilidade de `.text-muted` no tema escuro
   - Cor mais clara: `#cbd5e1`
   - Tema claro preservado

### Database
7. **`migrations/versions/9abfd19b8eec_add_old_price_to_offers.py`**
   - Migração automática criada pelo Flask-Migrate
   - Adiciona coluna `old_price` à tabela `offers`

---

## 🎨 Como Fica Visualmente

### No Formulário (Tema Escuro)
```
┌─────────────────────────────────────────────────────────┐
│ 💰 Preço Atual *        💵 Preço Antigo                 │
│ ┌─────────────┐        ┌─────────────┐                 │
│ │   99.90     │        │   149.90    │                 │
│ └─────────────┘        └─────────────┘                 │
│                        ℹ️  Opcional - Para mostrar...   │
│                                                         │
│ 💱 Moeda                                                │
│ ┌─────────────┐                                        │
│ │ BRL - Real  │                                        │
│ └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

### Na Lista de Ofertas
**Com Desconto:**
```
┌────────────────────────────┐
│ PS5 Pro                    │
│ ──────────────             │
│ 🏷️ BRL 2999.00              │
│    BRL 3999.00  [-25%]     │
│    ────────────  🟢        │
│ 🏪 Amazon                   │
│ ────────────────           │
│ Ver detalhes →             │
└────────────────────────────┘
```

**Sem Desconto:**
```
┌────────────────────────────┐
│ Xbox Series X              │
│ ──────────────             │
│ 🏷️ BRL 2499.90              │
│                            │
│ 🏪 Magazine Luiza           │
│ ────────────────           │
│ Ver detalhes →             │
└────────────────────────────┘
```

---

## 🔢 Cálculo de Desconto

### Fórmula Implementada
```python
desconto_percentual = ((old_price - price) / old_price) * 100
```

### Exemplo
```python
old_price = 3999.00  # Preço antigo
price = 2999.00       # Preço atual

desconto = ((3999.00 - 2999.00) / 3999.00) * 100
         = (1000.00 / 3999.00) * 100
         = 0.25006 * 100
         = 25.01%
         
# Formatado: -25% (arredondado)
```

---

## 💡 Exemplos de Uso

### 1. Criar Oferta COM Desconto
```
1. Acesse /ofertas/nova
2. Preencha:
   - Produto: "PS5 Pro"
   - Preço Atual: 2999.00
   - Preço Antigo: 3999.00  ← NOVO!
   - Moeda: BRL
3. Salvar
4. Na lista aparece:
   BRL 3999.00 (riscado)
   BRL 2999.00 [-25%] (badge verde)
```

### 2. Criar Oferta SEM Desconto
```
1. Acesse /ofertas/nova
2. Preencha:
   - Produto: "Xbox Series X"
   - Preço Atual: 2499.90
   - Preço Antigo: [deixar vazio] ← Campo opcional
   - Moeda: BRL
3. Salvar
4. Na lista aparece:
   BRL 2499.90 (sem preço riscado)
```

---

## 🎯 Validações

### Backend
- ✅ `old_price` é opcional (pode ser `None`)
- ✅ Se informado, deve ser ≥ 0
- ✅ Aceita até 2 casas decimais
- ✅ Tipo: `Decimal` (precisão financeira)

### Frontend
- ✅ Input type="number"
- ✅ Step="0.01" (centavos)
- ✅ Placeholder="0.00"
- ✅ Não é obrigatório (`required=False`)

### Exibição
- ✅ Badge de desconto só aparece se:
  - `old_price` existe E
  - `old_price > price` (desconto real)
- ✅ Formato do badge: `-XX%` (sem casas decimais)
- ✅ Cor do badge: verde (success)

---

## 🔐 Segurança

- ✅ Validação de tipo no backend (DecimalField)
- ✅ Validação de valor mínimo (>= 0)
- ✅ CSRF protection mantido
- ✅ Sanitização automática pelo SQLAlchemy

---

## 🎨 CSS Aplicado

### Preço Riscado
```css
.text-decoration-line-through {
  text-decoration: line-through;
}

font-size: 0.9rem;
color: text-muted;
```

### Badge de Desconto
```css
.badge.bg-success {
  background-color: #10b981 !important;
  color: white;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  margin-left: 0.5rem;
}
```

### Texto Muted (Tema Escuro) - NOVO!
```css
:root:not(.light-theme) .text-muted,
:root:not(.light-theme) small.text-muted {
  color: #cbd5e1 !important;  /* Mais claro! */
  opacity: 0.9;
}
```

---

## 📊 Schema do Banco de Dados

### Tabela: `offers`
```sql
CREATE TABLE offers (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    vendor_name VARCHAR(120) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    old_price NUMERIC(10, 2),          -- NOVO! (nullable)
    currency VARCHAR(3) DEFAULT 'BRL',
    offer_url VARCHAR(255),
    expires_at DATETIME,
    seller_id INTEGER,
    category_id INTEGER,
    manufacturer_id INTEGER,
    created_by_id INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (seller_id) REFERENCES sellers(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);
```

---

## 🚀 Migração

### Comando Executado
```bash
flask db migrate -m "add_old_price_to_offers"
flask db upgrade
```

### Resultado
```
INFO  [alembic.autogenerate.compare] Detected added column 'offers.old_price'
INFO  [alembic.runtime.migration] Running upgrade 42b51bfaa3e8 -> 9abfd19b8eec
```

### Arquivo Gerado
`migrations/versions/9abfd19b8eec_add_old_price_to_offers.py`

---

## ✅ Checklist de Implementação

- [x] Adicionar campo `old_price` no modelo
- [x] Criar formulário com campo opcional
- [x] Atualizar rota para salvar `old_price`
- [x] Gerar migração do banco de dados
- [x] Aplicar migração
- [x] Atualizar template de criação
- [x] Atualizar template de listagem
- [x] Implementar cálculo de desconto
- [x] Adicionar badge de percentual
- [x] Melhorar legibilidade no tema escuro
- [x] Testar com valores válidos
- [x] Testar com campo vazio
- [x] Documentar feature

---

## 🎓 Melhorias de UX

### Antes ❌
- Apenas um campo de preço
- Sem indicação de desconto
- Textos de ajuda difíceis de ler (cinza escuro)
- Sem visualização de economia

### Agora ✅
- Campo de preço antigo opcional
- Badge verde com percentual de desconto
- Textos de ajuda legíveis (cinza claro)
- Preço antigo riscado para contraste
- Cálculo automático de economia

---

## 📱 Responsividade

### Desktop
```
┌──────────────┬──────────────┬──────────────┐
│ Preço Atual  │ Preço Antigo │    Moeda     │
│   (col-3)    │    (col-3)   │   (col-3)    │
└──────────────┴──────────────┴──────────────┘
```

### Mobile
```
┌──────────────────┐
│  Preço Atual     │
│    (col-12)      │
├──────────────────┤
│  Preço Antigo    │
│    (col-12)      │
├──────────────────┤
│     Moeda        │
│    (col-12)      │
└──────────────────┘
```

---

## 🎯 Casos de Uso

### E-commerce / Marketplace
- Mostrar preços de/por
- Destacar promoções
- Aumentar conversão com descontos visíveis

### Comparação de Preços
- Histórico de preços
- Identificar melhores ofertas
- Rastrear variações de preço

### Ofertas Relâmpago
- Mostrar preço original
- Destacar economia
- Senso de urgência visual

---

## 🏆 Resultado Final

### Funcionalidades
- ✅ Campo opcional de preço antigo
- ✅ Cálculo automático de desconto
- ✅ Badge visual de economia
- ✅ Preço antigo riscado
- ✅ Tema claro e escuro
- ✅ Totalmente responsivo
- ✅ Validação completa
- ✅ Legibilidade perfeita

### Performance
- ⚡ Cálculo feito no template (zero overhead)
- ⚡ Campo nullable (não afeta ofertas antigas)
- ⚡ Consultas otimizadas
- ⚡ CSS minimalista

### Manutenibilidade
- 📖 Código limpo e documentado
- 📖 Migração reversível
- 📖 Testes compatíveis
- 📖 Fácil de estender

---

## 🎊 Status

**✅ IMPLEMENTADO COM SUCESSO!**

Todas as funcionalidades foram testadas e estão funcionando perfeitamente:
- Campo de preço antigo ✓
- Cálculo de desconto ✓
- Badge visual ✓
- Tema escuro legível ✓
- Migração aplicada ✓

---

**Desenvolvido com ❤️ para melhorar a experiência do usuário**

