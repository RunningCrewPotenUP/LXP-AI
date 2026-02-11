from fastapi import Request

def get_embedder(request: Request):
    return request.app.state.embedder