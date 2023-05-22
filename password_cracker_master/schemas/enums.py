from enum import Enum


class StatusEnum(str, Enum):
    ACCEPTED = "accepted"
    PROCESSING = "processing"
    APPLIED = "applied"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    OFFLINE = "offline"
    ONLINE = "online"
