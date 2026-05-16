from fastapi import Form
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.gateway import Gateway

app = FastAPI()

# Mount static folder (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template folder
templates = Jinja2Templates(directory="frontend")


gateway = Gateway(
    max_capacity = 10,
    admit_rate = 2,
    session_timeout = 5
)

@app.on_event("startup")
def startup_event(): # Starting VWR system
    gateway.start_auto_processing(interval=10) 


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# @app.get("/wait/{user_id}", response_class=HTMLResponse)
# async def wait_page(request: Request, user_id: str):
#     return templates.TemplateResponse(
#         request=request,
#         name="wait.html",
#         context={
#             "user_id": user_id
#         }
#     )

@app.post("/request-access")
async def request_access(user_id: str = Form(...)):
    result = gateway.request_access(user_id)
    return result

@app.get("/status/{user_id}")
async def user_status(user_id: str):
    return gateway.get_user_status(user_id)

@app.get("/dashboard-data")
async def dashboard_data():
    return gateway.get_dashboard_data()

