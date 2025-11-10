<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", () => {
  const products = [
    { id: 1, name: "iphone 15", price: 54999, image: "phone.png" },
    { id: 2, name: "Dell 15", price: 59599, image: "laptop.jpg" },
    { id: 3, name: "Sony Bravia 3", price: 69549, image: "tv.jpg" },
    { id: 4, name: "LG Air Conditioner", price: 27999, image: "ac.jpg" },
    { id: 5, name: "Samsung 3 star convertible refrigerator", price: 45999, image: "refrigerator.jpg" },
    { id: 6, name: "whirpool magic clean 5 star washing machine", price: 24999, image: "washing machine.jpg" }
  ];

  const productList = document.getElementById("productList");
  productList.innerHTML = products.map(p => `
    <div class="product-card">
      <img src="${p.image}" alt="${p.name}">
      <h3>${p.name}</h3>
      <p>$${p.price}</p>
    </div>
  `).join("");
});
=======
document.addEventListener("DOMContentLoaded", () => {
  const products = [
    { id: 1, name: "iphone 15", price: 54999, image: "phone.png" },
    { id: 2, name: "Dell 15", price: 59599, image: "laptop.jpg" },
    { id: 3, name: "Sony Bravia 3", price: 69549, image: "tv.jpg" },
    { id: 4, name: "LG Air Conditioner", price: 27999, image: "ac.jpg" },
    { id: 5, name: "Samsung 3 star convertible refrigerator", price: 45999, image: "refrigerator.jpg" },
    { id: 6, name: "whirpool magic clean 5 star washing machine", price: 24999, image: "washing machine.jpg" }
  ];

  const productList = document.getElementById("productList");
  productList.innerHTML = products.map(p => `
    <div class="product-card">
      <img src="${p.image}" alt="${p.name}">
      <h3>${p.name}</h3>
      <p>$${p.price}</p>
    </div>
  `).join("");
});
>>>>>>> 3ed5567 (Initial commit)
