from fastapi import APIRouter
from src.app.auth.api import auth_router
from src.app.user.endpoint import users, admin
from src.app.board.endpoint import category, toolkit, project, task
from src.app.company.endpoint import company, vacancy

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=["login"])
api_router.include_router(users.user_router, prefix='/user', tags=["user"])
api_router.include_router(category.category_router, prefix='/board/category', tags=["board"])
api_router.include_router(toolkit.toolkit_router, prefix='/board/toolkit', tags=["board"])
api_router.include_router(project.project_router, prefix='/board/project', tags=["board"])
api_router.include_router(task.task_router, prefix='/board/task', tags=["board"])
api_router.include_router(company.company_router, prefix='/company', tags=["company"])
api_router.include_router(vacancy.vacancy_router, prefix='/vacancy', tags=["company"])

api_router.include_router(admin.admin_router, prefix='/admin/user', tags=["admin"])
