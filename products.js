const API_BASE = 'http://localhost:8000'
let currentUser = null;
let categories = [];
let products = [];

// Check if we have a token before anything else
function checkAuth() {
    const token = localStorage.getItem('access_token');
    console.log('Checking authentication...');
    if (!token) {
        console.log('No token found, redirecting to login...');
        window.location.replace('/index.html');
        return false;
    }
    console.log('Token found, proceeding with initialization...');
    return true;
}

// Ensure we're authenticated before running anything
if (!checkAuth()) {
    throw new Error('Not authenticated');
}

// Check authentication on page load
console.log("Script loaded!");
document.addEventListener('DOMContentLoaded', async () => {
    console.log("DOM fully loaded!");
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    try {
        // Get current user info
        const res = await fetch(`${API_BASE}/protected`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) {
            throw new Error('Authentication failed');
        }
        const data = await res.json();
        currentUser = data;
        updateUserInfo();

        // Load initial data
        await Promise.all([
            loadCategories(),
            loadProducts()
        ]);
    } catch (err) {
        console.error('Auth error:', err);
        window.location.href = 'index.html';
    }
});

// User info display
function updateUserInfo() {
    const userInfo = document.getElementById('user-info');
    if (currentUser) {
        userInfo.textContent = `Welcome, ${currentUser.username}`;
    }
}

// Logout handler


// Load and display categories
async function loadCategories() {
    try {
        const res = await fetch(`${API_BASE}/category/`);
        if (!res.ok) throw new Error('Failed to load categories');
        const data = await res.json();
        categories = data.categories;
        
        // Update category filters
        const categoryFilters = document.getElementById('category-filters');
        categoryFilters.innerHTML = categories.map(cat => `
            <div class="category-filter">
                <input type="checkbox" id="cat-${cat.id}" value="${cat.id}">
                <label for="cat-${cat.id}">${cat.name}</label>
            </div>
        `).join('');

        // Update category select in add product form
        const categorySelect = document.getElementById('product-category');
        categorySelect.innerHTML = categories.map(cat => 
            `<option value="${cat.id}">${cat.name}</option>`
        ).join('');

        // Add event listeners for filtering
        categoryFilters.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', filterProducts);
        });
    } catch (err) {
        console.error('Error loading categories:', err);
    }
}

// Load and display products
async function loadProducts() {
    try {
        const res = await fetch(`${API_BASE}/product/`);
        if (!res.ok) throw new Error('Failed to load products');
        const data = await res.json();
        products = data.data;
        displayProducts(products);
    } catch (err) {
        console.error('Error loading products:', err);
    }
}

// Display products in grid
function displayProducts(productsToShow) {
    const container = document.getElementById('products-container');
    container.innerHTML = productsToShow.map(product => `
        <div class="product-card">
            <img src="${product.image_url || 'https://placehold.co/300'}" alt="${product.name}" class="product-image">
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div class="product-meta">
                    <div>Quantity: ${product.quantity}</div>
                    ${product.size ? `<div>Size: ${product.size}</div>` : ''}
                    ${product.color ? `<div>Color: ${product.color}</div>` : ''}
                    <div>Status: ${product.stock_status ? 'In Stock' : 'Out of Stock'}</div>
                </div>
                <button class="primary-button add-to-cart-btn" data-product-id="${product.id}">
          🛒 Add to Cart
        </button>
            </div>
        </div>
    `).join('');
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      const productId = e.target.getAttribute('data-product-id');
      const product = products.find(p => p.id == productId);
      if (!product) return;

      // Get existing cart or create empty
      let cart = JSON.parse(localStorage.getItem('cart')) || [];

      // Check if product already in cart
      const existing = cart.find(item => item.id === product.id);
      if (existing) {
        existing.quantity += 1;
      } else {
        cart.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image_url: product.image_url,
          quantity: 1
        });
      }

      // Save updated cart
      localStorage.setItem('cart', JSON.stringify(cart));

      // Confirmation alert
      alert(`🛒 ${product.name} added to cart!`);
    });
  });
}


// Search and filter functionality


function filterProducts() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const selectedCategories = Array.from(document.querySelectorAll('#category-filters input:checked'))
        .map(input => parseInt(input.value));

    const filtered = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) ||
                            product.description.toLowerCase().includes(searchTerm);
        const matchesCategory = selectedCategories.length === 0 || 
                              selectedCategories.includes(product.category_id);
        return matchesSearch && matchesCategory;
    });

    displayProducts(filtered);
}

// modal
function openModal() {
    document.getElementById('product-modal').style.display = 'flex';
}
function closeModal() {
    document.getElementById('product-modal').style.display = 'none';
}

// Product form submit handler
document.addEventListener("DOMContentLoaded", () => {
    const addProductBtn = document.getElementById('add-product');
    if (addProductBtn) addProductBtn.addEventListener('click', openModal);

    const logoutBtn = document.getElementById('logout');
    if (logoutBtn) logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = 'index.html';
    });

    const productForm = document.getElementById('product-form');
    if (productForm) {
        productForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const form = e.target;
            const token = localStorage.getItem('access_token');
            console.log("Token being sent:", token);  // 🧩 important check

            if (!token) {
                alert("No token found! Please log in again.");
                return;
            }

            const productData = {
                name: form.name.value,
                description: form.description.value,
                price: parseFloat(form.price.value),
                quantity: parseInt(form.quantity.value),
                category_id: parseInt(form.category_id.value),
                size: form.size.value,
                color: form.color.value,
                stock_status: true,
                seller_id: currentUser?.id
            };

            try {
                const res = await fetch(`${API_BASE}/product/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`  // ✅ fix
                    },
                    body: JSON.stringify(productData)
                });

                if (!res.ok) throw new Error('Failed to create product');
                const productResponse = await res.json();
                console.log("Product created:", productResponse);

                await loadProducts();
                closeModal();
                form.reset();
            } catch (err) {
                console.error('Error creating product:', err);
                alert('Failed to create product. Please try again.');
            }
        });
    }
});


