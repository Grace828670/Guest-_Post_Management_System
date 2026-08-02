// ================= ADD CLIENT =================

document.getElementById("addClient").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/add-client`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            full_name: document.getElementById("full_name").value,
            email: document.getElementById("email").value,
            company_name: document.getElementById("company_name").value,
            phone: document.getElementById("phone").value
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
    });

});

// ================= LOAD CLIENTS =================

document.getElementById("loadClients").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/clients`)

    .then(response => response.json())

    .then(data => {

        let output = "";

        data.forEach(client => {

            output += `
            <tr>
                <td>${client.client_id}</td>
                <td>${client.full_name}</td>
                <td>${client.email}</td>
                <td>${client.company_name}</td>
                <td>${client.phone}</td>

                <td>
                    <button onclick="editClient(${client.client_id})">
                        ✏️ Edit
                    </button>

                    <button onclick="deleteClient(${client.client_id})">
                        🗑 Delete
                    </button>
                </td>
            </tr>
            `;

        });

        document.getElementById("output").innerHTML = output;

    });

});
// ================= LOAD CLIENTS =================

/// ================= LOAD PAYMENTS =================

document.getElementById("loadPayments").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/payments`)

    .then(response => response.json())

    .then(data => {

        let output = "";

        data.forEach(payment => {

            output += `
            <tr>
                <td>${payment.payment_id}</td>
                <td>${payment.client_id}</td>
                <td>${payment.amount}</td>
                <td>${payment.payment_status}</td>
                <td>${payment.payment_date}</td>

                <td>
                    <button onclick="editPayment(${payment.payment_id})">
                        ✏️ Edit
                    </button>

                    <button onclick="deletePayment(${payment.payment_id})">
                        🗑 Delete
                    </button>
                </td>

            </tr>
            `;

        });

        document.getElementById("paymentOutput").innerHTML = output;

    });

});
// ================= ADD ORDER =================

document.getElementById("addOrder").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/add-order`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            client_id: document.getElementById("client_id").value,
            target_link: document.getElementById("target_link").value,
            anchor_text: document.getElementById("anchor_text").value,
            price: document.getElementById("price").value,
            status: document.getElementById("status").value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message || data.error);

    });

});


// ================= UPDATE CLIENT =================

document.getElementById("updateClient").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/update-client`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            client_id: document.getElementById("update_client_id").value,
            full_name: document.getElementById("update_full_name").value,
            email: document.getElementById("update_email").value,
            company_name: document.getElementById("update_company_name").value,
            phone: document.getElementById("update_phone").value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message || data.error);

    });

});
// ================= DELETE CLIENT =================

document.getElementById("deleteClient").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/delete-client`, {

        method: "DELETE",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            client_id: document.getElementById("delete_client_id").value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message || data.error);

    });

});
// ================= ADD PAYMENT =================

document.getElementById("addPayment").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/add-payment`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            client_id: document.getElementById("payment_client_id").value,
            amount: document.getElementById("payment_amount").value,
            payment_status: document.getElementById("payment_status").value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message || data.error);

    });

});




// ================= DASHBOARD =================

function loadDashboard() {

    fetch(`${API_BASE_URL}/dashboard`)

    .then(response => response.json())

    .then(data => {

        document.getElementById("totalClients").innerHTML = data.total_clients;
        document.getElementById("totalOrders").innerHTML = data.total_orders;
        document.getElementById("totalPayments").innerHTML = data.total_payments;
        document.getElementById("totalRevenue").innerHTML = data.total_revenue;

    });

}

loadDashboard();
// ================= SEARCH CLIENT =================

document.getElementById("searchClient").addEventListener("keyup", function () {

    let searchValue = this.value.toLowerCase();

    let rows = document.querySelectorAll("#output tr");

    rows.forEach(row => {

        let rowText = row.innerText.toLowerCase();

        if(rowText.includes(searchValue)) {
            row.style.display = "";
        }
        else {
            row.style.display = "none";
        }

    });

});
// ================= DELETE FROM TABLE =================

function deleteClient(client_id) {

    let confirmDelete = confirm("Are you sure you want to delete this client?");

    if(confirmDelete){

        fetch(`${API_BASE_URL}/delete-client`, {

            method: "DELETE",

            headers:{
                "Content-Type":"application/json"
            },

            body: JSON.stringify({
                client_id: client_id
            })

        })

        .then(response => response.json())

        .then(data => {

            alert(data.message || data.error);

            location.reload();

        });

    }

}
// ================= EDIT CLIENT =================

function editClient(client_id) {

    fetch(`${API_BASE_URL}/clients`)

    .then(response => response.json())

    .then(data => {

        let client = data.find(c => c.client_id == client_id);

        if(client){

            document.getElementById("update_client_id").value = client.client_id;

            document.getElementById("update_full_name").value = client.full_name;

            document.getElementById("update_email").value = client.email;

            document.getElementById("update_company_name").value = client.company_name;

            document.getElementById("update_phone").value = client.phone;


            alert("Client data loaded. Now update and save.");

        }

    });

}
// ================= LOAD ORDERS =================

document.getElementById("loadOrders").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/orders`)

    .then(response => response.json())

    .then(data => {

        let output = "";

        data.forEach(order => {

            output += `
            <tr>
                <td>${order.order_id}</td>
                <td>${order.client_id}</td>
                <td>${order.target_link}</td>
                <td>${order.anchor_text}</td>
                <td>${order.price}</td>
                <td>${order.status}</td>
                <td>
    <button onclick="editOrder(${order.order_id})">
        ✏️ Edit
    </button>

    <button onclick="deleteOrder(${order.order_id})">
        🗑 Delete
    </button>
</td>
            </tr>
            `;

        });

        document.getElementById("orderOutput").innerHTML = output;

    });

});
// ================= SEARCH ORDERS =================

document.getElementById("searchOrder").addEventListener("keyup", function () {

    let searchValue = this.value.toLowerCase();

    let rows = document.querySelectorAll("#orderOutput tr");

    rows.forEach(row => {

        let rowText = row.innerText.toLowerCase();

        if(rowText.includes(searchValue)) {
            row.style.display = "";
        }
        else {
            row.style.display = "none";
        }

    });

}); 
// ================= DELETE ORDER =================

function deleteOrder(order_id) {

    let confirmDelete = confirm("Delete this order?");

    if(confirmDelete){

        fetch(`${API_BASE_URL}/delete-order`, {

            method: "DELETE",

            headers:{
                "Content-Type":"application/json"
            },

            body: JSON.stringify({
                order_id: order_id
            })

        })

        .then(response => response.json())

        .then(data => {

            alert(data.message || data.error);

            location.reload();

        });

    }

}
// ================= EDIT ORDER =================

function editOrder(order_id) {

    fetch(`${API_BASE_URL}/orders`)

    .then(response => response.json())

    .then(data => {

        let order = data.find(o => o.order_id == order_id);

        if(order){

            document.getElementById("update_order_id").value = order.order_id;

            document.getElementById("update_target_link").value = order.target_link;

            document.getElementById("update_anchor_text").value = order.anchor_text;

            document.getElementById("update_price").value = order.price;

            document.getElementById("update_status").value = order.status;


            alert("Order data loaded. Now update and save.");

        }

    });

}
// ================= UPDATE ORDER =================

document.getElementById("updateOrder").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/update-order`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            order_id: document.getElementById("update_order_id").value,
            target_link: document.getElementById("update_target_link").value,
            anchor_text: document.getElementById("update_anchor_text").value,
            price: document.getElementById("update_price").value,
            status: document.getElementById("update_status").value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message || data.error);

        location.reload();

    });

});
// ================= SEARCH CLIENT =================

document.getElementById("searchClientBtn").addEventListener("click", function () {

    const keyword = document.getElementById("searchClient").value;

    fetch(`${API_BASE_URL}/search-client/${keyword}`)
        .then(response => response.json())
        .then(data => {

            let output = "";

            data.forEach(client => {

                output += `
                    <tr>
                        <td>${client.client_id}</td>
                        <td>${client.full_name}</td>
                        <td>${client.email}</td>
                        <td>${client.company_name}</td>
                        <td>${client.phone}</td>

                        <td>
                            <button onclick="editClient(${client.client_id},
                            '${client.full_name}',
                            '${client.email}',
                            '${client.company_name}',
                            '${client.phone}')">
                            Edit
                            </button>

                            <button onclick="deleteClient(${client.client_id})">
                            Delete
                            </button>
                        </td>
                    </tr>
                `;
            });

            document.getElementById("output").innerHTML = output;

        });

});
// ================= SEARCH ORDER =================

document.getElementById("searchOrderBtn").addEventListener("click", function () {

    const keyword = document.getElementById("searchOrder").value;

    fetch(`${API_BASE_URL}/search-order/${keyword}`)
        .then(response => response.json())
        .then(data => {

            let output = "";

            data.forEach(order => {

                output += `
                    <tr>
                        <td>${order.order_id}</td>
                        <td>${order.client_id}</td>
                        <td>${order.target_link}</td>
                        <td>${order.anchor_text}</td>
                        <td>${order.price}</td>
                        <td>${order.status}</td>

                        <td>
                            <button onclick="editOrder(${order.order_id})">
                                Edit
                            </button>

                            <button onclick="deleteOrder(${order.order_id})">
                                Delete
                            </button>
                        </td>
                    </tr>
                `;
            });

            document.getElementById("orderOutput").innerHTML = output;

        });

});
// ================= SEARCH PAYMENT =================

document.getElementById("searchPaymentBtn").addEventListener("click", function () {

    const keyword = document.getElementById("searchPayment").value;

    fetch(`${API_BASE_URL}/search-payment/${keyword}`)
        .then(response => response.json())
        .then(data => {

            let output = "";

            data.forEach(payment => {

                output += `
                    <tr>
                        <td>${payment.payment_id}</td>
                        <td>${payment.client_id}</td>
                        <td>${payment.amount}</td>
                        <td>${payment.payment_status}</td>
                        <td>${payment.payment_date}</td>
                        <td>
                            <button onclick="editPayment(${payment.payment_id})">Edit</button>

                            <button onclick="deletePayment(${payment.payment_id})">Delete</button>
                        </td>
                    </tr>
                `;
            });

            document.getElementById("paymentOutput").innerHTML = output;

        });

});
// ================= DELETE PAYMENT =================

function deletePayment(payment_id) {

    if (!confirm("Are you sure you want to delete this payment?")) {
        return;
    }

    fetch(`${API_BASE_URL}/delete-payment`, {

        method: "DELETE",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            payment_id: payment_id
        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        document.getElementById("loadPayments").click();

    });

}
// ================= EDIT PAYMENT =================

function editPayment(payment_id) {

    fetch(`${API_BASE_URL}/payments`)

    .then(response => response.json())

    .then(data => {

        let payment = data.find(p => p.payment_id == payment_id);

        if(payment){

            document.getElementById("payment_client_id").value = payment.client_id;

            document.getElementById("payment_amount").value = payment.amount;

            document.getElementById("payment_status").value = payment.payment_status;

            document.getElementById("payment_id").value = payment.payment_id;

            alert("Payment data loaded. Now update and save.");

        }

    });

}
// ================= UPDATE PAYMENT =================

document.getElementById("updatePayment").addEventListener("click", function () {

    fetch(`${API_BASE_URL}/update-payment`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            payment_id: document.getElementById("payment_id").value,
            amount: document.getElementById("payment_amount").value,
            payment_status: document.getElementById("payment_status").value

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message || data.error);

        location.reload();

    });

});