from dataclasses import dataclass

@dataclass
class Ticket:
    creator_id: int
    title: str
    description: str
    priority: int
    type: int