document.addEventListener('DOMContentLoaded', function () {
    // CREATE USER
    document.getElementById('createUserForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const data = {
            username: event.target.username.value,
            email: event.target.email.value,
            password: event.target.password.value,
            reputation: parseInt(event.target.reputation.value),
            role: event.target.role.value
        };
        fetch('/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('createUserResult').innerText = JSON.stringify(result);
        });
    });

    // READ USER
    document.getElementById('readUserForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const userId = event.target.readUserId.value;
        fetch(`/users/${userId}`)
        .then(response => response.json())
        .then(result => {
            document.getElementById('readUserResult').innerText = JSON.stringify(result);
        });
    });

    // UPDATE USER
    document.getElementById('updateUserForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const userId = event.target.updateUserId.value;
        const data = {
            username: event.target.updateUsername.value,
            email: event.target.updateEmail.value,
            password: event.target.updatePassword.value,
            reputation: event.target.updateReputation.value ? parseInt(event.target.updateReputation.value) : undefined,
            role: event.target.updateRole.value
        };
        fetch(`/users/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('updateUserResult').innerText = JSON.stringify(result);
        });
    });

    // DELETE USER
    document.getElementById('deleteUserForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const userId = event.target.deleteUserId.value;
        fetch(`/users/${userId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('deleteUserResult').innerText = JSON.stringify(result);
        });
    });

    // CREATE ITEM
    document.getElementById('createItemForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const data = {
            name: event.target.name.value,
            tags: event.target.tags.value.split(',').map(tag => tag.trim()),
            brand: event.target.brand.value
        };
        fetch('/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('createItemResult').innerText = JSON.stringify(result);
        });
    });

    // READ ITEM
    document.getElementById('readItemForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const itemId = event.target.readItemId.value;
        fetch(`/items/${itemId}`)
        .then(response => response.json())
        .then(result => {
            document.getElementById('readItemResult').innerText = JSON.stringify(result);
        });
    });

    // UPDATE ITEM
    document.getElementById('updateItemForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const itemId = event.target.updateItemId.value;
        const data = {
            name: event.target.updateItemName.value,
            tags: event.target.updateItemTags.value ? event.target.updateItemTags.value.split(',').map(tag => tag.trim()) : undefined,
            brand: event.target.updateItemBrand.value
        };
        fetch(`/items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('updateItemResult').innerText = JSON.stringify(result);
        });
    });

    // DELETE ITEM
    document.getElementById('deleteItemForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const itemId = event.target.deleteItemId.value;
        fetch(`/items/${itemId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('deleteItemResult').innerText = JSON.stringify(result);
        });
    });

    // CREATE STORE
    document.getElementById('createStoreForm')?.addEventListener('submit', function (event) {
      event.preventDefault();
      const data = {
          name: event.target.name.value,
          location: event.target.location.value,
          latitude: parseFloat(event.target.latitude.value),
          longitude: parseFloat(event.target.longitude.value)
      };
      fetch('/stores', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(result => {
          document.getElementById('createStoreResult').innerText = JSON.stringify(result);
      });
    });

    // READ STORE
    document.getElementById('readStoreForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const storeId = event.target.readStoreId.value;
        fetch(`/stores/${storeId}`)
        .then(response => response.json())
        .then(result => {
            document.getElementById('readStoreResult').innerText = JSON.stringify(result);
        });
    });

    // UPDATE STORE
    document.getElementById('updateStoreForm')?.addEventListener('submit', function (event) {
      event.preventDefault();
      const storeId = event.target.updateStoreId.value;
      const data = {
          name: event.target.updateStoreName.value,
          location: event.target.updateStoreLocation.value,
          latitude: event.target.updateStoreLatitude.value ? parseFloat(event.target.updateStoreLatitude.value) : undefined,
          longitude: event.target.updateStoreLongitude.value ? parseFloat(event.target.updateStoreLongitude.value) : undefined
      };
      fetch(`/stores/${storeId}`, {
          method: 'PUT',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(result => {
          document.getElementById('updateStoreResult').innerText = JSON.stringify(result);
      });
    });

    // DELETE STORE
    document.getElementById('deleteStoreForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const storeId = event.target.deleteStoreId.value;
        fetch(`/stores/${storeId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('deleteStoreResult').innerText = JSON.stringify(result);
        });
    });

    // CREATE SHOPPING LIST
    document.getElementById('createShoppingListForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const data = {
            user_id: event.target.user_id.value,
            items: event.target.items.value.split(',').map(item => item.trim())
        };
        fetch('/shoppinglist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('createShoppingListResult').innerText = JSON.stringify(result);
        });
    });

    // READ SHOPPING LIST
    document.getElementById('readShoppingListForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const shoppingListId = event.target.readShoppingListId.value;
        fetch(`/shoppinglist/${shoppingListId}`)
        .then(response => response.json())
        .then(result => {
            document.getElementById('readShoppingListResult').innerText = JSON.stringify(result);
        });
    });

    // UPDATE SHOPPING LIST
    document.getElementById('updateShoppingListForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const shoppingListId = event.target.updateShoppingListId.value;
        const data = {
            items: event.target.updateShoppingListItems.value.split(',').map(item => item.trim())
        };
        fetch(`/shoppinglist/${shoppingListId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('updateShoppingListResult').innerText = JSON.stringify(result);
        });
    });

    // DELETE SHOPPING LIST
    document.getElementById('deleteShoppingListForm')?.addEventListener('submit', function (event) {
        event.preventDefault();
        const shoppingListId = event.target.deleteShoppingListId.value;
        fetch(`/shoppinglist/${shoppingListId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('deleteShoppingListResult').innerText = JSON.stringify(result);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const createUserForm = document.getElementById('createUserForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                const loginResult = document.getElementById('loginResult');
                loginResult.innerText = data.message;
                if (data.message === "Login successful") {
                    window.location.href = "/";
                }
            });
        });
    }

    if (createUserForm) {
        createUserForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/create_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username: username, email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                const createUserResult = document.getElementById('createUserResult');
                createUserResult.innerText = data.message;
                if (data.message === "User created successfully") {
                    window.location.href = "/login";
                }
            });
        });
    }
});
