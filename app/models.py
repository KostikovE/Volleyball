from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base



class VideoStatus(str, enum.Enum):
    uploaded = "uploaded"      
    queued = "queued"          
    processing = "processing"  
    completed = "completed"    
    error = "error"            

class ServeSide(str, enum.Enum):
    unknown = "unknown"  # подачи (неизвестно, дальний или ближний)
    near = "near"        
    far = "far"          



# Таблица users — пользователи системы

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    
    videos: Mapped[list["Video"]] = relationship(back_populates="user")



# Таблица videos 

class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    filename: Mapped[str] = mapped_column(String(512))          # путь к файлу
    duration: Mapped[float | None] = mapped_column(Float, nullable=True)  # длительность в секундах
    fps: Mapped[float | None] = mapped_column(Float, nullable=True)        # кадров в секунду
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)      # ширина
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)     # высота
    status: Mapped[VideoStatus] = mapped_column(Enum(VideoStatus), default=VideoStatus.uploaded)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    
    user: Mapped["User"] = relationship(back_populates="videos")
    jobs: Mapped[list["ProcessingJob"]] = relationship(back_populates="video")
    rallies: Mapped[list["Rally"]] = relationship(back_populates="video")



# Таблица processing_jobs 

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"))
    status: Mapped[str] = mapped_column(String(50), default="queued")
    progress: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    artifact_path: Mapped[str | None] = mapped_column(String(512), nullable=True)  
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    video: Mapped["Video"] = relationship(back_populates="jobs")



# Таблица rallies 

class Rally(Base):
    __tablename__ = "rallies"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"))
    number: Mapped[int] = mapped_column(Integer)           
    start_time: Mapped[float] = mapped_column(Float)       
    end_time: Mapped[float] = mapped_column(Float)         
    start_frame: Mapped[int] = mapped_column(Integer)      
    end_frame: Mapped[int] = mapped_column(Integer)        
    serve_side: Mapped[ServeSide] = mapped_column(Enum(ServeSide), default=ServeSide.unknown)

    video: Mapped["Video"] = relationship(back_populates="rallies")