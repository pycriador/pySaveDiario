# 📝 Editor HTML Embutido - Quill.js

## 📋 Visão Geral

Sistema completo de editor HTML rico integrado aos campos de descrição de ofertas e corpo de templates, com suporte total aos temas escuro e claro.

---

## ✅ Onde o Editor Está Disponível

### 1. **Ofertas** (`/ofertas/nova` e `/ofertas/{id}/editar`)
- Campo: **Descrição do produto**
- Permite formatação rica do texto
- Suporta HTML

### 2. **Templates** (`/templates/novo` e `/templates/{id}/editar`)
- Campo: **Corpo do Template**
- Permite formatação rica + namespaces
- Inserção de variáveis funciona no editor

---

## 🎨 Recursos do Editor

### Toolbar Completa

```
┌──────────────────────────────────────────────┐
│ H1 ▼ | B I U S | ● ● | 🔗 | 🧹            │  ← Toolbar
├──────────────────────────────────────────────┤
│                                              │
│  Digite aqui com formatação HTML...         │  ← Área de edição
│                                              │
│                                              │
└──────────────────────────────────────────────┘
```

### Ferramentas Disponíveis

| Ícone | Ferramenta | Atalho | Função |
|-------|------------|--------|--------|
| **H1 ▼** | Cabeçalhos | - | H1, H2, H3, Parágrafo |
| **B** | Negrito | Ctrl/Cmd+B | Texto em negrito |
| **I** | Itálico | Ctrl/Cmd+I | Texto em itálico |
| **U** | Sublinhado | Ctrl/Cmd+U | Texto sublinhado |
| **S** | Riscado | - | Texto ~~riscado~~ |
| **● ●** | Listas | - | Ordenada e não-ordenada |
| **●** | Cor do texto | - | Cores predefinidas |
| **●** | Cor de fundo | - | Destacar texto |
| **🔗** | Link | - | Inserir link |
| **🧹** | Limpar | - | Remove formatação |

---

## 🎨 Exemplo de Formatação

### Input no Editor

```
Produto INCRÍVEL!

Características:
• Alta qualidade
• Melhor preço
• Entrega rápida

Compre AGORA!
```

### HTML Gerado

```html
<h2>Produto INCRÍVEL!</h2>

<p><strong>Características:</strong></p>
<ul>
  <li>Alta qualidade</li>
  <li>Melhor preço</li>
  <li>Entrega rápida</li>
</ul>

<p><strong>Compre AGORA!</strong></p>
```

---

## 🌓 Tema Escuro e Claro

### Tema Claro

```
┌──────────────────────────────────┐
│ [Toolbar fundo branco]           │  ← Fundo #ffffff
├──────────────────────────────────┤
│ Texto preto em fundo branco      │  ← #212529 em #ffffff
└──────────────────────────────────┘
```

**Cores:**
- Toolbar: Fundo branco
- Editor: Fundo branco
- Texto: Preto (#212529)
- Ícones: Cinza escuro
- Hover: Azul primário

---

### Tema Escuro

```
┌──────────────────────────────────┐
│ [Toolbar fundo escuro]           │  ← Fundo rgba(255,255,255,0.05)
├──────────────────────────────────┤
│ Texto branco em fundo escuro     │  ← #e5e5e5 em #1a1a1a
└──────────────────────────────────┘
```

**Cores:**
- Toolbar: Fundo semi-transparente
- Editor: Fundo #1a1a1a
- Texto: Branco (#e5e5e5)
- Ícones: Cinza claro
- Hover: Azul claro (#60a5fa)

---

## 💻 Implementação Técnica

### Componente Reutilizável

```html
<!-- app/templates/components/html_editor.html -->

<!-- Quill.js CSS -->
<link href="https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css" rel="stylesheet">

<!-- Custom styling for themes -->
<style>
  .ql-toolbar { /* Toolbar styling */ }
  .ql-container { /* Editor container */ }
  .ql-editor { /* Content area */ }
  
  body[data-theme="dark"] .ql-toolbar { /* Dark theme */ }
  body[data-theme="dark"] .ql-editor { /* Dark theme */ }
</style>

<!-- Quill.js JavaScript -->
<script src="https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js"></script>

<script>
  function initEditor(fieldId, initialContent, placeholder) {
    // Auto-initialize on textareas with class 'html-editor'
  }
</script>
```

---

### Uso nos Templates

```html
<!-- 1. Adicionar classe 'html-editor' ao textarea -->
{{ form.product_description(class="form-control html-editor", 
                            id="product_description",
                            placeholder="Descrição com formatação...") }}

<!-- 2. Incluir componente -->
{% include 'components/html_editor.html' %}

<!-- 3. Editor inicializa automaticamente! -->
```

---

### JavaScript - Auto-inicialização

```javascript
document.addEventListener('DOMContentLoaded', function() {
  // Auto-detect textareas with class 'html-editor'
  document.querySelectorAll('textarea.html-editor').forEach(textarea => {
    const fieldId = textarea.id;
    const initialContent = textarea.value || '';
    const placeholder = textarea.getAttribute('placeholder') || 'Digite aqui...';
    
    editors[fieldId] = initEditor(fieldId, initialContent, placeholder);
  });
});
```

**Benefício:** Adicione apenas a classe `html-editor` e pronto!

---

## 🔧 Sincronização com Formulário

### Sincronização Automática

```javascript
// Sync Quill content to textarea on change
quill.on('text-change', function() {
  textarea.value = quill.root.innerHTML;
});

// Also sync on form submit
form.addEventListener('submit', function() {
  textarea.value = quill.root.innerHTML;
});
```

**Garantia:** O HTML é sempre salvo no banco de dados corretamente!

---

## 🎯 Integração com Namespaces

### Templates com Variáveis

**Problema:** Inserir `{product_name}` no editor Quill

**Solução:**
```javascript
function insertNamespace(namespaceName) {
  const editorId = 'templateBody';
  
  // Check if Quill editor exists
  if (editors && editors[editorId]) {
    const quill = editors[editorId];
    const range = quill.getSelection(true);
    const namespaceText = `{${namespaceName}}`;
    
    // Insert at cursor position
    quill.insertText(range.index, namespaceText);
    quill.setSelection(range.index + namespaceText.length);
  }
}
```

**Resultado:** Variáveis funcionam perfeitamente no editor HTML!

---

## 📊 Configuração do Editor

### Toolbar Modules

```javascript
modules: {
  toolbar: [
    [{ 'header': [1, 2, 3, false] }],        // H1, H2, H3
    ['bold', 'italic', 'underline', 'strike'], // Formatação
    [{ 'list': 'ordered'}, { 'list': 'bullet' }], // Listas
    [{ 'color': [] }, { 'background': [] }],  // Cores
    ['link'],                                 // Links
    ['clean']                                 // Limpar formatação
  ]
}
```

**Minimalista e funcional!**

---

## 🎨 CSS Customizado

### Light Theme

```css
.ql-toolbar.ql-snow {
  border: 1px solid var(--border-color);
  background: var(--panel-solid);
  border-radius: 8px 8px 0 0;
}

.ql-container.ql-snow {
  background: var(--bg-secondary);
  border-radius: 0 0 8px 8px;
}

.ql-editor {
  min-height: 150px;
  max-height: 400px;
  color: var(--text-primary);
}
```

---

### Dark Theme

```css
body[data-theme="dark"] .ql-toolbar.ql-snow {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

body[data-theme="dark"] .ql-container.ql-snow {
  background: #1a1a1a;
  border-color: rgba(255, 255, 255, 0.1);
}

body[data-theme="dark"] .ql-editor {
  color: #e5e5e5;
}

body[data-theme="dark"] .ql-toolbar .ql-stroke {
  stroke: #e5e5e5;
}
```

---

## ✅ Recursos Implementados

### Visual
- [x] Toolbar com bordas arredondadas
- [x] Editor com altura mínima (150px)
- [x] Altura máxima com scroll (400px)
- [x] Bordas suaves
- [x] Sombras sutis
- [x] Scrollbar customizado

### Funcionalidade
- [x] Auto-inicialização
- [x] Sincronização automática com textarea
- [x] Suporte a HTML completo
- [x] Inserção de namespaces
- [x] Placeholder personalizado
- [x] Conteúdo inicial carregado

### Temas
- [x] Tema claro completo
- [x] Tema escuro completo
- [x] Transição suave entre temas
- [x] Ícones adaptáveis
- [x] Cores consistentes

---

## 🧪 Como Testar

### 1. Testar em Ofertas

```bash
# Acesse
http://localhost:5000/ofertas/nova

# No campo "Descrição do produto":
1. Veja o editor HTML aparecer
2. Digite texto
3. Clique em "B" para negrito
4. Clique em "•" para lista
5. Salve a oferta
6. Edite a oferta
7. Veja conteúdo HTML carregado
```

---

### 2. Testar em Templates

```bash
# Acesse
http://localhost:5000/templates/novo

# No campo "Corpo do Template":
1. Veja o editor HTML aparecer
2. Digite: "Oferta de {product_name}"
3. Selecione "Oferta de" e deixe negrito
4. Clique em uma variável para inserir
5. Veja variável inserida no editor
6. Salve o template
```

---

### 3. Testar Mudança de Tema

```bash
# Com editor aberto:
1. Alterne entre tema claro/escuro
2. Veja cores do editor mudarem
3. Ícones devem ser visíveis
4. Texto deve ser legível
5. Hover deve funcionar
```

---

## 📁 Estrutura de Arquivos

```
app/templates/
├── components/
│   └── html_editor.html           ✅ Componente reutilizável
├── offer_create.html              ✅ Inclui editor
├── offer_edit.html                ✅ Inclui editor
├── template_create.html           ✅ Inclui editor + namespace integration
└── template_edit.html             ✅ Inclui editor + namespace integration

docs/
└── HTML_EDITOR_FEATURE.md         ✅ Esta documentação
```

---

## 🎯 Benefícios

### Para o Usuário
- ✅ Interface WYSIWYG intuitiva
- ✅ Formatação visual rica
- ✅ Não precisa saber HTML
- ✅ Toolbar com ícones claros
- ✅ Preview em tempo real
- ✅ Funciona no tema escuro

### Para Desenvolvedores
- ✅ Componente reutilizável
- ✅ Fácil de adicionar a novos campos
- ✅ Auto-inicialização
- ✅ Sincronização automática
- ✅ Código limpo e organizado
- ✅ CDN (sem instalação local)

---

## 🚀 Como Adicionar em Novos Campos

### Passo 1: Adicionar Classe ao Textarea

```html
{{ form.meu_campo(class="form-control html-editor", 
                  id="meu_campo",
                  placeholder="Digite aqui...") }}
```

### Passo 2: Incluir Componente

```html
{% block scripts %}
{% include 'components/html_editor.html' %}
{% endblock %}
```

### Passo 3: Pronto!

**O editor inicializa automaticamente!**

---

## 📊 Comparação: Antes vs Agora

### ❌ Antes (Textarea simples)

```
┌──────────────────────────────────┐
│ Texto sem formatação             │
│ Tudo em uma linha                │
│ Sem negrito, sem listas          │
└──────────────────────────────────┘
```

### ✅ Agora (Editor HTML)

```
┌──────────────────────────────────┐
│ H1 ▼ | B I U S | ● ● | 🔗 | 🧹  │  ← Toolbar
├──────────────────────────────────┤
│ Texto com formatação             │
│ • Listas                         │
│ Links clicáveis                  │
│ Cores e destaques               │
└──────────────────────────────────┘
```

---

## 🎨 Visual no Tema Escuro

```
┌────────────────────────────────────┐
│ [Toolbar com fundo escuro]         │
│ Ícones em branco/cinza claro       │
├────────────────────────────────────┤
│ [Editor com fundo #1a1a1a]         │
│ Texto branco (#e5e5e5)             │
│ Placeholder cinza médio (#6b7280)  │
└────────────────────────────────────┘
```

**Totalmente legível e profissional!**

---

## 🔧 Tecnologia

### Quill.js v2.0.2

**Por que Quill?**
- ✅ Leve e rápido (~40KB minified)
- ✅ API simples e poderosa
- ✅ Excelente suporte a temas
- ✅ Bem documentado
- ✅ Muito usado (40k+ stars no GitHub)
- ✅ Mantido ativamente
- ✅ Sem dependências pesadas

**Alternativas descartadas:**
- ❌ TinyMCE: Muito pesado
- ❌ CKEditor: Complexo demais
- ❌ Summernote: Bootstrap 4 only

---

## 💾 Salvamento de Dados

### Fluxo

```
Usuário edita no Quill
         ↓
quill.on('text-change')
         ↓
textarea.value = quill.root.innerHTML
         ↓
form.submit()
         ↓
Backend recebe HTML
         ↓
Salva no banco de dados
         ↓
Próxima edição
         ↓
HTML carrega no editor
```

**Sincronização perfeita!**

---

## 🎯 Casos de Uso

### 1. Descrição Rica de Produto

```html
<h3>iPhone 15 Pro Max</h3>

<p><strong>Características principais:</strong></p>
<ul>
  <li>Tela de 6.7"</li>
  <li>Câmera de 48MP</li>
  <li>Chip A17 Pro</li>
</ul>

<p><em>Disponível em 4 cores!</em></p>
```

---

### 2. Template de Promoção

```html
<h2>🔥 PROMOÇÃO RELÂMPAGO!</h2>

<p><strong>{product_name}</strong> com <strong>desconto IMPERDÍVEL!</strong></p>

<p>De <s>R$ {old_price}</s> por apenas <span style="color: red;">R$ {price}</span></p>

<ul>
  <li>Frete GRÁTIS</li>
  <li>Parcele em {installment_full}</li>
</ul>

<p><a href="{offer_url}">🛒 Compre AGORA!</a></p>
```

---

## 📱 Responsividade

### Desktop
- Editor ocupa largura total
- Toolbar completa visível
- Altura ajustável (150px-400px)

### Mobile
- Toolbar responsiva
- Botões mantêm tamanho adequado
- Touch-friendly
- Scroll vertical funciona

---

## ✅ Checklist de Funcionalidades

### Editor
- [x] Formatação de texto (B, I, U, S)
- [x] Cabeçalhos (H1, H2, H3)
- [x] Listas ordenadas e não-ordenadas
- [x] Cores de texto e fundo
- [x] Links
- [x] Limpar formatação
- [x] Altura min/max configurada
- [x] Scrollbar customizado

### Temas
- [x] Tema claro completo
- [x] Tema escuro completo
- [x] Ícones visíveis em ambos
- [x] Texto legível em ambos
- [x] Hover effects adequados
- [x] Transição suave

### Integração
- [x] Auto-inicialização
- [x] Sincronização com textarea
- [x] Salva HTML corretamente
- [x] Carrega conteúdo inicial
- [x] Funciona com namespaces (templates)
- [x] Componente reutilizável

### Páginas Implementadas
- [x] `/ofertas/nova` - Descrição do produto
- [x] `/ofertas/{id}/editar` - Descrição do produto
- [x] `/templates/novo` - Corpo do template
- [x] `/templates/{id}/editar` - Corpo do template

---

## 🎨 Scrollbar Customizado

### Tema Claro

```css
.ql-editor::-webkit-scrollbar {
  width: 8px;
}

.ql-editor::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.ql-editor::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}
```

### Tema Escuro

```css
body[data-theme="dark"] .ql-editor::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
}

body[data-theme="dark"] .ql-editor::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
```

---

## 📚 Documentação Quill.js

### Links Úteis

- **Website oficial:** https://quilljs.com/
- **Documentação:** https://quilljs.com/docs/
- **API Reference:** https://quilljs.com/docs/api/
- **GitHub:** https://github.com/quilljs/quill
- **CDN:** jsDelivr (usado no projeto)

---

## 🆘 Troubleshooting

### Problema: Editor não aparece

**Solução:**
1. Verifique se o textarea tem classe `html-editor`
2. Verifique se o componente foi incluído
3. Verifique console do navegador
4. Verifique se CDN está acessível

---

### Problema: Conteúdo não salva

**Solução:**
- A sincronização é automática
- Verifique se textarea tem ID único
- Cheque se formulário está sendo submetido corretamente

---

### Problema: Tema não muda

**Solução:**
- Verifique se body tem `data-theme="dark"`
- CSS usa CSS variables do sistema
- Hard refresh (Ctrl+Shift+R)

---

## 💡 Dicas de Uso

### 1. Formatação Básica

```
Selecione texto → Clique em "B" → Negrito
Selecione texto → Clique em "I" → Itálico
Selecione texto → Clique em "U" → Sublinhado
```

### 2. Criar Lista

```
1. Clique em "●" (lista não-ordenada)
2. Digite item
3. Enter para novo item
4. Enter duas vezes para sair
```

### 3. Adicionar Link

```
1. Selecione texto
2. Clique no ícone de link (🔗)
3. Digite URL
4. Enter
```

### 4. Mudar Cor

```
1. Selecione texto
2. Clique no ícone de cor (●)
3. Escolha cor da paleta
4. Texto muda de cor
```

---

## 🎉 Conclusão

Editor HTML embutido completo implementado com:

- ✅ **Quill.js integrado** (leve e moderno)
- ✅ **4 páginas com editor** (ofertas + templates)
- ✅ **Tema escuro/claro** (100% compatível)
- ✅ **Auto-inicialização** (apenas adicione classe)
- ✅ **Sincronização automática** (salva HTML)
- ✅ **Toolbar completa** (7 ferramentas)
- ✅ **Namespaces funcionam** (templates)
- ✅ **Componente reutilizável** (DRY)
- ✅ **Scrollbar customizado** (ambos temas)
- ✅ **Totalmente responsivo** (mobile-friendly)

**Status:** 🟢 **COMPLETO E PRONTO PARA USO**

---

**Última atualização:** 04/12/2025

