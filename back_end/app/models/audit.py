from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, JSON
from datetime import datetime
from typing import Optional
from app.models.base_model import BaseModel

class Audit(BaseModel):
    __tablename__ = "audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    site: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="audits")

    def __init__(
        self,
        user_id: uuid.UUID,
        site: str,
        content: dict,
        timestamp: Optional[str | datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.site = site
        self.content = content
        self.timestamp = (
            datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
        ) or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "site": self.site,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Audit":
        return cls(
            user_id=uuid.UUID(data["user_id"]),
            site=data["site"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"])
            if data.get("timestamp")
            else datetime.utcnow(),
        )

    def __repr__(self):
        return f"<Audit site='{self.site}' user_id='{self.user_id}' at {self.timestamp}>"

from app.models.user import User

