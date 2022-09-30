
# from djdsdsango.shortcuts import HttpResponse
from fastapi import Depends, FastAPI, File ,Form, UploadFile, Request
from  typing import List, Optional
from flask import request
from pydantic import BaseModel, Json
from sqlalchemy import Column,String,Integer,Boolean
from fastapi.responses import HTMLResponse
from database_connection_fastapi2 import Base, engine , SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="htmlfile")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,primary_key=True,index=True)
    phone = Column(Integer,primary_key=True,index=True)
    
Base.metadata.create_all(bind=engine)    

app = FastAPI()
    
def gert_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
   
    
class Userschema(BaseModel):
    id:int
    name:str
    phone:int

    class Config:
        orm_mode = True



@app.post('/userform', response_model=Userschema)
def userform(user:Userschema,db:Session=Depends(gert_db)):
    u = User(id=user.id,name=user.name,phone=user.phone)        
    db.add(u)
    db.commit()
    return u 



@app.get('/userdata', response_model= List[Userschema])
def userdata(request:Request,db:Session=Depends(gert_db)):
        u = db.query(User).all()
        print(u)
        return templates.TemplateResponse('ab.html',{'request':request, "u":u})
        


@app.get('/data/{name}',response_class=HTMLResponse)
def write_data(request:Request, name:str):
    return templates.TemplateResponse("ab.html", {"request":request,"name":name})
    





@app.put('/userup/{id}',response_model=Userschema)
def userupdate( id:int,user:Userschema, db:Session=Depends(gert_db)):
    
    u = db.query(User).filter(User.id==id).first()
    u.name = user.name
    u.phone = user.phone
    u.id = user.id
    
    print(u.id,"fsndfsnf")
    db.add(u)
    db.commit()
    print(u.name,"nfskfnkdnsfndsnfns")
    return u
    
    
@app.delete('/delete/{id}',response_class=JSONResponse)    
def userdelete(id:int,db:Session=Depends(gert_db)):
        u = db.query(User).filter(User.id==id).first()
        db.delete(u)
        db.commit()
        return {f"{u.name} is delete"} 
    
    
    
    
    