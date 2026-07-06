from fastapi import (APIRouter,Depends,HTTPException)
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import can_modify_ticket
from app.models.board_member import BoardMember
from app.models.ticket import Ticket
from app.models.section import Section
from app.models.board import Board
from app.models.user import User
from app.schemas.ticket import (TicketCreate,TicketResponse)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("/",response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    section = db.query(Section).filter(
        Section.id == ticket.section_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )
    board = db.query(Board).filter(
        Board.id == section.board_id
    ).first()

    member = db.query(BoardMember).filter(
        BoardMember.board_id == board.id,
        BoardMember.user_id == current_user.id
    ).first()

    if (
     board.owner_id != current_user.id
     and not member
    ):
     raise HTTPException(
        status_code=403,
        detail="Not authorized"
     )

    if ticket.assigned_user_id is not None:
        assignee = db.query(User).filter(
            User.id == ticket.assigned_user_id
        ).first()
        if not assignee:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
            )

    new_ticket = Ticket(
        name=ticket.name,
        description=ticket.description,
        section_id=ticket.section_id,
        assigned_user_id=ticket.assigned_user_id,
        created_by_id=current_user.id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

@router.get("/section/{section_id}",response_model=list[TicketResponse])
def get_tickets(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    section = db.query(Section).filter(
        Section.id == section_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    board = db.query(Board).filter(
        Board.id == section.board_id
    ).first()
    member = db.query(BoardMember).filter(
      BoardMember.board_id == board.id,
      BoardMember.user_id == current_user.id
    ).first()

    if (
      board.owner_id != current_user.id
      and not member
    ):
      raise HTTPException(
        status_code=403,
        detail="Not authorized"
      )
    tickets = db.query(Ticket).filter(
        Ticket.section_id == section_id
    ).all()

    return tickets

@router.put("/{ticket_id}",response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    old_section = db.query(Section).filter(
        Section.id == ticket.section_id
    ).first()

    new_section = db.query(Section).filter(
        Section.id == ticket_data.section_id
    ).first()

    if not new_section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    old_board = db.query(Board).filter(
        Board.id == old_section.board_id
    ).first()
    can_modify_ticket(old_board,ticket,current_user,db)
    if old_section.board_id != new_section.board_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot move ticket to different board"
        )

    if ticket_data.assigned_user_id is not None:
        assignee = db.query(User).filter(
            User.id == ticket_data.assigned_user_id
        ).first()
        if not assignee:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
            )

    ticket.name = ticket_data.name
    ticket.description = ticket_data.description
    ticket.section_id = ticket_data.section_id
    ticket.assigned_user_id = ticket_data.assigned_user_id

    db.commit()
    db.refresh(ticket)

    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    section = db.query(Section).filter(
        Section.id == ticket.section_id
    ).first()

    board = db.query(Board).filter(
        Board.id == section.board_id
    ).first()

    can_modify_ticket(board,ticket,current_user,db)
    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted"
    }