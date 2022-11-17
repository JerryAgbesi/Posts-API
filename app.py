from fastapi import FastAPI,Depends,status,HTTPException
from typing import Tuple,List
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from database import database,metadata,engine,get_database,posts
from models import Post,PostCreate,PostUpdate
from datetime import datetime



app = FastAPI(title="Posts-API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_post_or_404(post_id: int,database: Database = Depends(get_database)):
    get_query = posts.select().where(posts.c.id == post_id)
    
    get_post = await database.fetch_one(get_query)

    if get_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Post(**get_post)  

#skip and limit values to be used in pagination
async def pagination(skip: int = 0,limit:int = 10) -> Tuple[int,int]:
    return (skip,limit)


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

#Home route
@app.get("/")
async def home():
    return {"Welcome to the Posts API, redirect to /posts to get all posts"}       


#Create a new post 
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostCreate,database: Database = Depends(get_database)) -> Post:
    post_query = posts.insert().values(post.dict())
    query_id = await database.execute(post_query)
    row = await get_post_or_404(query_id,database)

    return row

#get a post based on its id
@app.get("/posts/{post_id}",response_model=Post)
async def get_post(post: Post = Depends(get_post_or_404),database: Database = Depends(get_database)) -> Post:
    postquery = posts.select().where(posts.c.id == post.id)

    row = await database.fetch_one(postquery)

    return Post(**row)

    
#get a list of all posts
@app.get("/posts")
async def get_posts(pagination: Tuple[int,int] = Depends(pagination),database: Database = Depends(get_database)) -> List[Post]:
    skip,limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows =  await database.fetch_all(select_query)
    result = [Post(**row) for row in rows ] 

    return result

#Update a post
@app.patch("/posts/{post_id}")
async def update_post(p:PostUpdate,post: Post = Depends(get_post_or_404),database: Database = Depends(get_database)) -> Post:
    #change date to current date on update
    p.date_updated = datetime.utcnow()

    update_query = posts.update().where(posts.c.id == post.id).values(p.dict(exclude_unset=True))
  
    await database.execute(update_query)

    result = await get_post_or_404(post.id,database)

    return result

#Delete a post
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post:Post = Depends(get_post_or_404),database: Database = Depends(get_database)):
    query = posts.delete().where(posts.c.id == post.id)

    await database.execute(query)







                                                                                                          