import aiohttp
from fastapi.exceptions import HTTPException
from functools import wraps
from http import HTTPStatus

from core.config import settings


def special_permissions(roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(**kwargs):
            request = kwargs.get('request')
            authorization = request.headers.get('Authorization')
            if not authorization:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
            auth_service_url = f'http://{settings.auth_host}:{settings.auth_port}/api/v1/'
            url = auth_service_url + 'role/user/roles'
            headers = {'Authorization': authorization, "Accept": 'application/json'}
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    if not response.status == 200:
                        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED) 
                    body = await response.json()
            if not any([role in body for role in roles]):
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
            res = await func(**kwargs)
            return res
        
        return wrapper
    
    return decorator
    
   
                

