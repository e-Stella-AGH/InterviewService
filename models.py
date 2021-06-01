from connect_to_database import Base

if Base is not None:
    class Interviews(Base):
        """"""
        __tablename__ = 'interviews'
        __table_args__ = {'autoload': True}


    class HrPartners(Base):
        """"""
        __tablename__ = 'hrpartners'
        __table_args__ = {'autoload': True}
else:
    class Interviews:
        pass


    class HrPartners:
        pass
