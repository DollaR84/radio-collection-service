from dishka import Provider, Scope, provide

from application import interactors


class AppProvider(Provider):

    create_user_interactor = provide(interactors.CreateUser, scope=Scope.REQUEST)
    delete_user_interactor = provide(interactors.DeleteUser, scope=Scope.REQUEST)

    create_station_interactor = provide(interactors.CreateStation, scope=Scope.REQUEST)
    delete_station_interactor = provide(interactors.DeleteStation, scope=Scope.REQUEST)
    get_station_urls_interactor = provide(interactors.GetStationUrls, scope=Scope.REQUEST)
