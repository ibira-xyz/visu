class CmsRouter:
    """Route blog app models to the 'cms' database."""

    app_label = "blog"

    def db_for_read(self, model, **_hints):
        """Route read operations for blog app models to the 'cms' database."""
        if model._meta.app_label == self.app_label:
            return "cms"
        return None

    def db_for_write(self, model, **_hints):
        """Route write operations for blog app models to the 'cms' database."""
        if model._meta.app_label == self.app_label:
            return "cms"
        return None

    def allow_relation(self, obj1, obj2, **_hints):
        """Allow relations if either object belongs to the blog app."""
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, _model_name=None, **_hints):
        """Allow migrations for blog app models only on the 'cms' database."""
        if app_label == self.app_label:
            return db == "cms"
        return None