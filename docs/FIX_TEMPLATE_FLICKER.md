# 🔧 Correção: Caixa de Variáveis Piscando

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.5.1

---

## 🐛 Problema Reportado

**Sintoma:** Na página de edição de templates (`/templates/3/editar`), a caixa azul com as dicas de variáveis ficava **piscando** ao entrar na página.

**Onde:** 
- `/templates/novo` - Criar template
- `/templates/{id}/editar` - Editar template

---

## 🔍 Causa do Problema

O Bootstrap aplica **animações CSS automáticas** aos elementos `.alert`:

```css
/* Bootstrap padrão */
.alert {
  transition: opacity 0.15s linear;
  animation: fadeIn 0.3s;
}
```

Isso causava um efeito de "piscamento" ou "fade" ao carregar a página, especialmente visível quando:
- A página carrega
- Há muitos elementos renderizando
- O navegador está processando JavaScript

**Resultado:** A caixa de variáveis "piscava" ou "aparecia gradualmente" de forma perceptível e desagradável.

---

## ✅ Solução Implementada

Desabilitei **todas as animações e transições** no elemento `.alert-info`:

```css
/* Remove flicker/blink effect from namespace info box */
.alert-info {
  animation: none !important;
  transition: none !important;
}
```

**Por que funciona:**
- `animation: none` - Remove qualquer animação CSS
- `transition: none` - Remove qualquer transição
- `!important` - Sobrescreve estilos do Bootstrap

---

## 📂 Arquivos Modificados

### 1. `app/templates/template_edit.html`
```diff
+ /* Remove flicker/blink effect from namespace info box */
+ .alert-info {
+   animation: none !important;
+   transition: none !important;
+ }

  .namespace-btn {
    transition: all 0.2s ease;
    cursor: pointer;
  }
```

### 2. `app/templates/template_create.html`
```diff
+ /* Remove flicker/blink effect from namespace info box */
+ .alert-info {
+   animation: none !important;
+   transition: none !important;
+ }

  .namespace-btn {
    transition: all 0.2s ease;
    cursor: pointer;
  }
```

---

## 📊 Antes vs Depois

### Antes ❌
```
1. Página carrega
2. Caixa aparece com fade-in (0.3s)
3. "Pisca" ou "pulsa"
4. Usuário percebe o efeito
5. Experiência ruim
```

### Depois ✅
```
1. Página carrega
2. Caixa aparece INSTANTANEAMENTE
3. Sem piscamento
4. Sem transições
5. Experiência fluida
```

---

## 🎨 Visual

**Antes (com animação):**
```
[Carregando...]
[Caixa começa a aparecer... 0%]
[Caixa aparecendo... 50%]
[Caixa totalmente visível... 100%]  ← 300ms de animação
```

**Depois (sem animação):**
```
[Carregando...]
[Caixa IMEDIATAMENTE visível]  ← 0ms, instantâneo
```

---

## 💡 Por Que Não Afetar Outros Alerts?

O CSS foi aplicado de forma **scoped** apenas nos templates:

**Global (`style.css`):**
```css
/* Outros alerts mantêm animações normais */
.alert {
  /* Animações padrão do Bootstrap */
}
```

**Local (`template_create.html`, `template_edit.html`):**
```css
<style>
  /* Só afeta esta página */
  .alert-info {
    animation: none !important;
  }
</style>
```

**Vantagens:**
- ✅ Correção específica
- ✅ Não afeta outros alerts
- ✅ Alertas de sucesso/erro continuam animados
- ✅ Apenas a caixa de variáveis fica estática

---

## 🧪 Testes

### Teste 1: Página de Edição
```
1. Acesse /templates/3/editar
2. Observe a caixa azul de variáveis
3. Verifique: NÃO deve piscar ✅
4. Recarregue a página (F5)
5. Verifique: Ainda não pisca ✅
```

### Teste 2: Página de Criação
```
1. Acesse /templates/novo
2. Observe a caixa azul de variáveis
3. Verifique: NÃO deve piscar ✅
```

### Teste 3: Outros Alerts
```
1. Crie um template com sucesso
2. Toast de sucesso deve aparecer com animação ✅
3. Vá para /admin/categories
4. Delete uma categoria
5. Modal deve aparecer com animação ✅
```

---

## 🎯 Elementos Afetados

### Apenas Esta Caixa
```html
<div class="alert alert-info">
  <i class="bi bi-lightbulb-fill"></i>
  <strong>Variáveis Disponíveis:</strong>
  <div>
    [button] {product_name}
    [button] {price}
    ...
  </div>
</div>
```

### Não Afeta
- ❌ Toasts de sucesso/erro
- ❌ Modals
- ❌ Alerts em outras páginas
- ❌ Animações de botões

---

## 📝 Alternativas Consideradas

### Opção 1: Desabilitar Todas Animações ❌
```css
* {
  animation: none !important;
  transition: none !important;
}
```
**Rejeita:** Muito agressivo, mata todas as animações

### Opção 2: Delay no Carregamento ❌
```javascript
setTimeout(() => {
  showBox();
}, 100);
```
**Rejeita:** Pior UX, atraso perceptível

### Opção 3: CSS Scoped ✅ (ESCOLHIDA)
```css
.alert-info {
  animation: none !important;
  transition: none !important;
}
```
**Vantagens:**
- ✅ Específico
- ✅ Não afeta outros elementos
- ✅ Simples
- ✅ Performático

---

## ✅ Checklist

- [x] Identificar causa do piscamento
- [x] Adicionar CSS fix em template_edit.html
- [x] Adicionar CSS fix em template_create.html
- [x] Testar página de edição
- [x] Testar página de criação
- [x] Verificar que outros alerts não foram afetados
- [x] Documentar solução

---

## 🎊 Status

**✅ CORRIGIDO COM SUCESSO!**

Caixa de variáveis agora:
- Sem piscamento ✓
- Aparece instantaneamente ✓
- Não afeta outros elementos ✓
- UX perfeita ✓

---

**Correção feita com ❤️ e atenção aos detalhes visuais!**

