from sqlalchemy import create_engine, Column, String, Integer, Date, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class SearchVolumeKeywordGenerator(Base):
    __tablename__ = 'searchvolume_keyword_generator'
    
    __table_args__ = (
        UniqueConstraint('seed_keyword', 'keyword', 'month', name='uix_seed_keyword_keyword_month'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    seed_keyword = Column(String)
    keyword = Column(String)
    avg_monthly_searches = Column(Integer)
    competition = Column(String)
    competition_index = Column(Integer)
    month = Column(Date)
    monthly_searches = Column(Integer)
    cpc = Column(Float)
    low_range_bid = Column(Float)
    high_range_bid = Column(Float)
    keyword_annotation = Column(String)
    brand_bool = Column(String)
    concept_group = Column(String)
    concept_name = Column(String)
    language_id = Column(Integer)
    location_id = Column(Integer)


Session = sessionmaker()

