/* ============================================
   ORDER TRACKING SYSTEM - MAIN JAVASCRIPT
   ============================================ */

// ============================================
// 1. AUTO-HIDE ALERTS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentElement) {
                alert.style.display = 'none';
            }
        }, 5000);
    });
});

// ============================================
// 2. FORM VALIDATION
// ============================================

function validateOrderForm() {
    const form = document.querySelector('form');
    if (!form) return true;

    const orderId = document.getElementById('order_id');
    const customerName = document.getElementById('customer_name');
    const productName = document.getElementById('product_name');
    const quantity = document.getElementById('quantity');
    const price = document.getElementById('price');
    const orderDate = document.getElementById('order_date');
    const shippingAddress = document.getElementById('shipping_address');
    const contactNumber = document.getElementById('contact_number');

    let isValid = true;
    let errors = [];

    // Order ID validation
    if (orderId && orderId.value.trim() === '') {
        errors.push('Order ID is required');
        isValid = false;
    }

    // Customer name validation
    if (customerName && customerName.value.trim() === '') {
        errors.push('Customer name is required');
        isValid = false;
    }

    // Product name validation
    if (productName && productName.value.trim() === '') {
        errors.push('Product name is required');
        isValid = false;
    }

    // Quantity validation
    if (quantity && (quantity.value === '' || parseInt(quantity.value) <= 0)) {
        errors.push('Quantity must be greater than 0');
        isValid = false;
    }

    // Price validation
    if (price && (price.value === '' || parseFloat(price.value) < 0)) {
        errors.push('Price cannot be negative');
        isValid = false;
    }

    // Order date validation
    if (orderDate && orderDate.value === '') {
        errors.push('Order date is required');
        isValid = false;
    }

    // Shipping address validation
    if (shippingAddress && shippingAddress.value.trim() === '') {
        errors.push('Shipping address is required');
        isValid = false;
    }

    // Contact number validation
    if (contactNumber && contactNumber.value.trim() === '') {
        errors.push('Contact number is required');
        isValid = false;
    }

    if (!isValid) {
        errors.forEach(error => {
            console.error(error);
        });
    }

    return isValid;
}

// ============================================
// 3. DELETE CONFIRMATION
// ============================================

function confirmDelete(orderId) {
    if (confirm(`Are you sure you want to delete order ${orderId}? This action cannot be undone.`)) {
        return true;
    }
    return false;
}

// ============================================
// 4. DATE HELPERS
// ============================================

function setTodayDate(elementId) {
    const today = new Date().toISOString().split('T')[0];
    const element = document.getElementById(elementId);
    if (element) {
        element.value = today;
    }
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// ============================================
// 5. CURRENCY FORMATTING
// ============================================

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function updateTotal() {
    const quantityInput = document.getElementById('quantity');
    const priceInput = document.getElementById('price');
    const totalDisplay = document.getElementById('total');

    if (quantityInput && priceInput && totalDisplay) {
        const quantity = parseFloat(quantityInput.value) || 0;
        const price = parseFloat(priceInput.value) || 0;
        const total = quantity * price;
        totalDisplay.textContent = formatCurrency(total);
    }
}

// ============================================
// 6. SEARCH FUNCTIONALITY
// ============================================

function performSearch(event) {
    event.preventDefault();
    
    const searchType = document.getElementById('search_type').value;
    const searchTerm = document.getElementById('search_term').value.trim();

    if (!searchType) {
        alert('Please select a search type');
        return false;
    }

    if (!searchTerm) {
        alert('Please enter a search term');
        return false;
    }

    return true;
}

// ============================================
// 7. EXPORT FUNCTIONALITY
// ============================================

function exportToExcel(exportType) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/export/excel';

    const typeInput = document.createElement('input');
    typeInput.type = 'hidden';
    typeInput.name = 'export_type';
    typeInput.value = exportType;
    form.appendChild(typeInput);

    // Add date range if available
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');

    if (startDate && startDate.value) {
        const startInput = document.createElement('input');
        startInput.type = 'hidden';
        startInput.name = 'start_date';
        startInput.value = startDate.value;
        form.appendChild(startInput);
    }

    if (endDate && endDate.value) {
        const endInput = document.createElement('input');
        endInput.type = 'hidden';
        endInput.name = 'end_date';
        endInput.value = endDate.value;
        form.appendChild(endInput);
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function exportToCSV(exportType) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/export/csv';

    const typeInput = document.createElement('input');
    typeInput.type = 'hidden';
    typeInput.name = 'export_type';
    typeInput.value = exportType;
    form.appendChild(typeInput);

    // Add date range if available
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');

    if (startDate && startDate.value) {
        const startInput = document.createElement('input');
        startInput.type = 'hidden';
        startInput.name = 'start_date';
        startInput.value = startDate.value;
        form.appendChild(startInput);
    }

    if (endDate && endDate.value) {
        const endInput = document.createElement('input');
        endInput.type = 'hidden';
        endInput.name = 'end_date';
        endInput.value = endDate.value;
        form.appendChild(endInput);
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

// ============================================
// 8. STATUS UPDATE VIA AJAX
// ============================================

function updateOrderStatus(orderId) {
    const statusSelect = document.getElementById('newStatus');
    const newStatus = statusSelect.value;

    if (!newStatus) {
        alert('Please select a status');
        return;
    }

    const formData = new FormData();
    formData.append('status', newStatus);

    fetch(`/orders/${orderId}/update-status`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the status');
    });
}

// ============================================
// 9. TABLE SORTING
// ============================================

function sortTable(columnIndex) {
    const table = document.querySelector('table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        // Try to convert to numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }

        return aValue.localeCompare(bValue);
    });

    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}

// ============================================
// 10. PAGINATION
// ============================================

function goToPage(pageNumber) {
    const url = new URL(window.location);
    url.searchParams.set('page', pageNumber);
    window.location.href = url.toString();
}

// ============================================
// 11. MODAL/DIALOG FUNCTIONALITY
// ============================================

function showModal(title, message) {
    if (confirm(title + '\n\n' + message)) {
        return true;
    }
    return false;
}

// ============================================
// 12. EVENT LISTENERS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to all quantity and price inputs
    const quantityInputs = document.querySelectorAll('#quantity, #price');
    quantityInputs.forEach(input => {
        input.addEventListener('change', updateTotal);
        input.addEventListener('keyup', updateTotal);
    });

    // Form submission validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Only validate order forms, not search forms
            if (this.id !== 'statusForm' && this.action.includes('/orders/add')) {
                if (!validateOrderForm()) {
                    e.preventDefault();
                }
            }
        });
    });

    // Set today's date for order date field
    if (document.getElementById('order_date') && !document.getElementById('order_date').value) {
        setTodayDate('order_date');
    }

    // Table row click for mobile
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(row => {
        row.style.cursor = 'pointer';
    });
});

// ============================================
// 13. UTILITY FUNCTIONS
// ============================================

function getQueryParam(param) {
    const params = new URLSearchParams(window.location.search);
    return params.get(param);
}

function setQueryParam(param, value) {
    const url = new URL(window.location);
    url.searchParams.set(param, value);
    window.history.pushState({}, '', url);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard: ' + text);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// ============================================
// 14. PRINT FUNCTIONALITY
// ============================================

function printPage() {
    window.print();
}

function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const printWindow = window.open('', '', 'height=400,width=800');
        printWindow.document.write('<html><head><title>Print</title>');
        printWindow.document.write('<link rel="stylesheet" href="' + 
            document.querySelector('link[rel="stylesheet"]').href + '">');
        printWindow.document.write('</head><body>');
        printWindow.document.write(element.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }
}

// ============================================
// 15. KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', function(event) {
    // Ctrl+S to save (for forms)
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    }

    // Escape to go back
    if (event.key === 'Escape') {
        window.history.back();
    }
});

// ============================================
// 16. LOADING STATES
// ============================================

function showLoadingState(buttonElement) {
    if (buttonElement) {
        buttonElement.disabled = true;
        buttonElement.textContent = 'Loading...';
    }
}

function hideLoadingState(buttonElement, originalText) {
    if (buttonElement) {
        buttonElement.disabled = false;
        buttonElement.textContent = originalText;
    }
}

// ============================================
// 17. NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'success', duration = 5000) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.maxWidth = '400px';

    document.body.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, duration);
}

// ============================================
// 18. DARK MODE TOGGLE (OPTIONAL)
// ============================================

function toggleDarkMode() {
    const body = document.body;
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'false');
    } else {
        body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'true');
    }
}

// Load dark mode preference on page load
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
});