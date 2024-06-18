document.addEventListener('DOMContentLoaded', () => {
    const userList = document.getElementById('user-list');
    const roleList = document.getElementById('role-list');
    const createUserForm = document.getElementById('create-user-form');
    const createRoleForm = document.getElementById('create-role-form');

    async function fetchUsers() {
        try {
            const response = await fetch('/api/users');
            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }
            const users = await response.json();
            displayUsers(users);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }

    function displayUsers(users) {
        userList.innerHTML = '';
        users.forEach(user => {
            const userElement = document.createElement('div');
            userElement.classList.add('user');
            userElement.innerHTML = `<strong>${user.username}</strong>`;
            userList.appendChild(userElement);
        });
    }

    async function fetchRoles() {
        try {
            const response = await fetch('/api/roles');
            if (!response.ok) {
                throw new Error('Failed to fetch roles');
            }
            const roles = await response.json();
            displayRoles(roles);
        } catch (error) {
            console.error('Error fetching roles:', error);
        }
    }

    function displayRoles(roles) {
        roleList.innerHTML = '';
        roles.forEach(role => {
            const roleElement = document.createElement('div');
            roleElement.classList.add('role');
            roleElement.textContent = role.name;
            roleList.appendChild(roleElement);
        });
    }

    createUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            if (!response.ok) {
                throw new Error('Failed to create user');
            }
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
            fetchUsers();
        } catch (error) {
            console.error('Error creating user:', error);
        }
    });

    createRoleForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const roleName = document.getElementById('role-name').value;

        try {
            const response = await fetch('/api/roles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: roleName, permissions: [] })
            });
            if (!response.ok) {
                throw new Error('Failed to create role');
            }
            document.getElementById('role-name').value = '';
            fetchRoles();
        } catch (error) {
            console.error('Error creating role:', error);
        }
    });

    fetchUsers();
    fetchRoles();
});
