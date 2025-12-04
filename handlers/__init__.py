from aiogram import Router
from .admin_commands import router as admin_commands_router
from .user_panel import router as user_panel_router
# from .admin_obrabotka import router as admin_obrabotka_router

router = Router()
router.include_router(admin_commands_router)
router.include_router(user_panel_router)
# router.include_router(admin_obrabotka_router)