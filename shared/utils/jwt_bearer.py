from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt 
from shared.config import Config
from shared.enums import StatusCodeEnum


class JWTBearerUtil(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearerUtil, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerUtil, self).__call__(request)
        
        if credentials:
            if not credentials.scheme.lower() == "bearer":
                raise HTTPException(
                    status_code=StatusCodeEnum.UNAUTHORIZED.value,
                    detail="Invalid authentication scheme."
                )

            try:                
                payload = jwt.decode(
                    credentials.credentials,
                    Config.JWT_SECRET,
                    algorithms=["HS256"]
                )
                request.state.user = payload
                return payload
        
            except Exception as e:                
                raise HTTPException(
                    status_code=StatusCodeEnum.INTERNAL_ERROR.value,
                    detail=str(e)
                )
        else:
             raise HTTPException(
                    status_code=StatusCodeEnum.UNAUTHORIZED.value,
                    detail="Invalid authorization code."
                )

        
           