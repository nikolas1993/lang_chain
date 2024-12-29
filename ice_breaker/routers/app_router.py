from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from ice_breaker import ice_break_with

router = APIRouter(
    prefix='', tags=['app']
)

templates = Jinja2Templates(directory="templates")


@router.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/process")
async def process(request: Request):
    form = await request.form()
    name = form["name"]

    # name = "Nik"

    summary, profile_pic_url = ice_break_with(name=name)
    print(summary.to_dict(), profile_pic_url)
    return {"summary_and_facts": summary.to_dict(), "picture_url": profile_pic_url}
