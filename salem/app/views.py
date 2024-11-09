from enum import Enum
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET

import time
import threading
from datetime import datetime


class Clients:
    clients: list[str] = []
    last_clients_ping: dict[str, datetime] = {}

    @staticmethod
    def add_client(client):
        Clients.clients.append(client)

    @staticmethod
    def get_size():
        return len(Clients.clients)

    @staticmethod
    def last_client_ping(username: str):
        Clients.last_clients_ping[username] = time.time()

    @staticmethod
    def checkUsersActive():
        """Will be called every 10 seconds to check if all added users are still active."""
        for client in Clients.clients[
            :
        ]:  # Create a copy to avoid modification during iteration
            if time.time() - Clients.last_clients_ping.get(client, 0) > 10:
                Clients.clients.remove(client)

        # Schedule the next run in 10 seconds
        timer = threading.Timer(10.0, Clients.checkUsersActive)
        timer.daemon = True  # Allow the thread to be killed when the main program exits
        timer.start()

    def __init__(self):
        Clients.checkUsersActive()  # initial recursive call


class RoleType(Enum):
    INVESTIGATOR = "investigator"
    LOOKOUT = "lookout"
    SHERIFF = "sheriff"
    POTION_MASTER = "potion_master"
    ESCORT = "escort"
    MEDIUM = "medium"
    DEAD = "dead"


ROLE_LIMITS = {
    RoleType.INVESTIGATOR: 2,
    RoleType.LOOKOUT: 4,
    RoleType.SHERIFF: 2,
    RoleType.POTION_MASTER: 1,
}


class Player:
    # store map of role to number of players
    ROLE_TO_PLAYERS: dict[RoleType, list[str]] = {
        RoleType.INVESTIGATOR: [],
        RoleType.LOOKOUT: [],
        RoleType.SHERIFF: [],
        RoleType.POTION_MASTER: [],
    }

    def __init__(self, username: str):
        self.username = username
        self.role = None

    def attempt_assign_role(self, role: RoleType):
        if len(Player.ROLE_TO_PLAYERS[role]) >= ROLE_LIMITS[role]:
            return False
        Player.ROLE_TO_PLAYERS[role].append(self.username)
        self.role = role
        return True


class Role:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


def home(request) -> HttpRequest:
    return render(request, "app/home.html")


def check_user(request) -> HttpResponse:
    """Make sure added user still active."""
    username = str(request.session.get("username"))
    Clients.last_clients_ping[username] = datetime.now()


@require_POST
def add_client(request) -> HttpResponse:
    # get form data
    form = request.POST
    username = form.get("username")
    # store anonymous user
    request.session["username"] = username
    Clients.add_client(username)
    print("Amount of clients: ", len(Clients.clients))
    return HttpResponse(status=200)


@require_GET
def get_clients_size(request):
    return JsonResponse({"clients_size": Clients.get_size()})


@require_POST
def attempt_assign_role(request):
    form = request.POST

    role = form.get("role")
    username = request.session.get("username")
    if not Player.attempt_assign_role(username, role):
        return HttpResponse(status=400)
    return HttpResponse(status=200)


def main(request):
    # Get user
    username = request.session.get("username")

    return render(request, "app/main.html")
