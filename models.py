from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# two models 1. Role 2. Auditions
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key = True)
    character_name = Column(String, nullable = False)

    #Relationship - role has many auditions
    auditions = relationship('Audition', back_populates = 'role')

    # get a list of actor in a given role
    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    # to return a list of locations for auditions associated with a role
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    # return the first hired audition
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else 'No actor has been hired for this role'
    
    # return the second hired audtion
    def understudy(self):
        hired_audtions = [audition for audition in self.auditions if audition.hired]
        return hired_audtions[1] if len(hired_audtions) > 1 else "No actor has been hired as an understudy for this role"




class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(String, primary_key = True)
    actor = Column(String, nullable = False)
    location = Column(String, nullable = False)
    phone_no = Column(Integer, nullable = False)
    hired = Column(Boolean, default = False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable = False)

    # relationship: an audition belongs to a role
    role = relationship('Role', back_populates = 'auditions' )

    # change the hired attribute to True
    def call_back(self):
        self.hired = True




# Database Set-Up
theater_engine = create_engine('sqlite:///moringa_theater.db')
my_theater_session = sessionmaker(bind = theater_engine)
session = my_theater_session()



