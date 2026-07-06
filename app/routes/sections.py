from fastapi import (APIRouter, Depends, HTTPException)
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.section import Section
from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.user import User
from app.schemas.section import (SectionCreate, SectionResponse)

router = APIRouter(
    prefix="/sections",
    tags=["Sections"]
)

@router.post("/", response_model=SectionResponse)
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    board = db.query(Board).filter(
        Board.id == section.board_id
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
    new_section = Section(
        name=section.name,
        description=section.description,
        board_id=section.board_id
    )
    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section

@router.get("/board/{board_id}",response_model=list[SectionResponse]) 
def get_sections(
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

    member = db.query(BoardMember).filter(
        BoardMember.board_id == board.id,
        BoardMember.user_id == current_user.id
    ).first()

    if board.owner_id != current_user.id and not member:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    sections = db.query(Section).filter(
        Section.board_id == board_id
    ).all()

    return sections

@router.put("/{section_id}",response_model=SectionResponse)
def update_section(
    section_id: int,
    section_data: SectionCreate,
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

    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    section.name = section_data.name
    section.description = section_data.description

    db.commit()
    db.refresh(section)

    return section

@router.delete("/{section_id}")
def delete_section(
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

    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    db.delete(section)
    db.commit()

    return {
        "message": "Section deleted"
    }