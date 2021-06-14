from database.connect_to_database import Base

if Base is not None:
    class Interviews(Base):
        """"""
        __tablename__ = 'interviews'
        __table_args__ = {'autoload': True}


    class HrPartners(Base):
        """"""
        __tablename__ = 'hrpartners'
        __table_args__ = {'autoload': True}


    class Applications(Base):
        """"""
        __tablename__ = 'applications'
        __table_args__ = {'autoload': True}


    class Users(Base):
        """"""
        __tablename__ = 'users'
        __table_args__ = {'autoload': True}


else:
    class Interviews:
        pass


    class HrPartners:
        pass


    class Applications:
        pass


    class Users:
        pass
