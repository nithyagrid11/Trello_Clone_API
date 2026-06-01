from fastapi import HTTPException
from app.dependencies.permissions import can_modify_ticket
#testing authorization logic for modifying tickets

class MockBoard:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.id = 1

class MockTicket:
    def __init__(self, created_by_id):
        self.created_by_id = created_by_id

class MockUser:
    def __init__(self, user_id):
        self.id = user_id

class MockQuery:
    def __init__(self, member):
        self.member = member
    def filter(self, *args):
        return self
    def first(self):
        return self.member

class MockDB:
    def __init__(self, member):
        self.member = member
    def query(self, model):
        return MockQuery(self.member)

def test_owner_can_modify_ticket():
    board = MockBoard(owner_id=1)
    ticket = MockTicket(created_by_id=2)
    user = MockUser(user_id=1)
    db = MockDB(member=None)
    assert can_modify_ticket(
        board,
        ticket,
        user,
        db
    ) is True

def test_ticket_creator_can_modify():
    board = MockBoard(owner_id=1)
    ticket = MockTicket(created_by_id=2)
    user = MockUser(user_id=2)
    db = MockDB(member=object())
    assert can_modify_ticket(
        board,
        ticket,
        user,
        db
    ) is True

def test_non_member_cannot_modify():
    board = MockBoard(owner_id=1)
    ticket = MockTicket(created_by_id=2)
    user = MockUser(user_id=3)
    db = MockDB(member=None)
    try:
        can_modify_ticket(board,ticket,user,db)
        assert False
    except HTTPException as e:
        assert e.status_code == 403
        assert e.detail == "Not board member"

def test_member_cannot_modify_others_ticket():
    board = MockBoard(owner_id=1)
    ticket = MockTicket(created_by_id=2)
    user = MockUser(user_id=3)
    db = MockDB(member=object())
    try:
        can_modify_ticket(
            board,
            ticket,
            user,
            db
        )
        assert False
    except HTTPException as e:
        assert e.status_code == 403
        assert e.detail == "Cannot modify others tickets"