
import shutil
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, File ,Form, UploadFile, Request
from  typing import List, Optional
app = FastAPI()

  



app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/itemsa/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item2.html", {"request": request})


# @app.post("login")
# async def login(username: str = Form(), password: str = Form()):
#     return {"username": username}


@app.post("/img")
async def filedata(files:List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}' , 'wb')as abc:
            shutil.copyfileobj(img.file, abc)
    
    
    return {'file name':"good"}        
