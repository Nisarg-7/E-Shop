const API_BASE = 'http://localhost:8000';

// Ensure token exists
const token = localStorage.getItem('access_token');
console.log("Admin Token:", token);
if (!token) {
  alert("No token found! Please login again.");
  window.location.href = "index.html";
}

// Fetch and display all products for admin
async function loadAdminProducts() {
  try {
    const res = await fetch(`${API_BASE}/product/`);
    if (!res.ok) throw new Error('Failed to fetch products');
    const data = await res.json();

    const adminTable = document.getElementById('admin-products-table');
    adminTable.innerHTML = `
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Color</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Description</th>
        <th>Actions</th>
      </tr>
    `;

    data.data.forEach(product => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${product.id}</td>
        <td><input type="text" value="${product.name}" id="name-${product.id}"></td>
        <td><input type="text" value="${product.color || ''}" id="color-${product.id}"></td>
        <td><input type="number" value="${product.quantity}" id="qty-${product.id}"></td>
        <td><input type="number" value="${product.price}" id="price-${product.id}"></td>
        <td><input type="text" value="${product.description}" id="desc-${product.id}"></td>
        <td>
          <button onclick="updateProduct(${product.id})">💾 Save</button>
          <button onclick="deleteProduct(${product.id})">🗑️ Delete</button>
        </td>
      `;
      adminTable.appendChild(row);
    });

  } catch (err) {
    console.error('Error loading admin products:', err);
  }
}

// Update product details
async function updateProduct(id) {
  const updatedData = {
    name: document.getElementById(`name-${id}`).value,
    color: document.getElementById(`color-${id}`).value,
    quantity: parseInt(document.getElementById(`qty-${id}`).value),
    price: parseFloat(document.getElementById(`price-${id}`).value),
    description: document.getElementById(`desc-${id}`).value
  };

  try {
    const res = await fetch(`${API_BASE}/product/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(updatedData)
    });

    if (!res.ok) throw new Error('Failed to update product');
    alert('✅ Product updated successfully!');
    await loadAdminProducts();

  } catch (err) {
    console.error('Error updating product:', err);
    alert('Error updating product!');
  }
}

// Delete product
async function deleteProduct(id) {
  if (!confirm('Are you sure you want to delete this product?')) return;

  try {
    const res = await fetch(`${API_BASE}/product/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!res.ok) throw new Error('Failed to delete product');
    alert('🗑️ Product deleted!');
    await loadAdminProducts();

  } catch (err) {
    console.error('Error deleting product:', err);
    alert('Error deleting product!');
  }
}

// Auto-load on page open
//document.addEventListener('DOMContentLoaded', loadAdminProducts);
