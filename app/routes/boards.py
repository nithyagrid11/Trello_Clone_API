from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.board import Board
from app.models.user import User
from app.schemas.board import (BoardCreate,BoardResponse)
from app.schemas.board import BoardDetailResponse
import secrets
from app.models.board_member import BoardMember

router = APIRouter(
    prefix="/boards",
    tags=["Boards"]
)

@router.post("/",response_model=BoardResponse)
def create_board(
    board: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_board = Board(
        name=board.name,
        description=board.description,
        owner_id=current_user.id
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)

    owner_member = BoardMember(
    board_id=new_board.id,
    user_id=current_user.id,
    role="owner"
    )
    db.add(owner_member)
    db.commit()

    return new_board

@router.get("/", response_model=list[BoardResponse])
def get_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    boards = db.query(Board).filter(
        Board.owner_id == current_user.id
    ).all()

    return boards

@router.get("/{board_id}",response_model=BoardDetailResponse)
def get_board_detail(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    board = db.query(Board).filter(
        Board.id == board_id
    ).first()

    if not board:
        raise HTTPException(
            status_code=404,
            detail="Board not found"
        )
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return board

@router.post("/{board_id}/invite")
def generate_invitation(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    board = db.query(Board).filter(Board.id == board_id).first()

    if not board:
        raise HTTPException(
            status_code=404,
            detail="Board not found"
        )

    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only owner can invite users"
        )
    token = secrets.token_hex(16)
    board.invitation_token = token
    db.commit()
    return {
        "invitation_token": token
    }

@router.post("/join/{token}")
def join_board(
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    board = db.query(Board).filter(Board.invitation_token == token).first()

    if not board:
        raise HTTPException(
            status_code=404,
            detail="Invalid invitation token"
        )

    existing_member = db.query(BoardMember).filter(
        BoardMember.board_id == board.id,
        BoardMember.user_id == current_user.id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="Already member of board"
        )

    member = BoardMember(
        board_id=board.id,
        user_id=current_user.id,
        role="member"
    )

    db.add(member)
    db.commit()
    return {
        "message": "Joined board successfully"
    }