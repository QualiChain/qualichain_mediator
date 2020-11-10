from sqlalchemy import Column, Integer, String, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

from settings import ENGINE_STRING

Base = declarative_base()


class ExtractedSkill(Base):
    """Extracted Skills Table"""
    __tablename__ = 'extracted_skill_temp'

    id = Column(Integer, primary_key=True, nullable=False)
    job_name = Column(String(1024), nullable=True)
    skill = Column(String(1024), nullable=True)
    frequencyOfMention = Column(Integer, nullable=True)
    kind = Column(String(1024), nullable=True)

    def __repr__(self):
        return '<ExtractedSkill name: {}, job_name: {}>'.format(self.skill, self.job_name)


class ExtractedCourseSkill(Base):
    """Extracted Course Skills Table"""
    __tablename__ = 'skills_courses'

    id = Column(Integer, primary_key=True, nullable=False)
    skill_id = Column(Integer, nullable=True)
    course_id = Column(Integer, nullable=True)

    def __repr__(self):
        return '<ExtractedSkill id: {}, course_id: {}>'.format(self.skill_id, self.course_id)


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


    def upsert_new_skill_per_course(self,**kwargs):
        """
                This function is used to append a new skill per course
                :param kwargs: provided kwargs
                :return: None
                """
        this_skill = self.session.query(ExtractedCourseSkill).filter_by(
            course_id=int(kwargs['course_id']),
            skill_id=int(kwargs['skill_id'])
        )


        if this_skill.count():
            pass
        else:
            new_skill = ExtractedCourseSkill(**kwargs)
            self.session.add(new_skill)
            self.session.commit()




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

    def insert_job_post(self, **kwargs):
        """This function is used to insert a CSV file that contains information about job posts"""
        file_path = kwargs['file_path']
        table_name = 'job_post'

        jobs_df = pd.read_csv(file_path)
        jobs_df.requirements.fillna(jobs_df.full_text, inplace=True)

        jobs_df.to_sql(table_name, con=self.engine, index=False)
