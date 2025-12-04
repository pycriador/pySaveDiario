# 📦 Result Data - Dados Coletados

Esta pasta contém os **arquivos CSV e JSON** gerados pelo scraper do MercadoLivre.

## 📁 Estrutura dos Arquivos

Os arquivos seguem o padrão de nomenclatura:

```
ml_{vendedor}_{timestamp}.json
ml_{vendedor}_{timestamp}.csv
```

**Exemplo:**
```
ml_videogstore_20251119_203045.json
ml_videogstore_20251119_203045.csv
```

### Campos:
- `{vendedor}` - Nickname do vendedor no MercadoLivre
- `{timestamp}` - Data e hora da coleta no formato YYYYMMDD_HHMMSS

## 📊 Formato dos Dados

### JSON
Arquivo estruturado com array de produtos:

```json
[
  {
    "id": "MLB1234567890",
    "title": "Nome do Produto",
    "price": 99.90,
    "currency_id": "BRL",
    "link": "https://produto.mercadolivre.com.br/...",
    "image": "https://http2.mlstatic.com/...",
    "condition": "new",
    "free_shipping": true,
    "collected_date": "2025-11-19 20:30:45"
  }
]
```

### CSV
Arquivo tabular compatível com Excel/Google Sheets:

```csv
id,title,price,currency_id,link,image,condition,free_shipping,collected_date
MLB123...,Produto,99.90,BRL,https://...,https://...,new,true,2025-11-19 20:30:45
```

## 🔒 Segurança

Esta pasta está no `.gitignore` e **NÃO será** commitada ao Git, protegendo seus dados de coleta.

## 🗂️ Organização

Recomendações:
- ✅ Mantenha backups dos dados importantes
- ✅ Delete arquivos antigos periodicamente
- ✅ Use nomes descritivos ao salvar manualmente

## 📝 Como os Arquivos São Gerados

Ao executar o scraper:

```bash
python3 scripts/mercadolivre_selenium_scraper.py
```

E escolher o formato de exportação:

```
💾 Escolha o formato de exportação:
1. JSON
2. CSV
3. Ambos
```

Os arquivos serão salvos automaticamente nesta pasta (`result_data/`).

## 📍 Localização

```
/Users/willian.jesus/Downloads/pySaveDiario/result_data/
```

## 🧹 Limpeza

Para limpar arquivos antigos:

```bash
# Listar arquivos
ls -lh result_data/

# Deletar todos os arquivos (CUIDADO!)
rm result_data/ml_*.json
rm result_data/ml_*.csv

# Deletar arquivos de um vendedor específico
rm result_data/ml_videogstore_*.json
rm result_data/ml_videogstore_*.csv

# Deletar arquivos mais antigos que 30 dias
find result_data/ -name "ml_*.json" -mtime +30 -delete
find result_data/ -name "ml_*.csv" -mtime +30 -delete
```

## 📈 Análise dos Dados

### Python (Pandas)

```python
import pandas as pd
import json

# Carregar JSON
with open('result_data/ml_videogstore_20251119.json') as f:
    data = json.load(f)
    df = pd.DataFrame(data)

# Ou carregar CSV diretamente
df = pd.read_csv('result_data/ml_videogstore_20251119.csv')

# Análises
print(f"Total de produtos: {len(df)}")
print(f"Preço médio: R$ {df['price'].mean():.2f}")
print(f"Preço mínimo: R$ {df['price'].min():.2f}")
print(f"Preço máximo: R$ {df['price'].max():.2f}")
print(f"Com frete grátis: {df['free_shipping'].sum()}")
```

### Excel/Google Sheets

1. Abra o arquivo `.csv`
2. Colunas serão automaticamente separadas
3. Use fórmulas do Excel normalmente:
   - `=MÉDIA(C:C)` - Preço médio
   - `=MIN(C:C)` - Preço mínimo
   - `=MAX(C:C)` - Preço máximo
   - `=CONT.SE(H:H;"TRUE")` - Contar frete grátis

## 💡 Dicas

1. **Backup Regular**: Copie arquivos importantes para outro local
2. **Nomeclatura**: Se renomear, mantenha o formato `ml_vendedor_data`
3. **Comparação**: Compare arquivos de datas diferentes para ver mudanças
4. **Automação**: Use scripts Python para análises automáticas

## 🎯 Status

- 📁 Pasta criada automaticamente pelo script
- 🔒 Ignorada pelo Git (.gitignore)
- ✅ Pronta para receber dados
- 📊 Compatível com análises e ferramentas

---

**Última atualização:** 19/11/2025  
**Gerado por:** MercadoLivre Selenium Scraper v2.1

