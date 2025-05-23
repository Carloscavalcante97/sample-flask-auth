from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = 'login'
#Session <- conexão ativa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        #login
        user = User.query.filter_by(username=username).first()
        if user and user.password == password: 
            login_user(user)
            print(f"Usuário {current_user.is_authenticated}")
            return jsonify({"message": "Login realizado com sucesso"})
       
    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

@app.route('/user', methods=['POST'])
@login_required
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso"}), 201
    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username}), 200
    return jsonify({"message": "Usuário não encontrado"}), 404


@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    data = request.json
    if user and data.get('password'):   
        user.password = data.get('password')    
        db.session.commit()
        return jsonify({"message": f"Usuário {user.username} atualizado com sucesso"}), 200
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if  user.id == current_user.id:
        return jsonify({"message": "Você não pode deletar sua própria conta"}), 403
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user.username} deletado com sucesso"}), 200
    return jsonify({"message": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)