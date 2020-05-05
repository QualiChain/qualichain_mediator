from sqlalchemy import Column, Integer, String, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import ENGINE_STRING

Base = declarative_base()


class ExtractedSkill(Base):
    """Extracted Skills Table"""
    __tablename__ = 'extracted_skill'

    id = Column(Integer, primary_key=True, nullable=False)
    job_name = Column(String(1024), nullable=True)
    skill = Column(String(1024), nullable=True)
    frequencyOfMention = Column(Integer, nullable=True)
    kind = Column(String(1024), nullable=True)

    def __repr__(self):
        return '<ExtractedSkill name: {}, job_name: {}>'.format(self.skill, self.job_name)


class PostgresClient(object):
    """This is a Python Object that handles Postgres DB using SQLAlchemy"""

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.meta = MetaData()
        self.conn = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()

    def initialize_extracted_skills_model(self):
        """This function is used to initialize ExtractedSkill Table"""
        Base.metadata.create_all(self.engine)
        print('ExtractedSkill Initiated Successfully')

    def upsert_new_skill(self, **kwargs):
        """
        This function is used to append a new skill per job name

        :param kwargs: provided kwargs
        :return: None
        """
        this_skill = self.session.query(ExtractedSkill).filter_by(
            job_name=kwargs['job_name'],
            skill=kwargs['skill']
        )
        if this_skill.count():
            this_skill.update({'frequencyOfMention': ExtractedSkill.frequencyOfMention + kwargs['frequencyOfMention']})
            self.session.commit()
        else:
            new_skill = ExtractedSkill(**kwargs)
            self.session.add(new_skill)
            self.session.commit()
