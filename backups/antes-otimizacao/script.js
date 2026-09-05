/**
 * HORTA INFINITA — SCRIPTS DE INTERAÇÃO, CARROSSEL & CONVERSÃO
 * 
 * Configurações fáceis para o produtor:
 * Insira os links das suas plataformas de pagamento favoritas
 * (Kiwify, Hotmart, Eduzz, Kirvano, Monetizze, etc.) no objeto CHECKOUT_URLS abaixo.
 */

// ==========================================================================
// 1. CONFIGURAÇÃO DE LINKS DE CHECKOUT
// ==========================================================================
const CHECKOUT_URLS = {
  // Oferta Inicial (R$ 7,90)
  essencial: "https://pay.exemplo.com/horta-infinita-essencial-790",

  // Oferta Intermediária / Popup Plus (R$ 12,90)
  plus: "https://pay.exemplo.com/horta-infinita-plus-1290",

  // Oferta Completa / Melhor Custo-Benefício (R$ 17,99)
  completo: "https://pay.exemplo.com/horta-infinita-completo-1799"
};

// ==========================================================================
// 2. INICIALIZAÇÃO APÓS O CARREGAMENTO DO DOM
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  initCheckoutLinks();
  initOfferModal();
  initFaqAccordion();
  initTestimonialsCarousel();
  initLegalModalLinks();
});

// ==========================================================================
// 3. GERENCIAMENTO DE LINKS DE CHECKOUT
// ==========================================================================
function initCheckoutLinks() {
  const checkoutElements = document.querySelectorAll(".checkout-link");
  
  checkoutElements.forEach((el) => {
    el.addEventListener("click", (e) => {
      const tier = el.getAttribute("data-tier");
      if (tier && CHECKOUT_URLS[tier]) {
        if (CHECKOUT_URLS[tier].includes("exemplo.com")) {
          console.info(`[Horta Infinita] Link configurado para o plano "${tier}": ${CHECKOUT_URLS[tier]}`);
        }
        el.href = CHECKOUT_URLS[tier];
      }
    });
  });
}

// ==========================================================================
// 4. MODAL POPUP DE UPSELL (R$ 12,90)
// ==========================================================================
function initOfferModal() {
  const modal = document.getElementById("upgradeModal");
  const closeBtn = document.getElementById("modalCloseBtn");
  const openButtons = document.querySelectorAll(".open-offer-modal");

  if (!modal) return;

  let lastFocusedElement = null;

  function openModal() {
    lastFocusedElement = document.activeElement;
    modal.classList.add("active");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden"; // Evita rolagem de fundo
    if (closeBtn) {
      setTimeout(() => closeBtn.focus(), 50);
    }
  }

  function closeModal() {
    modal.classList.remove("active");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
      lastFocusedElement.focus();
    }
  }

  openButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      openModal();
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      closeModal();
    }
  });
}

// ==========================================================================
// 5. ACCORDION DE DÚVIDAS FREQUENTES (FAQ)
// ==========================================================================
function initFaqAccordion() {
  const faqTriggers = document.querySelectorAll(".faq-trigger");

  faqTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const isExpanded = trigger.getAttribute("aria-expanded") === "true";
      const content = trigger.nextElementSibling;
      const parentItem = trigger.closest(".faq-item");

      faqTriggers.forEach((otherTrigger) => {
        if (otherTrigger !== trigger) {
          otherTrigger.setAttribute("aria-expanded", "false");
          const otherItem = otherTrigger.closest(".faq-item");
          if (otherItem) otherItem.classList.remove("active");
          const otherContent = otherTrigger.nextElementSibling;
          if (otherContent) {
            otherContent.style.maxHeight = null;
            otherContent.classList.remove("open");
          }
        }
      });

      if (isExpanded) {
        trigger.setAttribute("aria-expanded", "false");
        if (parentItem) parentItem.classList.remove("active");
        content.style.maxHeight = null;
        content.classList.remove("open");
      } else {
        trigger.setAttribute("aria-expanded", "true");
        if (parentItem) parentItem.classList.add("active");
        content.classList.add("open");
        content.style.maxHeight = content.scrollHeight + 30 + "px";
      }
    });
  });
}



// ==========================================================================
// 7. CARROSSEL DE DEPOIMENTOS DE WHATSAPP COM FOTOS REAIS
// ==========================================================================
function initTestimonialsCarousel() {
  const track = document.getElementById("carouselTrack");
  const slides = document.querySelectorAll(".carousel-slide");
  const dots = document.querySelectorAll(".carousel-dot");
  const carouselContainer = document.getElementById("testimonialsCarousel");

  if (!track || slides.length === 0) return;

  let currentIndex = 0;
  const totalSlides = slides.length;
  let autoplayTimer = null;
  const AUTOPLAY_INTERVAL = 3800; // 3,8 segundos para leitura agradável

  function goToSlide(index) {
    if (index < 0) {
      currentIndex = totalSlides - 1;
    } else if (index >= totalSlides) {
      currentIndex = 0;
    } else {
      currentIndex = index;
    }

    // Move a esteira horizontalmente
    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    // Atualiza slides
    slides.forEach((slide, idx) => {
      slide.classList.toggle("active", idx === currentIndex);
    });

    // Atualiza os pontinhos (dots)
    dots.forEach((dot, idx) => {
      dot.classList.toggle("active", idx === currentIndex);
    });
  }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(() => {
      goToSlide(currentIndex + 1);
    }, AUTOPLAY_INTERVAL);
  }

  function stopAutoplay() {
    if (autoplayTimer) {
      clearInterval(autoplayTimer);
      autoplayTimer = null;
    }
  }

  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  // Iniciar autoplay
  startAutoplay();

  // Pausar ao passar o mouse por cima
  if (carouselContainer) {
    carouselContainer.addEventListener("mouseenter", stopAutoplay);
    carouselContainer.addEventListener("mouseleave", startAutoplay);
  }

  // Navegação pelos pontinhos menores
  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const targetIndex = parseInt(dot.getAttribute("data-index"), 10);
      if (!isNaN(targetIndex)) {
        goToSlide(targetIndex);
        restartAutoplay();
      }
    });
  });

  // Suporte a Touch / Arraste no celular
  let startX = 0;
  let endX = 0;
  let isSwiping = false;

  if (carouselContainer) {
    carouselContainer.addEventListener("touchstart", (e) => {
      stopAutoplay();
      startX = e.touches[0].clientX;
      isSwiping = true;
    }, { passive: true });

    carouselContainer.addEventListener("touchmove", (e) => {
      if (!isSwiping) return;
      endX = e.touches[0].clientX;
    }, { passive: true });

    carouselContainer.addEventListener("touchend", () => {
      if (!isSwiping) return;
      isSwiping = false;
      const diffX = startX - endX;
      
      // Limiar mínimo de 35px para considerar swipe
      if (Math.abs(diffX) > 35) {
        if (diffX > 0) {
          goToSlide(currentIndex + 1);
        } else {
          goToSlide(currentIndex - 1);
        }
      }
      startX = 0;
      endX = 0;
      startAutoplay();
    });
  }
}

// ==========================================================================
// 8. LINKS LEGAIS DO RODAPÉ
// ==========================================================================
function initLegalModalLinks() {
  const legalLinks = document.querySelectorAll(".legal-modal-link");
  
  legalLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const type = link.getAttribute("data-legal");
      let message = "";

      switch (type) {
        case "termos":
          message = "Termos de Uso: Este material destina-se ao aprendizado pessoal de cultivo doméstico. Proibida a redistribuição ou cópia não autorizada.";
          break;
        case "privacidade":
          message = "Política de Privacidade: Seus dados cadastrais e de pagamento são protegidos por criptografia de ponta a ponta e processados exclusivamente pela plataforma de pagamento certificada.";
          break;
        case "suporte":
          message = "Suporte & Atendimento: Você pode entrar em contato conosco pelo e-mail: suporte@hortainfinita.com (Atendimento de segunda a sexta, das 9h às 18h).";
          break;
        default:
          message = "Informações institucionais e educacionais do produto Horta Infinita.";
      }

      alert(message);
    });
  });
}
