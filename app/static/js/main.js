// ========================================
// pySave Diário - Main JavaScript
// ========================================

$(function () {
  // === Toast Notifications ===
  const toastElements = document.querySelectorAll("#toastZone .toast");
  toastElements.forEach((toastEl) => {
    if (window.bootstrap) {
      const toast = new bootstrap.Toast(toastEl);
      toast.show();
    }
  });

  // === Delete Confirmation Modal ===
  const modalEl = document.getElementById("confirmModal");
  let deleteModal = null;
  let deleteFormRef = null;

  if (modalEl && window.bootstrap) {
    deleteModal = new bootstrap.Modal(modalEl);
  }

  $(".trigger-delete").on("click", function () {
    if (!deleteModal) return;
    const formId = $(this).data("form-id");
    const userName = $(this).data("user-name");
    deleteFormRef = document.getElementById(formId);
    
    // Update modal content
    const modalBody = modalEl.querySelector(".modal-body");
    modalBody.innerHTML = `
      <div class="text-center">
        <i class="bi bi-exclamation-triangle-fill" style="font-size: 3rem; color: var(--danger);"></i>
        <p class="mt-3 mb-2" style="font-size: 1.1rem;">Tem certeza que deseja remover <strong>${userName}</strong>?</p>
        <p class="muted mb-0" style="font-size: 0.9rem;">Esta ação não pode ser desfeita.</p>
      </div>
    `;
    
    deleteModal.show();
  });

  $("#confirmModalBtn").on("click", function () {
    if (deleteFormRef) {
      deleteFormRef.submit();
      deleteFormRef = null;
    }
    if (deleteModal) {
      deleteModal.hide();
    }
  });

  // === Theme Toggle ===
  const root = document.documentElement;
  const storageKey = "pysave-theme";
  const toggleBtn = document.getElementById("themeToggle");

  function applyTheme(theme) {
    if (theme === "light") {
      root.classList.add("light-theme");
    } else {
      root.classList.remove("light-theme");
    }
  }

  const storedTheme = localStorage.getItem(storageKey) || "dark";
  applyTheme(storedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const isLight = root.classList.toggle("light-theme");
      localStorage.setItem(storageKey, isLight ? "light" : "dark");
      
      // Add smooth rotation animation
      toggleBtn.style.transform = "rotate(360deg)";
      setTimeout(() => {
        toggleBtn.style.transform = "rotate(0deg)";
      }, 300);
    });
  }

  // === Smooth Scroll for Anchor Links ===
  $('a[href^="#"]').on("click", function (e) {
    const target = $(this.getAttribute("href"));
    if (target.length) {
      e.preventDefault();
      $("html, body").animate(
        {
          scrollTop: target.offset().top - 80,
        },
        600
      );
    }
  });

  // === Add Animation Classes on Scroll ===
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  document.querySelectorAll(".panel, .card, .form-card").forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    observer.observe(el);
  });

  // === Form Validation Enhancement ===
  const forms = document.querySelectorAll("form[method='post']");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const requiredFields = form.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add("is-invalid");
          
          // Add visual feedback
          field.style.borderColor = "var(--danger)";
          setTimeout(() => {
            field.style.borderColor = "";
          }, 2000);
        } else {
          field.classList.remove("is-invalid");
        }
      });

      if (!isValid) {
        e.preventDefault();
        showToast("Por favor, preencha todos os campos obrigatórios.", "warning");
      }
    });
  });

  // === Auto-dismiss Alerts ===
  setTimeout(() => {
    $(".alert").fadeOut("slow");
  }, 5000);

  // === Loading State for Buttons ===
  $("form").on("submit", function () {
    const submitBtn = $(this).find('button[type="submit"]');
    if (submitBtn.length) {
      const originalText = submitBtn.html();
      submitBtn.html('<i class="bi bi-hourglass-split"></i> Processando...');
      submitBtn.prop("disabled", true);
      
      // Re-enable after 5 seconds as a fallback
      setTimeout(() => {
        submitBtn.html(originalText);
        submitBtn.prop("disabled", false);
      }, 5000);
    }
  });

  // === Modal Animation Enhancement ===
  $(".modal").on("show.bs.modal", function () {
    $(this).find(".modal-dialog").css({
      transform: "scale(0.95)",
      opacity: "0",
    });
    setTimeout(() => {
      $(this).find(".modal-dialog").css({
        transform: "scale(1)",
        opacity: "1",
        transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
      });
    }, 10);
  });

  // === Tooltip Initialization (if Bootstrap tooltips are used) ===
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // === Navbar Active Link Highlight ===
  const currentPath = window.location.pathname;
  $(".nav-link").each(function () {
    const linkPath = $(this).attr("href");
    if (currentPath === linkPath || currentPath.startsWith(linkPath + "/")) {
      $(this).addClass("active");
    }
  });

  // === Auto-hide Navbar on Scroll (Mobile) ===
  let lastScrollTop = 0;
  const navbar = $(".site-header");
  const scrollThreshold = 100;

  $(window).on("scroll", function () {
    const scrollTop = $(this).scrollTop();

    if (scrollTop > scrollThreshold) {
      if (scrollTop > lastScrollTop) {
        // Scrolling down
        navbar.css("transform", "translateY(-100%)");
      } else {
        // Scrolling up
        navbar.css("transform", "translateY(0)");
      }
    } else {
      navbar.css("transform", "translateY(0)");
    }

    lastScrollTop = scrollTop;
  });

  // Add transition to navbar
  navbar.css("transition", "transform 0.3s ease");

  // === Utility: Show Custom Toast ===
  function showToast(message, type = "info") {
    const toastHtml = `
      <div class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="4500">
        <div class="d-flex">
          <div class="toast-body">${message}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fechar"></button>
        </div>
      </div>
    `;

    const toastContainer = $("#toastZone");
    if (toastContainer.length) {
      toastContainer.append(toastHtml);
      const newToast = toastContainer.find(".toast").last()[0];
      const bsToast = new bootstrap.Toast(newToast);
      bsToast.show();
    }
  }

  // === Copy to Clipboard Functionality ===
  $(".copy-btn").on("click", function () {
    const textToCopy = $(this).data("copy");
    navigator.clipboard.writeText(textToCopy).then(() => {
      showToast("Copiado para a área de transferência!", "success");
    });
  });

  // === Character Counter for Textareas ===
  $("textarea[maxlength]").each(function () {
    const maxLength = $(this).attr("maxlength");
    const counter = $(`<small class="text-muted mt-1 d-block">0 / ${maxLength} caracteres</small>`);
    $(this).after(counter);

    $(this).on("input", function () {
      const currentLength = $(this).val().length;
      counter.text(`${currentLength} / ${maxLength} caracteres`);
      
      if (currentLength >= maxLength * 0.9) {
        counter.css("color", "var(--warning)");
      } else {
        counter.css("color", "var(--text-muted)");
      }
    });
  });

  // === Price Formatting for Input Fields ===
  $('input[type="number"]').on("blur", function () {
    const value = parseFloat($(this).val());
    if (!isNaN(value) && $(this).attr("step") === "0.01") {
      $(this).val(value.toFixed(2));
    }
  });

  // === Slug Generator ===
  function generateSlug(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-")
      .trim();
  }

  // Auto-generate slug from name field
  $('input[name="name"]').on("input", function () {
    const slugField = $('input[name="slug"]');
    if (slugField.length && !slugField.val()) {
      slugField.val(generateSlug($(this).val()));
    }
  });

  // === Console Welcome Message ===
  console.log(
    "%cpySave Diário",
    "color: #6366f1; font-size: 24px; font-weight: bold;"
  );
  console.log(
    "%cCentral inteligente de ofertas e wishlists 🚀",
    "color: #94a3b8; font-size: 14px;"
  );
  console.log(
    "%cAPI: /api/docs",
    "color: #8b5cf6; font-size: 12px;"
  );
});
