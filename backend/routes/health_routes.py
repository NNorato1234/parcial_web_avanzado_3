"""
Rutas de salud del sistema (health check)
Equivalente a un @RestController en Spring
"""

from flask import Blueprint, jsonify
from backend.config.database import test_connection, db
from backend.models.article import Article
from backend.models.user import User
from backend.models.report import Report
from datetime import datetime, timedelta
import os

# Blueprint = agrupación de rutas (como @RequestMapping en Spring)
bp = Blueprint("health", __name__, url_prefix="/api/health")


@bp.route("/", methods=["GET"])
def health_check():
    """
    GET /api/health/
    Verifica que la API esté funcionando
    """
    return (
        jsonify(
            {
                "status": "OK",
                "message": "API funcionando correctamente",
                "service": "Sistema de Inventario Petrolera",
                "version": "1.0.0",
                "timestamp": datetime.utcnow().isoformat()
            }
        ),
        200,
    )


@bp.route("/db", methods=["GET"])
def database_check():
    """
    GET /api/health/db
    Verifica la conexión a la base de datos y obtiene estadísticas
    """
    success, message = test_connection()
    
    stats = {}
    if success:
        try:
            stats = {
                "total_articles": Article.query.count(),
                "total_users": User.query.count(),
                "total_reports": Report.query.count(),
                "active_users": User.query.filter_by(status="ACTIVO").count()
            }
        except Exception as e:
            stats = {"error": str(e)}

    return jsonify(
        {
            "status": "OK" if success else "ERROR",
            "database": "MySQL",
            "message": message,
            "statistics": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    ), (200 if success else 500)


@bp.route("/detailed", methods=["GET"])
def detailed_health_check():
    """
    GET /api/health/detailed
    Verifica la salud detallada de todos los componentes
    """
    db_success, db_message = test_connection()
    
    detailed_stats = {
        "environment": os.getenv("FLASK_ENV", "development"),
        "database": {
            "connected": db_success,
            "message": db_message
        },
        "entities": {
            "articles": 0,
            "users": 0,
            "reports": 0,
            "recent_activity_24h": 0
        },
        "health_status": "HEALTHY" if db_success else "UNHEALTHY"
    }
    
    if db_success:
        try:
            now = datetime.utcnow()
            yesterday = now - timedelta(days=1)
            
            detailed_stats["entities"]["articles"] = Article.query.count()
            detailed_stats["entities"]["users"] = User.query.count()
            detailed_stats["entities"]["reports"] = Report.query.count()
            detailed_stats["entities"]["recent_activity_24h"] = Report.query.filter(
                Report.created_at >= yesterday
            ).count()
        except Exception as e:
            detailed_stats["health_status"] = "DEGRADED"
            detailed_stats["error"] = str(e)
    
    status_code = 200 if detailed_stats["health_status"] == "HEALTHY" else 503
    return jsonify(detailed_stats), status_code
