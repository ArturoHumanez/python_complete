import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LogProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        print(f"Ruta: {request.url.path} | Tiempo: {process_time:.4f}s")
        return response
