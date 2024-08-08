document.addEventListener('DOMContentLoaded', function() {
    let userId;

    function fetchCurrentUserId() {
        fetch("/api/current_user")
            .then(response => response.json())
            .then(data => {
                if (data.user_id) {
                    userId = data.user_id;
                    console.log("User ID set:", userId);
                    fetchShoppingList(userId);
                } else {
                    console.error("User not logged in");
                }
            })
            .catch(error => {
                console.error("Error fetching user ID:", error);
            });
    }

    function fetchShoppingList(userId) {
        fetch(`/api/shoppinglist/${userId}`)
            .then(response => response.json())
            .then(shoppingList => {
                console.log('Fetched shopping list:', shoppingList); 
                displayShoppingList(shoppingList);
            })
            .catch(error => console.error('Error fetching shopping list:', error));
    }
    
    function updateShoppingList() {
        fetch(`/api/shoppinglist/${userId}`)
        .then(response => response.json())
        .then(data => {
            const shoppingListContainer = document.getElementById("shoppingList");
            shoppingListContainer.innerHTML = "";
            if (data.error) {
                console.error(data.error);
            } else {
                data.forEach(item => {
                    const itemElement = document.createElement("div");
                    itemElement.className = "shopping-list-item";
                    itemElement.innerHTML = `
                        <h3>${item.name}</h3>
                        <p>Brand: ${item.brand}</p>
                        <p>Price: ${item.price}</p>
                        <p>Sale Status: ${item.sale_status}</p>
                        <button class="btn-primary" onclick="viewItem(${item.id})">View Item</button>
                        <button class="btn-secondary" onclick="removeItemFromShoppingList(${item.id})">Remove Item</button>
                    `;
                    shoppingListContainer.appendChild(itemElement);
                });
            }
        })
        .catch(error => {
            console.error("Error updating shopping list:", error);
        });
    }
    

    function displayShoppingList(shoppingList) {
        const shoppingListDiv = document.getElementById('shoppingList');
        if (shoppingListDiv) {
            shoppingListDiv.innerHTML = '';
            shoppingList.forEach(item => {
                console.log('Item:', item); 
                const itemDiv = document.createElement('div');
                itemDiv.className = 'shopping-list-item';
                itemDiv.dataset.itemId = item.id;
                itemDiv.innerHTML = `
                    <h3>${item.name}</h3>
                    <p>Brand: ${item.brand}</p>
                    <p>Price: ${item.price ? item.price : 'N/A'}</p>
                    <p>Sale Status: ${item.sale_status !== undefined ? item.sale_status : 'N/A'}</p>
                    <button class="btn-primary view-item-btn">View Item</button>
                    <button class="btn-danger remove-item-btn">Remove Item</button>
                `;
                shoppingListDiv.appendChild(itemDiv);
            });

            document.querySelectorAll('.remove-item-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemId = this.parentElement.dataset.itemId;
                    removeItemFromShoppingList(itemId);
                });
            });
        } else {
            console.error('Shopping list element not found.');
        }
    }

    function removeItemFromShoppingList(itemId) {
        fetch(`/api/shoppinglist/${userId}/remove/${itemId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log("Item removed successfully");
                updateShoppingList();
            } else {
                console.error("Error removing item:", data.error);
            }
        })
        .catch(error => {
            console.error("Error removing item:", error);
        });
    }
    

    fetchCurrentUserId();
});
