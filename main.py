from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Set
from uuid import UUID
from datetime import date, datetime, time, timedelta

class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta

class Profile(BaseModel):
    name: str
    email: str
    age: int

class Image(BaseModel):
    url: HttpUrl
    name: str

class Product(BaseModel):
    name: str = Field(examples=["phone"])
    price: int = Field(title="Price of the item", 
                       description="Test description", 
                       gt=0)
    discount: int
    discounted_price: float
    tags: Set[str] = Field(examples=[["electronics", "phones"]])
    images: List[Image]

class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product]

class User(BaseModel):
    name: str
    email: str

app = FastAPI()


@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount)/100
    return {
        "product": product,
        "product_id": product_id,
        "category": category
    }

@app.post('/login')
def login(hello: str, username: str = Form(...), password: str = Form(...)):
    return {"username": username}


@app.post('/addevent')
def addevent(event: Event):
    return event

@app.post('/addoffer')
def addoffer(offer: Offer):
    return {Offer}

@app.post('/purchase/')
def purchase(user: User, product: Product):
    product.discounted_price = product.price - (product.price * product.discount)/100
    return {
        "product": product,
        "user": user
    }


@app.get('/user/{username}')
def profile(username):
    return f'this is a profile page for the user called {username}'


@app.get('/products')
def products(id: int=None, price: int=None):
    return {f'Product with an id: {id} and price: {price}'}


@app.get('/profile/{userid}/comments')
def profile(userid: int, commentid: int):
    return {f'Profile page for user {userid} and comment with id {commentid}'}


@app.post('/adduser')
def adduser(profile: Profile):
    return profile