const API_BASE_URL = 'http://localhost:5000';

// --- Message Handling ---
function showMessage(message, type = 'success') {
    const msgDiv = document.getElementById('globalMessage');
    msgDiv.textContent = message;
    msgDiv.className = `message ${type}`;
    msgDiv.style.display = 'block';
    setTimeout(() => { msgDiv.style.display = 'none'; }, 5000);
}

// --- UOM Functions ---
async function fetchUOMs() {
    try {
        const response = await fetch(`${API_BASE_URL}/getUOM`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status} - ${await response.text()}`);
        const uoms = await response.json();
        
        const uomSelect = document.getElementById('productUom');
        uomSelect.innerHTML = '<option value="">Select UOM</option>'; // Clear existing
        uoms.forEach(uom => {
            const option = document.createElement('option');
            option.value = uom.uom_id;
            option.textContent = uom.uom_name;
            uomSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching UOMs:', error);
        showMessage('Failed to load UOMs. ' + error.message, 'error');
    }
}

// --- Product Functions ---
async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/getProducts`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status} - ${await response.text()}`);
        const products = await response.json();
        
        const tbody = document.getElementById('productsTable').getElementsByTagName('tbody')[0];
        tbody.innerHTML = ''; // Clear existing rows
        products.forEach(product => {
            const row = tbody.insertRow();
            row.insertCell().textContent = product.product_id;
            row.insertCell().textContent = product.name;
            row.insertCell().textContent = product.uom_name;
            row.insertCell().textContent = parseFloat(product.price_per_unit).toFixed(2);
            
            const actionsCell = row.insertCell();
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.className = 'delete';
            deleteButton.onclick = () => deleteProduct(product.product_id);
            actionsCell.appendChild(deleteButton);
        });
    } catch (error) {
        console.error('Error fetching products:', error);
        showMessage('Failed to load products. ' + error.message, 'error');
    }
}

document.getElementById('addProductForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const productData = {
        name: formData.get('productName'),
        uom_id: formData.get('productUom'),
        price_per_unit: formData.get('productPrice')
    };

    const payload = new FormData();
    payload.append('data', JSON.stringify(productData));

    try {
        const response = await fetch(`${API_BASE_URL}/insertProduct`, {
            method: 'POST',
            body: payload 
        });
        const result = await response.json();
        if (!response.ok) {
            const errorMsg = result.error || result.message || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg  + (result.details ? ` - ${result.details}` : ''));
        }
        
        showMessage(`Product added successfully! ID: ${result.product_id}`, 'success');
        fetchProducts(); // Refresh product list
        this.reset(); // Reset form
    } catch (error) {
        console.error('Error adding product:', error);
        showMessage('Failed to add product. ' + error.message, 'error');
    }
});

async function deleteProduct(productId) {
    if (!confirm(`Are you sure you want to delete product ID ${productId}?`)) return;

    const payload = new FormData();
    payload.append('product_id', productId);

    try {
        const response = await fetch(`${API_BASE_URL}/deleteProduct`, {
            method: 'POST',
            body: payload
        });
        const result = await response.json();
        if (!response.ok) {
             const errorMsg = result.error || result.message || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg  + (result.details ? ` - ${result.details}` : ''));
        }
        
        showMessage(result.message || `Product ID ${productId} deleted.`, 'success');
        fetchProducts(); // Refresh product list
    } catch (error) {
        console.error('Error deleting product:', error);
        showMessage('Failed to delete product. ' + error.message, 'error');
    }
}

// --- Order Functions ---
async function fetchOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/getAllOrders`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status} - ${await response.text()}`);
        const orders = await response.json();
        
        const tbody = document.getElementById('ordersTable').getElementsByTagName('tbody')[0];
        tbody.innerHTML = ''; // Clear existing rows
        orders.forEach(order => {
            const row = tbody.insertRow();
            row.insertCell().textContent = order.order_id;
            row.insertCell().textContent = order.customer_name;
            row.insertCell().textContent = parseFloat(order.total_cost).toFixed(2);
            row.insertCell().textContent = order.datetime;
        });
    } catch (error) {
        console.error('Error fetching orders:', error);
        showMessage('Failed to load orders. ' + error.message, 'error');
    }
}

document.getElementById('addOrderForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    const orderDetails = [
        {
            product_id: formData.get('product_id_1') || 1, 
            quantity: parseFloat(formData.get('quantity_1')) || 1,     
            total_price: parseFloat(formData.get('total_price_1')) || 10 
        }
    ];
    
    const validOrderDetails = orderDetails.filter(d => d.product_id && !isNaN(d.quantity) && !isNaN(d.total_price) );

    const orderData = {
        customer_name: formData.get('customerName'),
        grand_total: formData.get('grandTotal'),
        datetime: new Date().toISOString().slice(0, 19).replace('T', ' '), 
        order_details: validOrderDetails.length > 0 ? validOrderDetails : [{ product_id: 1, quantity: 0, total_price: 0 }]
    };
    
    if (validOrderDetails.length === 0) {
         console.warn("No valid order details could be constructed from form, sending a placeholder detail. Ensure hidden fields (product_id_1, etc.) are correctly set or modify JS to build details properly.");
    }

    const payload = new FormData();
    payload.append('data', JSON.stringify(orderData));

    try {
        const response = await fetch(`${API_BASE_URL}/insertOrder`, {
            method: 'POST',
            body: payload
        });
        const result = await response.json();
        if (!response.ok) {
            const errorMsg = result.error || result.message || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg  + (result.details ? ` - ${result.details}` : ''));
        }
        
        showMessage(`Order added successfully! ID: ${result.order_id}`, 'success');
        fetchOrders(); 
        this.reset(); 
    } catch (error) {
        console.error('Error adding order:', error);
        showMessage('Failed to add order. ' + error.message, 'error');
    }
});

// --- Initial Load ---
window.onload = () => {
    fetchUOMs();
    fetchProducts();
    fetchOrders();
};