# Sistema de Parcelamento em Ofertas

## 📋 Visão Geral

Sistema completo para cadastrar informações de parcelamento em ofertas, incluindo quantidade de parcelas, valor da parcela, e se é com ou sem juros.

## 🆕 Novos Campos

### Modelo `Offer`
```python
installment_count = db.Column(db.Integer, nullable=True)  # Quantidade de parcelas (ex: 5)
installment_value = db.Column(db.Numeric(10, 2), nullable=True)  # Valor da parcela (ex: 72.00)
installment_interest_free = db.Column(db.Boolean, default=True)  # Sem juros (True) ou com juros (False)
```

### Banco de Dados
```sql
ALTER TABLE offers ADD COLUMN installment_count INTEGER;
ALTER TABLE offers ADD COLUMN installment_value NUMERIC(10, 2);
ALTER TABLE offers ADD COLUMN installment_interest_free BOOLEAN DEFAULT 1;
```

## 📝 Namespaces Disponíveis

### Namespaces Individuais

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{installment_count}` | Quantidade de parcelas | `5` |
| `{installment_value}` | Valor da parcela | `72.00` |
| `{installment_interest_free}` | Com/sem juros | `sem juros` ou `com juros` |

### Namespace Formatado

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{installment_full}` | Texto completo formatado | `5x de R$ 72.00 sem juros` |
| `{parcelamento}` | Alias para installment_full | `5x de R$ 72.00 sem juros` |

## 🎨 Interface

### Formulário de Criação/Edição

Nova seção "Parcelamento (Opcional)" com três campos:

1. **Quantidade de Parcelas**
   - Campo numérico
   - Mínimo: 1, Máximo: 99
   - Placeholder: "Ex: 5"

2. **Valor da Parcela**
   - Campo decimal
   - Formato: 0.00
   - Placeholder: "Ex: 72.00"

3. **Sem Juros**
   - Switch (toggle)
   - Marcado por padrão
   - Ícone: percentual

## 💡 Exemplo de Uso

### No Cadastro de Oferta
```
Nome do produto: iPhone 15 Pro Max
Preço: 3599.00
Quantidade de Parcelas: 5
Valor da Parcela: 72.00
Sem Juros: ✓ (marcado)
```

### No Template
```
🔥 OFERTA IMPERDÍVEL!

{product_name} por apenas {price}!

Ou em {installment_full}

🛒 Garanta já: {offer_url}
```

### Resultado Final
```
🔥 OFERTA IMPERDÍVEL!

iPhone 15 Pro Max por apenas 3599.00!

Ou em 5x de R$ 72.00 sem juros

🛒 Garanta já: https://example.com/offer
```

## 🔧 Implementação Técnica

### Backend (Flask)

1. **Modelo** (`app/models.py`)
   - Adicionados 3 campos ao modelo `Offer`

2. **Formulário** (`app/forms.py`)
   - `IntegerField` para quantidade
   - `DecimalField` para valor
   - `BooleanField` para juros

3. **Rotas** (`app/routes/web.py`)
   - `create_offer`: Salva dados de parcelamento
   - `edit_offer`: Carrega e atualiza dados de parcelamento

### Frontend (Jinja2 + JavaScript)

1. **Templates HTML**
   - `offer_create.html`: Formulário de criação
   - `offer_edit.html`: Formulário de edição
   - Novos campos com ícones e tooltips

2. **JavaScript** (`offer_share.html`)
   - `offerData`: Inclui campos de parcelamento
   - `generateText()`: Substitui namespaces de parcelamento
   - Formatação automática do texto completo

### Banco de Dados

1. **Namespaces**
   ```sql
   INSERT INTO namespaces (name, label, description, scope)
   VALUES 
     ('installment_count', 'Quantidade de Parcelas', 'Número de parcelas', 'OFFER'),
     ('installment_value', 'Valor da Parcela', 'Valor de cada parcela', 'OFFER'),
     ('installment_interest_free', 'Com/Sem Juros', 'Se tem juros', 'OFFER'),
     ('installment_full', 'Parcelamento Completo', 'Texto formatado completo', 'OFFER');
   ```

## ✅ Validações

- Quantidade de parcelas: 1-99
- Valor da parcela: deve ser numérico positivo
- Todos os campos são opcionais
- Se não houver parcelamento, os namespaces são removidos do texto

## 🎯 Casos de Uso

### 1. Parcelamento Sem Juros
```
Entrada: 12x de 100.00, Sem Juros
Saída: "12x de R$ 100.00 sem juros"
```

### 2. Parcelamento Com Juros
```
Entrada: 6x de 150.00, Com Juros
Saída: "6x de R$ 150.00 com juros"
```

### 3. Sem Parcelamento
```
Entrada: (campos vazios)
Saída: Namespaces removidos do template
```

## 📁 Arquivos Modificados

```
app/
  models.py ✓
  forms.py ✓
  routes/
    web.py ✓
  templates/
    offer_create.html ✓
    offer_edit.html ✓
    offer_share.html ✓

scripts/
  add_installment_namespaces.sql ✓

docs/
  INSTALLMENT_FEATURE.md ✓ (este arquivo)
```

## 🚀 Como Testar

1. Acesse `/ofertas/nova`
2. Preencha os dados da oferta
3. Na seção "Parcelamento", preencha:
   - Quantidade: 5
   - Valor: 72.00
   - Sem juros: marcado
4. Salve a oferta
5. Acesse `/ofertas/{id}/compartilhar`
6. Selecione um template com `{installment_full}`
7. Verifique o texto gerado: "5x de R$ 72.00 sem juros"

## 🎨 Ícones Utilizados

- `bi-credit-card`: Seção de parcelamento
- `bi-123`: Quantidade de parcelas
- `bi-cash-coin`: Valor da parcela
- `bi-percent`: Com/sem juros

## 📊 Status

✅ **COMPLETO E FUNCIONAL**

- [x] Modelo atualizado
- [x] Formulário atualizado
- [x] Banco de dados atualizado
- [x] Namespaces criados
- [x] Templates HTML atualizados
- [x] JavaScript atualizado
- [x] Rotas atualizadas
- [x] Documentação criada

