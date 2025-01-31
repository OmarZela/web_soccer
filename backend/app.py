from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Modelo de la base de datos
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

# Ruta para agregar jugador
@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    name = data.get('name')
    position = data.get('position')

    # Verificar si la posición está ocupada
    existing_player = Player.query.filter_by(position=position, confirmed=True).first()
    if existing_player:
        return jsonify({"error": "La posición ya está ocupada."}), 400

    # Crear nuevo jugador
    new_player = Player(name=name, position=position)
    db.session.add(new_player)
    db.session.commit()

    # Enviar mensaje de WhatsApp (usar Twilio API)
    send_whatsapp_message(name, position)

    return jsonify({"message": "Jugador agregado. Esperando confirmación."}), 200

# Ruta para confirmar asistencia
@app.route('/confirm', methods=['POST'])
def confirm():
    data = request.json
    player_id = data.get('player_id')
    player = Player.query.get(player_id)

    if player:
        player.confirmed = True
        db.session.commit()
        socketio.emit('update_lineup', {'player': player.name, 'position': player.position})
        return jsonify({"message": "Confirmación exitosa."}), 200
    else:
        return jsonify({"error": "Jugador no encontrado."}), 404

# Función para enviar mensaje de WhatsApp (usar Twilio)
def send_whatsapp_message(name, position):
    # Lógica para enviar mensaje usando Twilio API
    pass

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)