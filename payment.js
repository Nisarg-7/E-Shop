document.addEventListener("DOMContentLoaded", () => {
  const cardOption = document.getElementById("cardOption");
  const upiOption = document.getElementById("upiOption");
  const cardForm = document.getElementById("cardForm");
  const upiForm = document.getElementById("upiForm");

  // show card form
  cardOption.addEventListener("click", () => {
    cardForm.classList.remove("hidden");
    upiForm.classList.add("hidden");
  });

  // show upi form
  upiOption.addEventListener("click", () => {
    upiForm.classList.remove("hidden");
    cardForm.classList.add("hidden");
  });

  // handle card payment
  cardForm.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Processing Card Payment...");
    window.location.href = "success.html";
  });

  // handle upi payment
  upiForm.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Processing UPI Payment...");
    window.location.href = "success.html";
  });
});
