document.addEventListener('DOMContentLoaded', function() {
    let userId;

    fetchCurrentUserId();

    function fetchCurrentUserId() {
        fetch("/api/current_user")
            .then(response => response.json())
            .then(data => {
                if (data.user_id) {
                    userId = data.user_id;
                    console.log("User ID set:", userId);
                } else {
                    console.error("User not logged in");
                }
            })
            .catch(error => {
                console.error("Error fetching user ID:", error);
            });
    }

    function fetchStores() {
        fetch('/api/stores')
            .then(response => response.json())
            .then(stores => {
                displayStores(stores);
            })
            .catch(error => console.error('Error fetching stores:', error));
    }

    function displayStores(stores) {
        const storeList = document.getElementById('storeList');
        if (storeList) {
            storeList.innerHTML = '';
            stores.forEach(store => {
                const storeDiv = document.createElement('div');
                storeDiv.className = 'store-item';
                storeDiv.dataset.storeId = store.id;
                storeDiv.innerHTML = `
                    <h3>${store.name}</h3>
                    <p>Location: ${store.location}</p>
                    <button class="view-items-btn">View Items</button>
                `;
                storeList.appendChild(storeDiv);
            });

            document.querySelectorAll('.view-items-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const storeId = this.parentElement.dataset.storeId;
                    fetchItemsByStore(storeId);
                });
            });
        } else {
            console.error('Store list element not found.');
        }
    }

    function fetchItemsByStore(storeId) {
        fetch(`/api/store/${storeId}/items`)
            .then(response => response.json())
            .then(items => {
                displayItems(items);
            })
            .catch(error => console.error('Error fetching items:', error));
    }

    function displayItems(items) {
        const itemList = document.getElementById('itemList');
        if (itemList) {
            itemList.innerHTML = '';
            items.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'item';
                itemDiv.dataset.itemId = item.id;
                itemDiv.innerHTML = `
                    <h4>${item.name}</h4>
                    <p>Brand: ${item.brand}</p>
                    <p>Price: ${item.price}</p>
                    <p>Sale Status: ${item.sale_status}</p>
                    <button class="add-to-cart-btn">Add to Shopping List</button>
                `;
                itemList.appendChild(itemDiv);
            });

            document.querySelectorAll('.add-to-cart-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemId = this.parentElement.dataset.itemId;
                    console.log('Adding item to shopping list:', itemId);
                    addItemToShoppingList(itemId);
                });
            });
        } else {
            console.error('Item list element not found.');
        }
    }

    function addItemToShoppingList(itemId) {
        const parsedItemId = parseInt(itemId);
        if (!isNaN(parsedItemId)) {
            console.log('Adding item to shopping list:', { user_id: userId, item_id: parsedItemId });
            fetch("/api/shoppinglist", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, item_id: parsedItemId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log('Item added to shopping list:', data.message);
                    updateShoppingListDisplay();
                } else {
                    console.error('Error adding item to shopping list:', data.error);
                }
            })
            .catch(error => console.error('Error adding item to shopping list:', error));
        } else {
            console.error('Invalid item ID:', itemId);
        }
    }

    function removeItemFromShoppingList(itemId) {
        const parsedItemId = parseInt(itemId);
        if (!isNaN(parsedItemId)) {
            fetch(`/api/shoppinglist/${userId}/remove/${parsedItemId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log("Item removed successfully");
                    updateShoppingListDisplay();
                } else {
                    console.error("Error removing item:", data.error);
                }
            })
            .catch(error => {
                console.error("Error removing item:", error);
            });
        } else {
            console.error('Invalid item ID:', itemId);
        }
    }

    function updateShoppingListDisplay() {
        fetch(`/api/shoppinglist/${userId}`)
            .then(response => response.json())
            .then(shoppingList => {
                displayShoppingList(shoppingList);
            })
            .catch(error => console.error('Error updating shopping list:', error));
    }

    function displayShoppingList(shoppingList) {
        const shoppingListDiv = document.getElementById('shoppingList');
        if (shoppingListDiv) {
            shoppingListDiv.innerHTML = '';
            shoppingList.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'shopping-list-item';
                itemDiv.innerHTML = `
                    <h3>${item.name}</h3>
                    <p>Brand: ${item.brand}</p>
                    <p>Price: ${item.price}</p>
                    <p>Sale Status: ${item.sale_status}</p>
                    <button class="remove-from-cart-btn" data-item-id="${item.id}">Remove Item</button>
                `;
                shoppingListDiv.appendChild(itemDiv);
            });

            document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemId = this.dataset.itemId;
                    removeItemFromShoppingList(itemId);
                });
            });
        } else {
            console.error('Shopping list element not found.');
        }
    }

    document.getElementById('loadStoresButton').addEventListener('click', function() {
        fetchStores();
    });
});
