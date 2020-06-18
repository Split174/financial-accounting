from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AlchemyORM:
    """
    Класс для работы с alchemy orm db
    """
    def __init__(self, app=None):
        self._session = None
        self._app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._app = app
        self._app.teardown_appcontext(self.close_db)

    @property
    def connection(self): # TODO в контексте ORM называть проперти connection возможно не верно
        self._connect()
        return self._session

    def _connect(self):
        engine = create_engine(self._app.config['DB_CONNECTION'])
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def close_db(self, exception):
        if self._session is not None:
            self._session.close()
            self._session = None


db = AlchemyORM()

