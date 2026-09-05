/**
 * HORTA INFINITA — SCRIPTS DE INTERAÇÃO, CARROSSEL & CONVERSÃO
 */

// ==========================================================================
// 1. CONFIGURAÇÃO DE LINKS DE CHECKOUT
// ==========================================================================
const CHECKOUT_URLS = {
  // Oferta Inicial (R$ 7,90)
  essencial: 'https://pay.lowify.com.br/checkout?product_id=kjttls',

  // Oferta Intermediária / Popup Plus (R$ 12,90)
  plus: 'https://pay.lowify.com.br/go.php?offer=laixs9z',

  // Oferta Completa / Melhor Custo-Benefício (R$ 17,90)
  completo: 'https://pay.lowify.com.br/go.php?offer=82j9nx7'
};

// ==========================================================================
// 2. INICIALIZAÇÃO ROBUSTA APÓS O CARREGAMENTO DO DOM
// ==========================================================================
function initAll() {
  initCheckoutLinks();
  initOfferModal();
  initFaqAccordion();
  initTestimonialsCarousel();
  initLegalModalLinks();
  initVslPlayer();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAll);
} else {
  initAll();
}

// ==========================================================================
// 3. GERENCIAMENTO DE LINKS DE CHECKOUT
// ==========================================================================
function initCheckoutLinks() {
  const checkoutElements = document.querySelectorAll('.checkout-link');
  
  checkoutElements.forEach((el) => {
    const tier = el.getAttribute('data-tier');
    if (tier && CHECKOUT_URLS[tier]) {
      el.href = CHECKOUT_URLS[tier];
      el.target = '_blank';
      el.rel = 'noopener noreferrer';
    }

    el.addEventListener('click', () => {
      const tier = el.getAttribute('data-tier');
      if (tier && CHECKOUT_URLS[tier]) {
        el.href = CHECKOUT_URLS[tier];
      }
    });
  });
}

// ==========================================================================
// 4. MODAL POPUP DE UPSELL (R$ 12,90 COM OPÇÃO DE R$ 7,90)
// ==========================================================================
function initOfferModal() {
  const modal = document.getElementById('upgradeModal');
  const closeBtn = document.getElementById('modalCloseBtn');
  const openButtons = document.querySelectorAll('.open-offer-modal');

  if (!modal) return;

  let lastFocusedElement = null;

  function openModal() {
    lastFocusedElement = document.activeElement;
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    if (closeBtn) {
      setTimeout(() => closeBtn.focus(), 50);
    }
  }

  function closeModal() {
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus();
    }
  }

  openButtons.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openModal();
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

// ==========================================================================
// 5. ACCORDION DE DÚVIDAS FREQUENTES (FAQ)
// ==========================================================================
function initFaqAccordion() {
  const faqTriggers = document.querySelectorAll('.faq-trigger');

  faqTriggers.forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
      const content = trigger.nextElementSibling;
      const parentItem = trigger.closest('.faq-item');

      faqTriggers.forEach((otherTrigger) => {
        if (otherTrigger !== trigger) {
          otherTrigger.setAttribute('aria-expanded', 'false');
          const otherItem = otherTrigger.closest('.faq-item');
          if (otherItem) otherItem.classList.remove('active');
          const otherContent = otherTrigger.nextElementSibling;
          if (otherContent) {
            otherContent.style.maxHeight = null;
            otherContent.classList.remove('open');
          }
        }
      });

      if (isExpanded) {
        trigger.setAttribute('aria-expanded', 'false');
        if (parentItem) parentItem.classList.remove('active');
        if (content) {
          content.style.maxHeight = null;
          content.classList.remove('open');
        }
      } else {
        trigger.setAttribute('aria-expanded', 'true');
        if (parentItem) parentItem.classList.add('active');
        if (content) {
          content.classList.add('open');
          content.style.maxHeight = (content.scrollHeight + 32) + 'px';
        }
      }
    });
  });
}

// ==========================================================================
// 6. CARROSSEL DE DEPOIMENTOS DE WHATSAPP COM FOTOS REAIS
// ==========================================================================
function initTestimonialsCarousel() {
  const track = document.getElementById('carouselTrack');
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  const carouselContainer = document.getElementById('testimonialsCarousel');

  if (!track || slides.length === 0) return;

  let currentIndex = 0;
  const totalSlides = slides.length;
  let autoplayTimer = null;
  const AUTOPLAY_INTERVAL = 3800;

  function goToSlide(index) {
    if (index < 0) {
      currentIndex = totalSlides - 1;
    } else if (index >= totalSlides) {
      currentIndex = 0;
    } else {
      currentIndex = index;
    }

    track.style.transform = "translateX(-" + (currentIndex * 100) + "%)";

    slides.forEach((slide, idx) => {
      slide.classList.toggle('active', idx === currentIndex);
    });

    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === currentIndex);
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

  startAutoplay();

  if (carouselContainer) {
    carouselContainer.addEventListener('mouseenter', stopAutoplay);
    carouselContainer.addEventListener('mouseleave', startAutoplay);
  }

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const targetIndex = parseInt(dot.getAttribute('data-index'), 10);
      if (!isNaN(targetIndex)) {
        goToSlide(targetIndex);
        restartAutoplay();
      }
    });
  });

  let startX = 0;
  let endX = 0;
  let isSwiping = false;

  if (carouselContainer) {
    carouselContainer.addEventListener('touchstart', (e) => {
      stopAutoplay();
      startX = e.touches[0].clientX;
      endX = 0;
      isSwiping = true;
    }, { passive: true });

    carouselContainer.addEventListener('touchmove', (e) => {
      if (!isSwiping) return;
      endX = e.touches[0].clientX;
    }, { passive: true });

    const handleTouchEnd = () => {
      if (!isSwiping) return;
      isSwiping = false;
      
      // Se houve movimento horizontal real acima de 35px
      if (endX !== 0) {
        const diffX = startX - endX;
        if (Math.abs(diffX) > 35) {
          if (diffX > 0) {
            goToSlide(currentIndex + 1);
          } else {
            goToSlide(currentIndex - 1);
          }
        }
      }
      
      startX = 0;
      endX = 0;
      startAutoplay();
    };

    carouselContainer.addEventListener('touchend', handleTouchEnd);
    carouselContainer.addEventListener('touchcancel', handleTouchEnd);
  }

  // Pausa se o usuário mudar de aba e retoma ao voltar
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopAutoplay();
    } else {
      startAutoplay();
    }
  });
}

// ==========================================================================
// 7. LINKS LEGAIS DO RODAPÉ (COM NOVO E-MAIL DE SUPORTE)
// ==========================================================================
function initLegalModalLinks() {
  const legalLinks = document.querySelectorAll('.legal-modal-link');
  
  legalLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const type = link.getAttribute('data-legal');
      let message = '';

      switch (type) {
        case 'termos':
          message = 'Termos de Uso: Este material destina-se ao aprendizado pessoal de cultivo doméstico. Proibida a redistribuição ou cópia não autorizada.';
          break;
        case 'privacidade':
          message = 'Política de Privacidade: Seus dados cadastrais e de pagamento são protegidos por criptografia de ponta a ponta e processados exclusivamente pela plataforma de pagamento certificada.';
          break;
        case 'suporte':
          message = 'Suporte & Atendimento: Você pode entrar em contato conosco pelo e-mail: suporte.centralaocliente@gmail.com (Atendimento de segunda a sexta, das 9h às 18h).';
          break;
        default:
          message = 'Informações institucionais e educacionais do produto Horta Infinita.';
      }

      alert(message);
    });
  });
}

// ==========================================================================
// 8. INTERAÇÃO DA VSL / VÍDEO DE APRESENTAÇÃO
// ==========================================================================
function initVslPlayer() {
  const vslPlayer = document.getElementById('vslPlayer');
  if (!vslPlayer) return;

  const playBtn = vslPlayer.querySelector('.vsl-play-btn');
  const handleClick = (e) => {
    e.preventDefault();
    const offersSection = document.getElementById('ofertas');
    if (offersSection) {
      offersSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (playBtn) {
    playBtn.addEventListener('click', handleClick);
  }
}
