async function sendName() {
    const name = document.getElementById('nameInput').value;
    if (!name) {
        document.getElementById('result').innerText = '请输入名字！';
        return;
    }
    try {
        const response = await fetch('/greet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name }),
        });
        const data = await response.json();
        document.getElementById('result').innerText = data.message;
        document.getElementById('nameInput').value = '';
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        document.getElementById('result').innerText = '发生错误，请稍后再试！';
    }
}

async function uploadAvatar() {
    const name = document.getElementById('nameInput').value;
    const avatarInput = document.getElementById('avatarInput');
    const file = avatarInput.files[0];

    if (!name) {
        document.getElementById('result').innerText = '请输入名字！';
        return;
    }
    if (!file) {
        document.getElementById('result').innerText = '请选择头像文件！';
        return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('avatar', file);

    try {
        const response = await fetch('/upload-avatar', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        document.getElementById('result').innerText = data.message;
        document.getElementById('nameInput').value = '';
        avatarInput.value = '';
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        document.getElementById('result').innerText = '发生错误，请稍后再试！';
    }
}