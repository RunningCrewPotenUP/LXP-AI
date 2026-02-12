from fastapi import Request

def get_embedder(request: Request):
    return request.app.state.embedder

def get_dragonkue_embedder(request: Request):
    return request.app.state.dragonkue_embedder