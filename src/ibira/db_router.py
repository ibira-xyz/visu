class CmsRouter:
    """Route blog app models to the 'cms' database."""

    app_label = "blog"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return "cms"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return "cms"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            return db == "cms"
        return None