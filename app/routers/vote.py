from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from models.schemas import CreateVote
from db_config.database import get_db
from sqlalchemy.orm import Session
import models.db_models as db_models
import oauth2

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=HTTP_201_CREATED)
def vote(vote: CreateVote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(db_models.Vote).filter(
        db_models.Vote.user_id == current_user.id, db_models.Vote.post_id == vote.post_id)

    post = db.query(db_models.Post).filter(
        db_models.Post.id == vote.post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post  with id {vote.post_id} not found")

    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} already voted for this post")
        new_vote = db_models.Vote(
            post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully deleted vote"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist")
