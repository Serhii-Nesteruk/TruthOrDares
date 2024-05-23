function getTask(taskType) {
    fetch('/get_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ taskType: taskType })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('task').textContent = data.player + ': ' + data.task;
    })
    .catch(error => console.error('Error:', error));
}
