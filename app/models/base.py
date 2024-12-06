from datetime import datetime
from db.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, Date, Text, ForeignKey, Boolean