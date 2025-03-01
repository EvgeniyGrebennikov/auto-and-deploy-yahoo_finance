import psycopg2

class PGDatabase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
        
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.connection = psycopg2.connect(
            host = host,
            port = 5432,
            database = database,
            user = user,
            password = password
        )

        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def post(self, query, args=()):
        try:
            self.cursor.execute(query, args)
        except Exception as err:
            print(repr(err))