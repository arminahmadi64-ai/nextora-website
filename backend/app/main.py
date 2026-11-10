from fastapi import FastAPI,Depends,HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,EmailStr,Field
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .config import settings
from .database import Base,engine,get_db
from .models import User,Post
from .security import hash_password,verify_password,create_access_token,decode_access_token
if settings.environment=='production' and (len(settings.jwt_secret)<32 or 'CHANGE_THIS' in settings.jwt_secret): raise RuntimeError('Set a unique JWT_SECRET of at least 32 characters')
app=FastAPI(title='NEXTORA API',docs_url=None if settings.environment=='production' else '/docs',redoc_url=None if settings.environment=='production' else '/redoc')
origins=[v.strip() for v in settings.cors_origins.split(',') if v.strip()]
if not origins or '*' in origins: raise RuntimeError('CORS_ORIGINS must be an explicit allowlist')
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['GET','POST'],allow_headers=['Authorization','Content-Type'])
security=HTTPBearer(auto_error=False)
class Register(BaseModel):
 email:EmailStr
 handle:str=Field(min_length=3,max_length=40,pattern=r'^[a-zA-Z0-9_]+$')
 display_name:str=Field(min_length=1,max_length=100)
 password:str=Field(min_length=12,max_length=128)
class Login(BaseModel): email:EmailStr; password:str=Field(min_length=1,max_length=128)
class PostIn(BaseModel): body:str=Field(min_length=1,max_length=5000)
def auth(credentials:HTTPAuthorizationCredentials|None=Depends(security),db:Session=Depends(get_db)):
 if not credentials: raise HTTPException(401,'Authentication required')
 uid=decode_access_token(credentials.credentials); user=db.get(User,uid) if uid else None
 if not user or not user.is_active: raise HTTPException(401,'Invalid or inactive account')
 return user
@app.middleware('http')
async def headers(request:Request,call_next):
 response=await call_next(request); response.headers['X-Content-Type-Options']='nosniff'; response.headers['X-Frame-Options']='DENY'; response.headers['Referrer-Policy']='strict-origin-when-cross-origin'; return response
@app.on_event('startup')
def startup():
 # Temporary initial-schema bootstrap; replace with Alembic migrations before production launch.
 Base.metadata.create_all(bind=engine)
@app.get('/health')
def health(): return {'status':'ok','service':'nextora-api'}
@app.get('/health/database')
def database_health(db:Session=Depends(get_db)):
 from sqlalchemy import text
 db.execute(text('SELECT 1')); return {'status':'ok','database':'connected'}
@app.post('/auth/register',status_code=201)
def register(data:Register,db:Session=Depends(get_db)):
 if not settings.registration_enabled: raise HTTPException(503,'Registration is closed while email verification is being configured')
 user=User(email=data.email.lower(),handle=data.handle.lower(),display_name=data.display_name.strip(),password_hash=hash_password(data.password))
 db.add(user)
 try: db.commit(); db.refresh(user)
 except IntegrityError: db.rollback(); raise HTTPException(409,'Email or handle already registered')
 # Registration remains disabled until email verification is implemented.
 return {'id':user.id,'message':'Account created; verification required'}
@app.post('/auth/login')
def login(data:Login,db:Session=Depends(get_db)):
 user=db.scalar(select(User).where(User.email==data.email.lower()))
 if not user or not verify_password(data.password,user.password_hash) or not user.is_active: raise HTTPException(401,'Invalid email or password')
 if not user.is_verified: raise HTTPException(403,'Email verification required')
 return {'access_token':create_access_token(user.id),'token_type':'bearer','expires_in':settings.access_token_minutes*60}
@app.get('/users/me')
def me(user:User=Depends(auth)): return {'id':user.id,'email':user.email,'handle':user.handle,'display_name':user.display_name,'is_verified':user.is_verified}
@app.post('/posts',status_code=201)
def create_post(data:PostIn,user:User=Depends(auth),db:Session=Depends(get_db)):
 post=Post(author_id=user.id,body=data.body.strip()); db.add(post); db.commit(); db.refresh(post); return {'id':post.id,'body':post.body,'created_at':post.created_at,'author':user.handle}
@app.get('/feed')
def feed(limit:int=20,user:User=Depends(auth),db:Session=Depends(get_db)):
 rows=db.scalars(select(Post).options(joinedload(Post.author)).order_by(Post.created_at.desc()).limit(max(1,min(limit,50)))).unique().all()
 return [{'id':p.id,'body':p.body,'created_at':p.created_at,'author':{'handle':p.author.handle,'display_name':p.author.display_name}} for p in rows]
@app.get('/')
def root(): return {'message':'NEXTORA API','health':'/health'}
