from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from src.models.api.v1 import ResponseString
from src.models.api.v1.login_history import (
    ResponseLoginHistory,
    ResponseLoginHistoryPaginated,
)
from src.models.api.v1.users_additional import (
    RequestPasswordChange,
)
from src.services.current_user import CurrentUserService, get_current_user
from src.services.login_history import (
    LoginHistoryService,
    get_login_history_service,
)
from src.services.user import UserService, get_user_service
from src.utils.pagination import Paginator, get_paginator
from src.validators.user import (
    UserValidator,
    get_user_validator,
    user_uuid_annotation,
)

router = APIRouter()


@router.get(
    "/{user_uuid}/history/",
    response_model=ResponseLoginHistoryPaginated,
    summary="Get user activity history",
)
async def get_user_history(
        request: Request,
        user_uuid: user_uuid_annotation,
        login_history_service: LoginHistoryService = Depends(
            get_login_history_service
        ),
        user_validator: UserValidator = Depends(get_user_validator),
        current_user: CurrentUserService = Depends(get_current_user),
        paginator: Paginator = Depends(get_paginator),
) -> ResponseLoginHistoryPaginated:
    """Available to authorized users

    Get user activity history

    Args:
    - **user_uuid** (str): The UUID of the user to get activity history
    - **page_number** (str): The number of the page to get
    - **page_size** (str): The size of the page to get

    Returns:
    - **list[ResponseLoginHistory]**: The user activity history list
    """
    await current_user.get_me(request)
    paginated_data = await paginator(
        login_history_service,
        "get_by_user",
        user_uuid=await user_validator.is_exists(user_uuid),
    )
    return ResponseLoginHistoryPaginated(
        count=paginated_data.count,
        total_pages=paginated_data.total_pages,
        prev=paginated_data.prev,
        next=paginated_data.next,
        results=[
            ResponseLoginHistory(
                uuid=result.uuid,
                user_uuid=result.user_uuid,
                ip_address=result.ip_address,
                user_agent=result.user_agent,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )
            for result in paginated_data.results
        ],
    )


@router.post(
    "/{user_uuid}/set_password/",
    response_model=ResponseString,
    summary="Change the user password by uuid",
)
async def change_password(
        request: Request,
        user_uuid: user_uuid_annotation,
        body: RequestPasswordChange,
        user_service: UserService = Depends(get_user_service),
        user_validator: UserValidator = Depends(get_user_validator),
        current_user: CurrentUserService = Depends(get_current_user),
) -> ResponseString:
    """Available to authorized users

    Change the user password

    Args:
    - **user_uuid** (str): The UUID of the user to change

    Returns:
    - **Str**: Message "Password successfully changed"
    """
    await current_user.get_me(request)
    await user_validator.is_exists(user_uuid)
    user = await user_service.change_password(user_uuid, body)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid password provided",
        )
    return ResponseString(
        code=HTTPStatus.OK,
        details="Password successfully changed",
    )
