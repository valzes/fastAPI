from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.models.schemas import CreatePost, ResponsePost, PostVote
from app.db_config.database import get_db
from sqlalchemy.orm import Session
import app.models.db_models as db_models
import app.oauth2 as oauth2
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   # posts = db.query(db_models.Post).filter(db_models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(db_models.Post, func.count(db_models.Vote.post_id).label("votes")).join(
        db_models.Vote, db_models.Post.id == db_models.Vote.post_id, isouter=True).group_by(db_models.Post.id).filter(
        db_models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.post("/", status_code=HTTP_201_CREATED,
             response_model=ResponsePost)
def create_posts(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = db_models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=PostVote)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(db_models.Post, func.count(db_models.Vote.post_id).label("votes")).join(
        db_models.Vote, db_models.Post.id == db_models.Vote.post_id, isouter=True).group_by(db_models.Post.id).filter(db_models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id}, not found")
    return post


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE from posts WHERE id = %s RETURNING * """, (str(id),))
    # delete_post = cursor.fetchone()

    delete_post_query = db.query(db_models.Post).filter(
        db_models.Post.id == id and db_models.Post.owner_id == current_user)

    delete_post = delete_post_query.first()

    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id}, not found")

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to delete post with id : {id}")

    delete_post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Post with id: {id} deleted successfully"}


@router.put("/{id}", status_code=HTTP_201_CREATED)
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id),))
    # new_post = cursor.fetchone()

    new_post = db.query(db_models.Post).filter(
        db_models.Post.id == id)

    upd_post = new_post.first()

    if upd_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id}, not found")

    if upd_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to update post with id : {id}")

    new_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"message": f"post with id: {id} successfully updated"}
