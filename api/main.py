from pathlib import Path
from fastapi import Depends, FastAPI, WebSocket, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from security import AuthHander, RequiresLoginException
import redis
from rq import Queue
from database import Postgres
from websocket_manager import WebSocketManager
from models import Run

api = FastAPI()
pg = Postgres()
auth_handler = AuthHander()
ws_manager = WebSocketManager()

redis_connection = redis.Redis(host='redis', port=6379)
rq = Queue(connection=redis_connection)

base_dir = Path(__file__).resolve().parent
api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=str(Path(base_dir, "templates")))


@api.exception_handler(RequiresLoginException)
async def exception_handler(request: Request,
                            exc: RequiresLoginException) -> Response:
    return RedirectResponse(url='/login')


@api.middleware("http")
async def create_auth_header(request: Request, call_next):
    if "Authorization" not in request.headers and "Authorization" in request.cookies:
        access_token = request.cookies["Authorization"]

        request.headers.__dict__["_list"].append(
            ("authorization".encode(), f"Bearer {access_token}".encode())
        )
    elif "Authorization" not in request.headers and "Authorization" not in request.cookies:
        request.headers.__dict__["_list"].append(
            ("authorization".encode(), "Bearer invalid".encode())
        )

    response = await call_next(request)
    return response


@api.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await ws_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"{data}")
    except Exception as e:
        print(e)
    finally:
        if websocket is not None:
            await ws_manager.disconnect(websocket)


@api.get("/", response_class=HTMLResponse)
async def index(request: Request, user=Depends(auth_handler.auth_wrapper)):
    context = {"title": "Home | Supercontinuum"}
    return templates.TemplateResponse("index.html.j2",
                                      {"request": request,
                                       "context": context,
                                       "user": user})


@api.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    context = {"title": "Login | Supercontinuum"}
    return templates.TemplateResponse("login.html.j2",
                                      {"request": request,
                                       "context": context})


@api.post("/auth")
async def auth(request: Request,
                response: Response,
                email: str = Form(...), password: str = Form(...)):

    if email != "test@test.com":
        return templates.TemplateResponse("partials/login_form.html.j2",
                                          {"request": request,
                                           "invalid_login": True})

    # add cookie
    response.set_cookie(key="Authorization",
                        value=f"token",
                        httponly=True,
                        samesite="strict")
    # redirect user to home
    response.headers["HX-Redirect"] = api.url_path_for('index')
    return {"success": "true"}


@api.get("/health")
async def get_health():
    return {"healthy": "true"}


@api.get("/runs")
async def get_test_runs():
    return pg.get_all_test_runs()


@api.post("/run")
async def start_new_run():
    run = Run(name='test')
    run_id = pg.insert_new_test_run(run.name, 'PENDING')
    task = rq.enqueue('worker.tasks.run_test', run_id)
    pg.update_test_run_status(run_id, 'QUEUED')
    return run_id
