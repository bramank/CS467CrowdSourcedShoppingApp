document.addEventListener('DOMContentLoaded', function() {
    fetchCurrentUserId();

    function fetchCurrentUserId() {
        fetch("/api/current_user")
            .then(response => response.json())
            .then(data => {
                if (data.user_id) {
                    userId = data.user_id;
                    console.log("User ID set:", userId);
                    fetchUserInfo(userId);
                    fetchActivityLog(userId);
                } else {
                    console.error("User not logged in");
                }
            })
            .catch(error => console.error("Error fetching user ID:", error));
    }

    function fetchUserInfo(userId) {
        fetch(`/api/users/${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.email) {
                    document.getElementById('email').textContent = data.email;
                    document.getElementById('reputation').textContent = data.reputation;
                    document.getElementById('badge').textContent = data.badge;
                } else {
                    console.error('Error fetching user info:', data.error);
                }
            })
            .catch(error => console.error('Error fetching user info:', error));
    }

    function fetchActivityLog(userId) {
        fetch(`/api/activitylogs/user/${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.activities && data.activities.length > 0) {
                    displayActivityLog(data.activities);
                } else {
                    displayNoActivityMessage();
                }
            })
            .catch(error => console.error('Error fetching activity log:', error));
    }

    function displayActivityLog(logs) {
        const activityLog = document.getElementById('activityLog');
        if (activityLog) {
            activityLog.innerHTML = '';
            logs.forEach(activity => {
                const activityItem = document.createElement('div');
                activityItem.textContent = activity.details;
                activityLog.appendChild(activityItem);
            });
        } else {
            console.error('Activity log element not found.');
        }
    }

    function displayNoActivityMessage() {
        const activityLog = document.getElementById('activityLog');
        if (activityLog) {
            activityLog.innerHTML = '';
            const noActivityMessage = document.createElement('div');
            noActivityMessage.textContent = 'No Activity On Record';
            activityLog.appendChild(noActivityMessage);
        } else {
            console.error('Activity log element not found.');
        }
    }

    const changePasswordForm = document.getElementById('changePasswordForm');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const oldPassword = document.getElementById('oldPassword').value;
            const newPassword = document.getElementById('newPassword').value;

            fetch('/api/changepassword', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
            })
            .then(response => response.json())
            .then(data => {
                const passwordChangeResult = document.getElementById('passwordChangeResult');
                if (data.message) {
                    passwordChangeResult.textContent = data.message;
                } else {
                    passwordChangeResult.textContent = `Error: ${data.error}`;
                }
            })
            .catch(error => console.error('Error changing password:', error));
        });
    }
});
