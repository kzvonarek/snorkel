"""
API路由模块
"""

from flask import Blueprint

simulation_bp = Blueprint('simulation', __name__)
report_bp = Blueprint('report', __name__)
projects_bp = Blueprint('projects', __name__)

from . import simulation  # noqa: E402, F401
from . import report  # noqa: E402, F401
from . import projects  # noqa: E402, F401

