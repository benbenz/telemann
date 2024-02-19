from django.apps import AppConfig


class SoundsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sounds'
    PLUGINS_CACHE = dict()

    def ready(self):
        pass
        # this should unblock the plugins on reload
        # for key,plugin in self.PLUGINS_CACHE.items():
        #     plugin([],duration=0,sample_rate=44100)
        #self.PLUGINS_CACHE = dict()
