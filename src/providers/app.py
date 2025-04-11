from dishka import Provider, Scope, provide

from application import interactors


class AppProvider(Provider):

    create_user_interactor = provide(interactors.CreateUser, scope=Scope.REQUEST)
    delete_user_interactor = provide(interactors.DeleteUser, scope=Scope.REQUEST)
