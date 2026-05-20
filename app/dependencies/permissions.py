from fastapi import HTTPException
from app.models.board_member import BoardMember

def can_modify_ticket(board,ticket,current_user,db):
    # Board owner can do everything
    if board.owner_id == current_user.id:
        return True

    member = db.query(BoardMember).filter(
        BoardMember.board_id == board.id,
        BoardMember.user_id == current_user.id
    ).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Not board member"
        )

    # Members only modify own tickets
    if ticket.created_by_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Cannot modify others tickets"
        )
    return True