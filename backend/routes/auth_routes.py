"""
Rutas de autenticacion (login, register, logout)
"""

from flask import Blueprint, jsonify, request, session
from backend.config.database import db
from backend.models.user import User
from flask_bcrypt import Bcrypt
import jwt
import os
from datetime import datetime, timedelta
import logging

# Configurar logging
logger = logging.getLogger(__name__)

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
bcrypt = Bcrypt()

# Rastreador de intentos fallidos (en producción usar Redis)
failed_login_attempts = {}


def track_failed_login(username):
    """Rastrear intentos de login fallidos por seguridad"""
    if username not in failed_login_attempts:
        failed_login_attempts[username] = {"count": 0, "timestamp": datetime.utcnow()}
    
    attempts = failed_login_attempts[username]
    # Reset si pasó más de 15 minutos
    if (datetime.utcnow() - attempts["timestamp"]).seconds > 900:
        failed_login_attempts[username] = {"count": 0, "timestamp": datetime.utcnow()}
    
    attempts["count"] += 1
    return attempts["count"]


def is_account_locked(username):
    """Verificar si la cuenta está temporalmente bloqueada"""
    if username in failed_login_attempts:
        attempts = failed_login_attempts[username]
        if attempts["count"] >= 5:
            return (datetime.utcnow() - attempts["timestamp"]).seconds < 900
    return False


@bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/auth/login
    Autenticar usuario
    Body: { "username": "admin", "password": "admin123" }
    """
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    username = data["username"]
    
    # Verificar si la cuenta está bloqueada por intentos fallidos
    if is_account_locked(username):
        logger.warning(f"Intento de login a cuenta bloqueada: {username}")
        return jsonify({"error": "Cuenta temporalmente bloqueada. Intente en 15 minutos"}), 429

    # Buscar usuario
    user = User.query.filter_by(username=username).first()

    if not user:
        attempt_count = track_failed_login(username)
        logger.warning(f"Intento de login fallido para usuario no existente: {username} (intento {attempt_count})")
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    # Verificar contraseña
    if not bcrypt.check_password_hash(user.password_hash, data["password"]):
        attempt_count = track_failed_login(username)
        logger.warning(f"Intento de login fallido para {username} - contraseña incorrecta (intento {attempt_count})")
        if attempt_count >= 5:
            return jsonify({"error": "Demasiados intentos fallidos. Cuenta bloqueada 15 minutos"}), 429
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    if user.status != "ACTIVO":
        logger.warning(f"Intento de login con usuario inactivo: {username}")
        return jsonify({"error": "Usuario inactivo"}), 403

    # Limpiar intentos fallidos al login exitoso
    if username in failed_login_attempts:
        del failed_login_attempts[username]

    # Actualizar ultimo login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    logger.info(f"Login exitoso para usuario: {username}")

    # Generar token JWT
    token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=24),
        },
        os.getenv("SECRET_KEY", "dev-secret-key"),
        algorithm="HS256",
    )

    return (
        jsonify({"message": "Login exitoso", "token": token, "user": user.to_dict()}),
        200,
    )


@bp.route("/create-user", methods=["POST"])
def create_user():
    """
    POST /api/auth/create-user
    Crear nuevo usuario (solo ADMIN puede hacerlo)
    Header: Authorization: Bearer <token>
    """
    # Verificar token y que sea admin
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "No autorizado"}), 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY", "dev-secret-key"), algorithms=["HS256"]
        )

        if payload["role"] != "ADMIN":
            return jsonify({"error": "Solo administradores pueden crear usuarios"}), 403

    except:
        return jsonify({"error": "Token invalido"}), 401

    data = request.get_json()

    # Validaciones
    required_fields = ["username", "email", "password", "full_name"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"El campo {field} es requerido"}), 400

    # Verificar si ya existe
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "El nombre de usuario ya existe"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    # Crear usuario
    password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=password_hash,
        full_name=data["full_name"],
        role=data.get("role", "USER"),  # Admin puede asignar rol
    )

    try:
        db.session.add(user)
        db.session.commit()
        return (
            jsonify({"message": "Usuario creado exitosamente", "user": user.to_dict()}),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/verify", methods=["GET"])
def verify_token():
    """
    GET /api/auth/verify
    Verificar si el token es valido
    Header: Authorization: Bearer <token>
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Token no proporcionado"}), 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY", "dev-secret-key"), algorithms=["HS256"]
        )

        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"valid": True, "user": user.to_dict()}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalido"}), 401
