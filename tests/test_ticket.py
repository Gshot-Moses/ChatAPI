from adapters.repo import TicketRepo
from model.ticket import Ticket
from .fixtures import *


def test_save_ticket_success(session):
    tick = Ticket(1, "Mauvaise connexion",
    "Je ne  parviens pas a me connecter a internet", 1, 1)
    session.add(tick)
    session.commit()
    expected = session.execute("SELECT * FROM tickets WHERE creator_id=1")
    print(expected.all())

engine = create_test_engine()
session = create_session(engine)
test_save_ticket_success(session)