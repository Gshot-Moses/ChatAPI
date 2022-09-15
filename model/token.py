from dataclasses import dataclass


@dataclass
class LoginToken:
	user_id: int
	token: str