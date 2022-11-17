from fastapi import FastAPI,Depends,status,HTTPException
from databases import Database
from database import database,metadata,engine,get_database,posts
from models import Post,PostCreate,PostUpdate
from datetime import datetime
import sqlalchemy


app = FastAPI(title="Posts-API")

async def get_post_or_404(post_id: int,database: Database = Depends(get_database)):
    get_query = posts.select().where(posts.c.id == post_id)
    
    get_post = await database.fetch_one(get_query)

    if get_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Post(**get_post)  

async def pagination(skip: int = 0,limit= 10) -> tuple[int,int]:
    return (skip,limit)


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()   


#Create a new post 
@app.post("/posts")
async def create_post(post:PostCreate,database: Database = Depends(get_database)) -> Post:
    post_query = posts.insert().values(post.dict())
    query_id = await database.execute(post_query)
    row = await get_post_or_404(query_id,database)

    return row

@app.get("/posts/{post_id}",response_model=Post)
async def get_post(post: Post = Depends(get_post_or_404),database: Database = Depends(get_database)) -> Post:
    postquery = posts.select().where(posts.c.id == post.id)

    row = await database.fetch_one(postquery)

    return Post(**row)

    

@app.get("/posts")
async def get_posts(pagination: tuple[int,int] = Depends(pagination),database: Database = Depends(get_database)) -> list[Post]:
    skip,limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows =  await database.fetch_all(select_query)
    result = [Post(**row) for row in rows ] 

    return result

@app.patch("/posts/{post_id}")
async def update_post(p:PostUpdate,post: Post = Depends(get_post_or_404),database: Database = Depends(get_database)) -> Post:
    update_query = posts.update().where(posts.c.id == post.id).values(p.dict(exclude_unset=True))
    print(p.dict(exclude_unset=True))
    await database.execute(update_query)

    result = await get_post_or_404(post.id,database)

    return result

@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post:Post = Depends(get_post_or_404),database: Database = Depends(get_database)):
    query = posts.delete().where(posts.c.id == post.id)

    await database.execute(query)







                                                                                                          