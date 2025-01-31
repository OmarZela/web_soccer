const socket = io();

// Actualizar la alineación en tiempo real
socket.on('update_lineup', (data) => {
    const field = document.getElementById('field');
    const playerElement = document.createElement('div');
    playerElement.className = 'player';
    playerElement.textContent = `${data.player} (${data.position})`;
    field.appendChild(playerElement);
});