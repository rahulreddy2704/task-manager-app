"""
Main FastAPI application.
This file contains all API routes for the Task Manager.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Task Manager API"}