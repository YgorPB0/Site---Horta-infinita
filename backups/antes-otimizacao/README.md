# 🌱 Horta Infinita — Página de Vendas de Alta Conversão

Página de vendas moderna, responsiva, persuasiva e com identidade visual premium desenvolvida para o produto digital **Horta Infinita**.

---

## 📁 Estrutura de Arquivos

```
Site de Horta/
├── index.html        # Estrutura HTML5 semântica com todas as 24 seções
├── styles.css        # Folha de estilos completa com a paleta de cores estrita
├── script.js         # Lógica de checkout, popup de R$ 12,90, FAQ e barra mobile
└── README.md         # Manual rápido de personalização
```

---

## 🎨 Paleta de Cores Implementada

- **Verde Escuro Natural:** `#1F4D36`
- **Verde Médio:** `#4D7C52`
- **Verde Claro / Menta Suave:** `#DCEBD7`
- **Creme / Fundo Acolhedor:** `#F7F4EA`
- **Branco:** `#FFFFFF`
- **Marrom Suave / Terra:** `#92745B`
- **Verde Vibrante de Conversão (Botões):** `#2F8F46`

---

## ⚙️ Como Configurar Seus Links de Checkout

Abra o arquivo `script.js` e localize o bloco inicial:

```javascript
const CHECKOUT_URLS = {
  // Oferta Inicial (R$ 7,90)
  essencial: "https://pay.kiwify.com.br/SEU_LINK_790",

  // Oferta Intermediária / Popup Plus (R$ 12,90)
  plus: "https://pay.kiwify.com.br/SEU_LINK_1290",

  // Oferta Completa / Melhor Custo-Benefício (R$ 17,99)
  completo: "https://pay.kiwify.com.br/SEU_LINK_1799"
};
```

Basta substituir as URLs de exemplo pelas URLs reais da sua plataforma de vendas (**Kiwify, Hotmart, Eduzz, Kirvano, Monetizze**, etc.).

---

## 🛒 Fluxo Psicológico de Conversão

1. **Oferta Inicial (R$ 7,90):** Posicionada como um ponto de entrada de fricção quase nula.
2. **Popup Elegante (R$ 12,90):** Ao clicar no botão de R$ 7,90, um modal elegante convida o usuário a levar a versão *Plus* por apenas R$ 5 adicionais, com opção clara e suave de continuar com os R$ 7,90.
3. **Oferta Completa (R$ 17,99):** Destacada visualmente como o **Melhor Custo-Benefício** logo abaixo, com a lista completa dos 21 itens e bônus inclusos, gerando o pensamento: *"Por R$ 17,99 faz muito mais sentido levar o pacote completo."*

---

## 💬 Como Adicionar Provas Sociais e Depoimentos Reais

Na seção `#depoimentos` do arquivo `index.html`, você encontrará 6 cards estruturados com marcações administrativas:

```html
<div class="card-testimonial-slot">
  <strong>[Nome do Aluno(a)]</strong>
  <p>"[INSERIR DEPOIMENTO REAL]"</p>
  <span>📷 [INSERIR FOTO REAL DA HORTA OU PRINT AUTORIZADO]</span>
</div>
```

Conforme seus alunos enviarem mensagens no WhatsApp ou fotos das suas colheitas, basta substituir esses textos e imagens preservando a transparência e credibilidade.

---

## 📱 Visualização e Testes

Para testar o site localmente, basta dar um duplo clique no arquivo `index.html` em qualquer navegador (Chrome, Edge, Firefox, Safari) ou abrir com a extensão *Live Server* do VS Code.
