from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer
from sqlalchemy.types import PickleType
from sqlalchemy.types import String

Base = declarative_base()


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filepath = Column(String)

    def __repr__(self):
        return f"Document(id={self.id}, filename=\"{self.filename}\", filepath=\"{self.filepath}\")"

class DocumentSnapshot(Base):
    __tablename__ = 'doc_snapshots'
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey('documents.id'))
    hash = Column(String)
    date_parsed = Column(DateTime)

    def __repr__(self):
        return f"DocumentSnapshot(id={self.id}, doc_id={self.doc_id}, hash=\"{self.hash}\", date_parsed={self.date_parsed})"

class DocumentEmbedding(Base):
    __tablename__ = 'doc_embeddings'
    id = Column(Integer, primary_key=True)
    snapshot_id = Column(Integer, ForeignKey('doc_snapshots.id'))
    snapshot = relationship('DocumentSnapshot')
    embeddings = Column(PickleType)

    def __repr__(self):
        return f"DocumentEmbedding(id={self.id}, snapshot_id={self.snapshot_id}, embeddings={self.embeddings})"
