    window.onload = function () {
  // Popup chào mừng
  const welcomePopup = document.getElementById("welcome-popup");
  const btnCloseWelcome = document.getElementById("close-popup");
  if (welcomePopup && btnCloseWelcome) {
    welcomePopup.style.display = "flex";
    btnCloseWelcome.addEventListener("click", () => {
      welcomePopup.style.display = "none";
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
      const nameEl = item.querySelectorAll("p")[0];
      const priceEl = item.querySelectorAll("p")[1];

      popupImage.src = imgEl?.src || "";
      popupImage.alt = nameEl?.innerText || "Sản phẩm";
      popupName.innerText = nameEl?.innerText || "";
      popupPrice.innerText = priceEl?.innerText || "";
      popupSize.value = ""; // reset chọn size

      productPopup.style.display = "flex";
      productPopup.setAttribute("aria-hidden", "false");
    });
  });

  // Đóng popup sản phẩm
  if (closeProductPopup) {
    closeProductPopup.addEventListener("click", () => {
      productPopup.style.display = "none";
      productPopup.setAttribute("aria-hidden", "true");
    });
  }

  // Thêm vào giỏ hàng
  if (btnAddCart) {
    btnAddCart.addEventListener("click", () => {
      // Bắt buộc chọn size trước khi thêm
      if (!popupSize.value) {
        alert("Vui lòng chọn size trước khi thêm vào giỏ hàng.");
        return;
      }

      cartCount += 1;
      cartCountEl.innerText = String(cartCount);
      cartCountEl.classList.remove("hidden"); // chỉ hiển thị sau khi nhấn mua

      // Ẩn popup sau khi thêm
      productPopup.style.display = "none";
      productPopup.setAttribute("aria-hidden", "true");
    });
  }

  // Thanh toán (demo): chuyển hướng hoặc hiện thông báo
  if (btnPay) {
    btnPay.addEventListener("click", () => {
      if (!popupSize.value) {
        alert("Bạn cần chọn size trước khi thanh toán.");
        return;
      }
      alert("Đi đến trang thanh toán (demo). Bạn có thể gắn link thật tại đây.");
      // Ví dụ: window.location.href = "/checkout.html";
    });
  }

  // Đóng popup khi click nền tối (bên ngoài nội dung)
  [welcomePopup, productPopup].forEach((pop) => {
    if (!pop) return;
    pop.addEventListener("click", (e) => {
      if (e.target === pop) {
        pop.style.display = "none";
        pop.setAttribute("aria-hidden", "true");
      }
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && productPopup.style.display === "flex") {
      productPopup.style.display = "none";
      productPopup.setAttribute("aria-hidden", "true");
    }
  });
  //sự kiện cho nút đăng nhập đăng kí
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
