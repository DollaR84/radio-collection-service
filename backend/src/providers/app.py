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
    create_stations_interactor = provide(interactors.CreateStations, scope=Scope.REQUEST)
    delete_station_interactor = provide(interactors.DeleteStation, scope=Scope.REQUEST)
    get_station_interactor = provide(interactors.GetStation, scope=Scope.REQUEST)
    get_stations_interactor = provide(interactors.GetStations, scope=Scope.REQUEST)
    get_stations_with_count_interactor = provide(interactors.GetStationsWithCount, scope=Scope.REQUEST)
    get_station_urls_interactor = provide(interactors.GetStationUrls, scope=Scope.REQUEST)
    check_station_url_interactor = provide(interactors.CheckStationUrl, scope=Scope.REQUEST)
    update_station_status_interactor = provide(interactors.UpdateStationStatus, scope=Scope.REQUEST)
    update_stations_status_interactor = provide(interactors.UpdateStationsStatus, scope=Scope.REQUEST)

    create_favorite_interactor = provide(interactors.CreateFavorite, scope=Scope.REQUEST)
    delete_favorite_interactor = provide(interactors.DeleteFavorite, scope=Scope.REQUEST)
    get_user_favorites_interactor = provide(interactors.GetUserFavorites, scope=Scope.REQUEST)
    get_user_favorites_with_count_interactor = provide(interactors.GetUserFavoritesWithCount, scope=Scope.REQUEST)

    create_access_permission_interactor = provide(interactors.CreateAccessPermission, scope=Scope.REQUEST)
    delete_access_permission_interactor = provide(interactors.DeleteAccessPermission, scope=Scope.REQUEST)
    get_access_permission_interactor = provide(interactors.GetAccessPermission, scope=Scope.REQUEST)
    get_current_access_permission_interactor = provide(interactors.GetCurrentAccessPermission, scope=Scope.REQUEST)
    get_access_permissions_interactor = provide(interactors.GetAccessPermissions, scope=Scope.REQUEST)
    update_access_permission_interactor = provide(interactors.UpdateAccessPermission, scope=Scope.REQUEST)

    create_file_interactor = provide(interactors.CreateFile, scope=Scope.REQUEST)
    delete_file_interactor = provide(interactors.DeleteFile, scope=Scope.REQUEST)
    get_file_by_id_interactor = provide(interactors.GetFileByID, scope=Scope.REQUEST)
    get_user_files_interactor = provide(interactors.GetUserFiles, scope=Scope.REQUEST)
    get_m3u_files_for_parse_interactor = provide(interactors.GetM3uFilesForParse, scope=Scope.REQUEST)
    get_pls_files_for_parse_interactor = provide(interactors.GetPlsFilesForParse, scope=Scope.REQUEST)
    get_json_files_for_parse_interactor = provide(interactors.GetJsonFilesForParse, scope=Scope.REQUEST)
    update_file_load_status_interactor = provide(interactors.UpdateFileLoadStatus, scope=Scope.REQUEST)
