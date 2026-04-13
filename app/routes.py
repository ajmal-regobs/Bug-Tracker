from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bug
from app.schemas import BugCreate, BugResponse

router = APIRouter(prefix="/bugs", tags=["bugs"])


@router.post("/", response_model=BugResponse, status_code=201)
def add_bug(bug: BugCreate, db: Session = Depends(get_db)):
    new_bug = Bug(**bug.model_dump())
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return new_bug


@router.delete("/{bug_id}", status_code=204)
def remove_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    db.delete(bug)
    db.commit()


@router.get("/", response_model=list[BugResponse])
def list_bugs(db: Session = Depends(get_db)):
    return db.query(Bug).order_by(Bug.created_at.desc()).all()
