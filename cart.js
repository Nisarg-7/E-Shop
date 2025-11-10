document.addEventListener("DOMContentLoaded", () => {
  let cartItems = JSON.parse(localStorage.getItem("cart")) || [];

  const cartContainer = document.getElementById("cart-items");
  const totalItems = document.getElementById("total-items");
  const totalPrice = document.getElementById("total-price");
  const checkoutBtn = document.getElementById("checkout-btn");

  function renderCart() {
    cartContainer.innerHTML = "";

    if (cartItems.length === 0) {
      cartContainer.innerHTML = `<p>Your cart is empty!</p>`;
      totalItems.textContent = "0";
      totalPrice.textContent = "$0";
      return;
    }

    cartItems.forEach((item) => {
      const card = document.createElement("div");
      card.classList.add("cart-item");

      card.innerHTML = `
        <img src="${item.image_url || 'https://via.placeholder.com/80'}" alt="${item.name}">
        <div class="cart-info">
          <h3>${item.name}</h3>
          <p>Price: $${item.price}</p>
          <label>Quantity:</label>
          <input type="number" min="1" value="${item.quantity}" data-id="${item.id}" class="qty-input">
          <p class="subtotal">Subtotal: $${(item.price * item.quantity).toFixed(2)}</p>
        </div>
        <button class="remove-btn" data-id="${item.id}">Remove</button>
      `;

      cartContainer.appendChild(card);
    });

    updateSummary();
  }

  function updateSummary() {
    const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const itemCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

    totalItems.textContent = itemCount;
    totalPrice.textContent = `$${total.toFixed(2)}`;
  }

  cartContainer.addEventListener("input", (e) => {
    if (e.target.classList.contains("qty-input")) {
      const id = parseInt(e.target.dataset.id);
      const newQty = parseInt(e.target.value);
      const item = cartItems.find((i) => i.id === id);
      if (item && newQty > 0) {
        item.quantity = newQty;
        localStorage.setItem("cart", JSON.stringify(cartItems));
        renderCart();
      }
    }
  });

  cartContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-btn")) {
      const id = parseInt(e.target.dataset.id);
      cartItems = cartItems.filter((i) => i.id !== id);
      localStorage.setItem("cart", JSON.stringify(cartItems));
      renderCart();
    }
  });

  checkoutBtn.addEventListener("click", () => {
    if (cartItems.length === 0) {
      alert("Your cart is empty!");
      return;
    }

    // Save for checkout
    localStorage.setItem("checkoutItems", JSON.stringify(cartItems));
    window.location.href = "checkout.html";
  });

  renderCart();
});
