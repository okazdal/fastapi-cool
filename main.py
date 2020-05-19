from app import create_app
from settings import GET

import uvicorn

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app=app,
                host=GET.HOST,
                port=GET.PORT)
