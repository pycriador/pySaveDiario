$(function () {
  const toastElements = document.querySelectorAll("#toastZone .toast");
  toastElements.forEach((toastEl) => {
    if (window.bootstrap) {
      const toast = new bootstrap.Toast(toastEl);
      toast.show();
    }
  });

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
    modalEl.querySelector(".modal-body").textContent =
      "Tem certeza que deseja remover " + userName + "?";
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
    });
  }
});

