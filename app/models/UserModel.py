class User(EntityMeta):
    __tablename__ = "user"
    userId = Column(Integer)
    username = Column(String)
    password = Column(String)
