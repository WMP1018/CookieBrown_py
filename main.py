from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import Base, engine, get_db
import models.database
import models.cookie
import logging

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def index():
    return {'mensaje': 'Bienvenidos la tienda de Cookie Brown'}

@app.post('/cookies', response_model=models.cookie.Product)
def create_cookie(cookie: models.cookie.ProductCreate, db: Session = Depends(get_db)):
    logging.info(f"Creando producto: {cookie}")
    db_cookie = models.cookie.ProductModel(**cookie.model_dump())
    db.add(db_cookie)
    db.commit()
    db.refresh(db_cookie)
    logging.info(f"Producto creado: {db_cookie}")
    return db_cookie

@app.get('/cookies', response_model= list[models.cookie.Product])
def get_cookies(skip: int=0, limit: int=10, db:Session = Depends(get_db)):
    cookies = db.query(models.cookie.ProductModel).offset(skip).limit(limit).all()
    logging.info(f"Obteniendo productos: {cookies}")
    return cookies

@app.get('/cookies/{cookie_id}', response_model=models.cookie.Product)
def get_cookie(cookie_id: int, db: Session = Depends(get_db)):
    cookie = db.query(models.cookie.ProductModel).filter(models.cookie.ProductModel.id == cookie_id).first()
    logging.info(f"Obteniendo producto con el id: {cookie_id}")
    if cookie is None:
        raise HTTPException(status_code=404, detail="Cookie not found")
    return cookie

@app.put('/cookies/{cookie_id}', response_model=models.cookie.Product)
def update_cookie(cookie_id: int, cookie: models.cookie.ProductUpdate, db: Session = Depends(get_db)):
    db_cookie = db.query(models.cookie.ProductModel).filter(models.cookie.ProductModel.id == cookie_id).first()
    logging.info(f"Actualizando producto con el id: {cookie_id}")
    if db_cookie is None:
        raise HTTPException(status_code=404, detail="Cookie not found")
    for key, value in cookie.model_dump().items():
        setattr(db_cookie, key, value)
    db.commit()
    db.refresh(db_cookie)
    return db_cookie

@app.delete('/cookies/{cookie_id}')
def delete_cookie(cookie_id: int, db: Session = Depends(get_db)):
    db_cookie = db.query(models.cookie.ProductModel).filter(models.cookie.ProductModel.id == cookie_id).first()
    logging.info(f"Eliminando producto con el id: {cookie_id}")
    if db_cookie is None:
        raise HTTPException(status_code=404, detail="Cookie not found")
    db.delete(db_cookie)
    db.commit()
    return {"message": "Cookie deleted"}