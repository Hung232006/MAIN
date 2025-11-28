window.onload = function () {
  // Popup chào mừng
  const welcomePopup = document.getElementById("welcome-popup");
  const btnCloseWelcome = document.getElementById("close-popup");
  if (welcomePopup && btnCloseWelcome) {
    welcomePopup.classList.add("active");;
welcomePopup.setAttribute("aria-hidden", "false");
    btnCloseWelcome.addEventListener("click", () => {
welcomePopup.classList.remove("active");
welcomePopup.setAttribute("aria-hidden", "true");

    });
  }

  // Popup sản phẩm
  const productPopup = document.getElementById("product-popup");
  const closeProductPopup = document.getElementById("close-product-popup");
  const popupImage = document.getElementById("popup-image");
  const popupName = document.getElementById("popup-name");
  const popupPrice = document.getElementById("popup-price");
  const popupSize = document.getElementById("popup-size");
  const btnPay = document.getElementById("btn-pay");
  const btnAddCart = document.getElementById("btn-add-cart");

  // Giỏ hàng
  const cartCountEl = document.getElementById("cart-count");
  let cartCount = 0;

  // Mở popup khi nhấn "Mua Ngay"
  document.querySelectorAll(".products .item .btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const item = e.target.closest(".item");
      const imgEl = item.querySelector("img");
      const nameEl = item.querySelector("h5");
      const priceEl = item.querySelector(".price");

      popupImage.src = imgEl?.src || "";
      popupImage.alt = nameEl?.innerText || "Sản phẩm";
      popupName.innerText = nameEl?.innerText || "";
      popupPrice.innerText = priceEl?.innerText || "";
      popupSize.value = ""; // reset chọn size

      productPopup.classList.add("active");
      productPopup.setAttribute("aria-hidden", "false");
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Đóng popup sản phẩm
  if (closeProductPopup) {
    closeProductPopup.addEventListener("click", () => {
      productPopup.classList.remove("active");
      productPopup.setAttribute("aria-hidden", "true");
    });
  }

  // Hàm hiển thị toast
  function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast-message ${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 100);
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 500);
    }, 3000);
  }

  // Lấy số lượng giỏ hàng từ server khi load
  fetch('/api/cart-count')
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        cartCount = data.count;
        if (cartCount > 0) {
          cartCountEl.innerText = cartCount;
          cartCountEl.classList.remove("hidden");
        }
      }
    })
    .catch(err => console.error("Không thể lấy số lượng giỏ hàng:", err));

  // Thêm vào giỏ hàng
  if (btnAddCart) {
    btnAddCart.addEventListener("click", () => {
      if (!popupSize.value) {
        showToast("Vui lòng chọn size trước khi thêm vào giỏ hàng.", "error");
        return;
      }

      const productName = popupName.innerText;
      const size = popupSize.value;

      fetch('/api/add-to-cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name: productName, size: size, quantity: 1 })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          cartCount += 1;
          cartCountEl.innerText = String(cartCount);
          cartCountEl.classList.remove("hidden");

          showToast("Đã thêm vào giỏ hàng!");
          productPopup.classList.remove("active");
          productPopup.setAttribute("aria-hidden", "true");
        } else {
          showToast("Lỗi: " + data.message, "error");
        }
      })
      .catch(err => {
        console.error("Error:", err);
        showToast("Có lỗi xảy ra khi thêm vào giỏ hàng", "error");
      });
    });
  }

  // Thanh toán demo
  if (btnPay) {
    btnPay.addEventListener("click", () => {
      if (!popupSize.value) {
        showToast("Bạn cần chọn size trước khi thanh toán.", "error");
        return;
      }
      showToast("Đi đến trang thanh toán (demo).");
      // window.location.href = "/checkout.html";
    });
  }

  // Đóng popup khi click nền tối
  [welcomePopup, productPopup].forEach((pop) => {
    if (!pop) return;
    pop.addEventListener("click", (e) => {
      if (e.target === pop) {
        pop.classList.remove("active");
        pop.setAttribute("aria-hidden", "true");
      }
    });
  });

  // Đóng popup bằng phím ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      [welcomePopup, productPopup].forEach((pop) => {
        if (pop && pop.classList.contains("active")) {
          pop.classList.remove("active");
          pop.setAttribute("aria-hidden", "true");
        }
      });
    }
  });

  // Sự kiện cho nút đăng nhập/đăng ký
  const btnLogin = document.getElementById("btn-login");
  const btnRegister = document.getElementById("btn-register");

  if (btnLogin) {
    btnLogin.addEventListener("click", () => {
      window.location.href = "/login.html";
    });
  }
  if (btnRegister) {
    btnRegister.addEventListener("click", () => {
      window.location.href = "/register.html";
    });
  }
};
