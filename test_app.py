from fastapi.testclient import TestClient
from app import app

testclient = TestClient(app)


def test_create_post():
    response = testclient.post("http://127.0.0.1:8000/posts",json={
        "author": "IBM",
        "content_tags": "API,websockets,backend",
        "content":'''What is a message broker?

                    A message broker is software that enables applications, systems, and services to communicate with each other and exchange information. The message broker does this by translating messages between formal messaging protocols. This allows interdependent services to “talk” with one another directly, even if they were written in different languages or implemented on different platforms.
                    
                    Message brokers are software modules within messaging middleware or message-oriented middleware (MOM) solutions. This type of middleware provides developers with a standardized means of handling the flow of data between an application’s components so that they can focus on its core logic. It can serve as a distributed communications layer that allows applications spanning multiple platforms to communicate internally.

                    Message brokers can validate, store, route, and deliver messages to the appropriate destinations. They serve as intermediaries between other applications, allowing senders to issue messages without knowing where the receivers are, whether or not they are active, or how many of them there are. This facilitates decoupling of processes and services within systems.

                    In order to provide reliable message storage and guaranteed delivery, message brokers often rely on a substructure or component called a message queue that stores and orders the messages until the consuming applications can process them. In a message queue, messages are stored in the exact order in which they were transmitted and remain in the queue until receipt is confirmed.

                    Asynchronous messaging (15:11) refers to the type of inter-application communication that message brokers make possible. It prevents the loss of valuable data and enables systems to continue functioning even in the face of the intermittent connectivity or latency issues common on public networks. Asynchronous messaging guarantees that messages will be delivered once (and once only) in the correct order relative to other messages.

                    Message brokers may comprise queue managers to handle the interactions between multiple message queues, as well as services providing data routing, message translation, persistence, and client state management functionalities.''',
        
        })
    assert response.status_code == 200 

def test_get_post():
    response = testclient.get("http://127.0.0.1:8000/posts/1")
    assert response.status_code == 200 

def test_get_posts():
    response = testclient.get("http://127.0.0.1:8000/posts")
    assert response.status_code == 200 





