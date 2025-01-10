"""Импорты router-ов для главного router-а."""
__all__ = ['charity_project_router', 'donation_router', 'user_router']

from .charity_project import router as charity_project_router
from .donation import router as donation_router
from .user import router as user_router
