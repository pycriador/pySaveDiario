# 📚 Documentação Técnica - pySaveDiário

Bem-vindo à documentação técnica completa do pySaveDiário! Este diretório contém guias detalhados sobre todas as funcionalidades do sistema.

---

## 📋 Índice Geral

### 🎯 Guias Principais

- **[FEATURES.md](FEATURES.md)** - Lista completa de funcionalidades do sistema
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Referência rápida de comandos e atalhos
- **[API_COMPLETE_INVENTORY.md](API_COMPLETE_INVENTORY.md)** - Inventário completo da API

### 🚀 Funcionalidades Principais

#### Ofertas
- **[INSTALLMENT_FEATURE.md](INSTALLMENT_FEATURE.md)** - Sistema de parcelas
- **[OLD_PRICE_FEATURE.md](OLD_PRICE_FEATURE.md)** - Preço antigo e cálculo de desconto
- **[SECURE_IMAGE_UPLOAD.md](SECURE_IMAGE_UPLOAD.md)** - Upload seguro de imagens (7 camadas)
- **[IMAGE_DISPLAY_FEATURE.md](IMAGE_DISPLAY_FEATURE.md)** - Exibição de imagens em ofertas
- **[DYNAMIC_FILTERS_FEATURE.md](DYNAMIC_FILTERS_FEATURE.md)** - Filtros dinâmicos em ofertas

#### Cupons
- **[COUPON_DISCOUNT_FEATURE.md](COUPON_DISCOUNT_FEATURE.md)** - Sistema de desconto (% ou fixo)
- **[MAX_DISCOUNT_LIMIT.md](MAX_DISCOUNT_LIMIT.md)** - Limite máximo de desconto
- **[COUPON_NAMESPACES.md](COUPON_NAMESPACES.md)** - Variáveis de cupons em templates

#### Vendedores
- **[SELLER_COLORS_FEATURE.md](SELLER_COLORS_FEATURE.md)** - Cores personalizadas para vendedores
- **[INACTIVE_SELLER_FILTER.md](INACTIVE_SELLER_FILTER.md)** - Filtro automático de vendedores inativos

#### Templates e Compartilhamento
- **[COMPARTILHAMENTO_SOCIAL.md](COMPARTILHAMENTO_SOCIAL.md)** - Sistema de compartilhamento social
- **[HTML_TO_TEXT_CONVERSION.md](HTML_TO_TEXT_CONVERSION.md)** - Conversão HTML para redes sociais
- **[TEMPLATE_SOCIAL_NETWORKS_INTEGRATION.md](TEMPLATE_SOCIAL_NETWORKS_INTEGRATION.md)** - Integração com redes
- **[ALL_COUPONS_NAMESPACE.md](ALL_COUPONS_NAMESPACE.md)** - Namespace `{all_coupons}`
- **[SOCIAL_NETWORK_PREFIX_SUFFIX_IMPLEMENTATION.md](SOCIAL_NETWORK_PREFIX_SUFFIX_IMPLEMENTATION.md)** - Prefixos e sufixos

#### Interface e UX
- **[HTML_EDITOR_FEATURE.md](HTML_EDITOR_FEATURE.md)** - Editor Quill.js
- **[COLOR_PICKER_FEATURE.md](COLOR_PICKER_FEATURE.md)** - Colorpicker visual
- **[TOAST_NOTIFICATIONS.md](TOAST_NOTIFICATIONS.md)** - Sistema de notificações
- **[CSS_REFACTORING_GUIDE.md](CSS_REFACTORING_GUIDE.md)** - Guia de refatoração CSS
- **[FILTERS_FEATURE.md](FILTERS_FEATURE.md)** - Filtros em Templates e Cupons

#### Sistema
- **[CURRENCY_SYMBOLS.md](CURRENCY_SYMBOLS.md)** - Símbolos de moedas
- **[SEPARATE_DATE_TIME_FIELDS.md](SEPARATE_DATE_TIME_FIELDS.md)** - Campos de data e hora separados
- **[ADMIN_MENU_REORGANIZATION.md](ADMIN_MENU_REORGANIZATION.md)** - Reorganização do menu admin

### 🔧 Correções e Troubleshooting

- **[FIX_COUPON_NAMESPACES_NOT_SHOWING.md](FIX_COUPON_NAMESPACES_NOT_SHOWING.md)** - Fix de namespaces
- **[FIX_ENUM_CASE_SENSITIVITY.md](FIX_ENUM_CASE_SENSITIVITY.md)** - Fix de case sensitivity
- **[FIX_JAVASCRIPT_SYNTAX_ERROR.md](FIX_JAVASCRIPT_SYNTAX_ERROR.md)** - Fix de erros JS
- **[FIX_JINJA2_SELECTATTR_ENUM.md](FIX_JINJA2_SELECTATTR_ENUM.md)** - Fix de Jinja2 selectattr
- **[FIX_TEMPLATE_FLICKER.md](FIX_TEMPLATE_FLICKER.md)** - Fix de piscamento em templates
- **[FIX_TEMPLATE_VARIABLE_REPLACEMENT.md](FIX_TEMPLATE_VARIABLE_REPLACEMENT.md)** - Fix de substituição

### 📖 Resumos e Guias

- **[RESUMO_FINAL_IMPLEMENTACOES.md](RESUMO_FINAL_IMPLEMENTACOES.md)** - Resumo geral
- **[GUIA_USO_REDES_SOCIAIS.md](GUIA_USO_REDES_SOCIAIS.md)** - Como usar redes sociais
- **[RESUMO_REDES_SOCIAIS_E_CUPONS.md](RESUMO_REDES_SOCIAIS_E_CUPONS.md)** - Integração redes + cupons

---

## 🎯 Por Funcionalidade

### Ofertas (Offers)
1. Criar, editar, deletar ofertas
2. Upload de imagens com validação
3. Sistema de parcelas
4. Preço antigo e desconto
5. Filtros dinâmicos
6. Compartilhamento social
7. Multi-moedas

**Docs Relacionadas:**
- `INSTALLMENT_FEATURE.md`
- `OLD_PRICE_FEATURE.md`
- `SECURE_IMAGE_UPLOAD.md`
- `IMAGE_DISPLAY_FEATURE.md`
- `DYNAMIC_FILTERS_FEATURE.md`

### Cupons (Coupons)
1. Desconto percentual ou fixo
2. Limite máximo de desconto
3. Data de expiração
4. Integração com ofertas
5. Namespaces em templates
6. Filtros avançados

**Docs Relacionadas:**
- `COUPON_DISCOUNT_FEATURE.md`
- `MAX_DISCOUNT_LIMIT.md`
- `COUPON_NAMESPACES.md`
- `ALL_COUPONS_NAMESPACE.md`
- `FILTERS_FEATURE.md`

### Vendedores (Sellers)
1. CRUD completo
2. Cores personalizadas
3. Colorpicker visual
4. Filtro de inativos
5. Páginas de edição

**Docs Relacionadas:**
- `SELLER_COLORS_FEATURE.md`
- `INACTIVE_SELLER_FILTER.md`
- `COLOR_PICKER_FEATURE.md`

### Templates
1. Editor HTML (Quill.js)
2. 50+ namespaces disponíveis
3. Configuração por rede social
4. Prefixos e sufixos
5. Conversão HTML → Texto
6. Filtros de busca

**Docs Relacionadas:**
- `HTML_EDITOR_FEATURE.md`
- `HTML_TO_TEXT_CONVERSION.md`
- `TEMPLATE_SOCIAL_NETWORKS_INTEGRATION.md`
- `SOCIAL_NETWORK_PREFIX_SUFFIX_IMPLEMENTATION.md`
- `FILTERS_FEATURE.md`

### Redes Sociais
1. Configuração de prefixo/sufixo
2. Colorpicker para botões
3. Ativar/desativar redes
4. Formatação específica por rede

**Docs Relacionadas:**
- `COMPARTILHAMENTO_SOCIAL.md`
- `SOCIAL_NETWORKS_AND_COUPONS_SHARE.md`
- `COLOR_PICKER_FEATURE.md`

### Interface
1. Tema claro e escuro
2. Toast notifications
3. CSS centralizado
4. Editor HTML
5. Colorpicker visual

**Docs Relacionadas:**
- `TOAST_NOTIFICATIONS.md`
- `CSS_REFACTORING_GUIDE.md`
- `HTML_EDITOR_FEATURE.md`
- `COLOR_PICKER_FEATURE.md`

---

## 🔍 Como Usar Esta Documentação

### Para Desenvolvedores

1. **Começando:** Leia `FEATURES.md` para visão geral
2. **Referência Rápida:** Use `QUICK_REFERENCE.md`
3. **API:** Consulte `API_COMPLETE_INVENTORY.md` ou acesse `/api-docs`
4. **Implementação:** Cada funcionalidade tem seu próprio `.md`

### Para Implementar uma Feature

1. Leia a documentação específica da feature
2. Veja exemplos de código
3. Execute os scripts de migração (se houver)
4. Teste a funcionalidade

### Para Troubleshooting

1. Verifique os arquivos `FIX_*.md`
2. Consulte `RESUMO_FINAL_IMPLEMENTACOES.md`
3. Veja logs de erro
4. Revise a documentação da feature específica

---

## 📦 Arquivos por Categoria

### 🎨 Interface e Design
- `HTML_EDITOR_FEATURE.md`
- `COLOR_PICKER_FEATURE.md`
- `TOAST_NOTIFICATIONS.md`
- `CSS_REFACTORING_GUIDE.md`

### 🏷️ Ofertas e Produtos
- `INSTALLMENT_FEATURE.md`
- `OLD_PRICE_FEATURE.md`
- `SECURE_IMAGE_UPLOAD.md`
- `IMAGE_DISPLAY_FEATURE.md`
- `DYNAMIC_FILTERS_FEATURE.md`

### 🎫 Cupons
- `COUPON_DISCOUNT_FEATURE.md`
- `MAX_DISCOUNT_LIMIT.md`
- `COUPON_NAMESPACES.md`
- `ALL_COUPONS_NAMESPACE.md`

### 🏪 Vendedores
- `SELLER_COLORS_FEATURE.md`
- `INACTIVE_SELLER_FILTER.md`

### 📱 Redes Sociais
- `COMPARTILHAMENTO_SOCIAL.md`
- `HTML_TO_TEXT_CONVERSION.md`
- `TEMPLATE_SOCIAL_NETWORKS_INTEGRATION.md`
- `SOCIAL_NETWORK_PREFIX_SUFFIX_IMPLEMENTATION.md`
- `SOCIAL_NETWORKS_AND_COUPONS_SHARE.md`

### ⚙️ Sistema
- `CURRENCY_SYMBOLS.md`
- `SEPARATE_DATE_TIME_FIELDS.md`
- `ADMIN_MENU_REORGANIZATION.md`
- `FILTERS_FEATURE.md`

### 🔧 Correções
- `FIX_COUPON_NAMESPACES_NOT_SHOWING.md`
- `FIX_ENUM_CASE_SENSITIVITY.md`
- `FIX_JAVASCRIPT_SYNTAX_ERROR.md`
- `FIX_JINJA2_SELECTATTR_ENUM.md`
- `FIX_SHARE_BUTTONS_OFERTAS.md`
- `FIX_TEMPLATE_FLICKER.md`
- `FIX_TEMPLATE_VARIABLE_REPLACEMENT.md`

---

## 🚀 Início Rápido

### Leitura Essencial (5 minutos)

1. `FEATURES.md` - Visão geral do sistema
2. `QUICK_REFERENCE.md` - Comandos principais
3. `GUIA_USO_REDES_SOCIAIS.md` - Como usar redes sociais

### Leitura Técnica (15 minutos)

1. `API_COMPLETE_INVENTORY.md` - Todos os endpoints
2. `SECURE_IMAGE_UPLOAD.md` - Sistema de upload
3. `SELLER_COLORS_FEATURE.md` - Cores de vendedores
4. `FILTERS_FEATURE.md` - Sistema de filtros

### Implementação (30 minutos)

1. Leia a doc específica da feature que quer implementar
2. Execute os scripts de migração listados
3. Teste a funcionalidade
4. Veja os exemplos de código

---

## 📝 Convenções

### Nomenclatura

- **FEATURE** - Documentação de funcionalidade
- **FIX** - Documentação de correção/bugfix
- **RESUMO** - Resumo de múltiplas implementações
- **GUIA** - Guia de uso prático

### Estrutura dos Docs

Cada documentação segue este padrão:

```markdown
# Título da Feature

## 📋 Visão Geral
Descrição breve

## 🎯 Funcionalidades
Lista de funcionalidades

## 🔧 Implementação Técnica
Código e exemplos

## 📝 Como Usar
Instruções práticas

## 📚 Referências
Arquivos relacionados
```

---

## 🔄 Última Atualização

**Data:** 04/12/2025  
**Versão:** 2.0  
**Total de Documentos:** 45+

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Consulte esta documentação
2. Veja os arquivos `FIX_*.md` para problemas conhecidos
3. Acesse `/api-docs` para documentação interativa
4. Abra uma issue no GitHub

---

**Documentação mantida e atualizada pela equipe pySaveDiário**
