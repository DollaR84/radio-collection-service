from dishka import Provider, Scope, provide

from application import interactors


class AppProvider(Provider):

    create_user_interactor = provide(interactors.CreateUser, scope=Scope.REQUEST)
    delete_user_interactor = provide(interactors.DeleteUser, scope=Scope.REQUEST)
    get_user_by_id_interactor = provide(interactors.GetUserByID, scope=Scope.REQUEST)
    get_user_by_uuid_interactor = provide(interactors.GetUserByUUID, scope=Scope.REQUEST)
    get_user_by_google_interactor = provide(interactors.GetUserByGoogle, scope=Scope.REQUEST)
    get_user_by_email_interactor = provide(interactors.GetUserByEmail, scope=Scope.REQUEST)
    update_user_by_id_interactor = provide(interactors.UpdateUserByID, scope=Scope.REQUEST)
    update_user_by_uuid_interactor = provide(interactors.UpdateUserByUUID, scope=Scope.REQUEST)
    update_user_by_google_interactor = provide(interactors.UpdateUserByGoogle, scope=Scope.REQUEST)
    update_user_by_email_interactor = provide(interactors.UpdateUserByEmail, scope=Scope.REQUEST)

    create_station_interactor = provide(interactors.CreateStation, scope=Scope.REQUEST)
    delete_station_interactor = provide(interactors.DeleteStation, scope=Scope.REQUEST)
    get_station_interactor = provide(interactors.GetStation, scope=Scope.REQUEST)
    get_stations_interactor = provide(interactors.GetStations, scope=Scope.REQUEST)
    get_station_urls_interactor = provide(interactors.GetStationUrls, scope=Scope.REQUEST)
    update_station_status_interactor = provide(interactors.UpdateStationStatus, scope=Scope.REQUEST)
    update_stations_status_interactor = provide(interactors.UpdateStationsStatus, scope=Scope.REQUEST)

    create_favorite_interactor = provide(interactors.CreateFavorite, scope=Scope.REQUEST)
    delete_favorite_interactor = provide(interactors.DeleteFavorite, scope=Scope.REQUEST)
    get_user_favorites_interactor = provide(interactors.GetUserFavorites, scope=Scope.REQUEST)
