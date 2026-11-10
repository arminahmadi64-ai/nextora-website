import uuid
from datetime import datetime,timezone
from sqlalchemy import String,Text,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .database import Base
def uid(): return str(uuid.uuid4())
def now(): return datetime.now(timezone.utc)
class User(Base):
 __tablename__='users'
 id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
 email:Mapped[str]=mapped_column(String(320),unique=True,index=True,nullable=False)
 handle:Mapped[str]=mapped_column(String(40),unique=True,index=True,nullable=False)
 display_name:Mapped[str]=mapped_column(String(100),nullable=False)
 password_hash:Mapped[str]=mapped_column(String(255),nullable=False)
 is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
 is_verified:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Post(Base):
 __tablename__='posts'
 id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
 author_id:Mapped[str]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
 body:Mapped[str]=mapped_column(Text,nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
 author:Mapped['User']=relationship()
