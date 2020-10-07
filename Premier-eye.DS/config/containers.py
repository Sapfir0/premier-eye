from dependency_injector import containers, providers
from services.baseInteractionService import BaseInteractionService
from services.apiInteractionService import ApiInteractionService


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')


class InteractionService(containers.DeclarativeContainer):
    apiInteractionService = providers.Singleton(ApiInteractionService, Configs.config)