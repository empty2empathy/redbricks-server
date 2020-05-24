from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER, TINYINT
from sqlalchemy.orm import relationship
from ..modules.database import Base


class Artist(Base):
    __tablename__ = "artist"

    artist_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(128, "utf8mb4_unicode_ci"))
    bio = Column(Text(collation="utf8mb4_unicode_ci"))
    profile_image = Column(String(128, "utf8mb4_unicode_ci"))
    instagram_id = Column(String(128, "utf8mb4_unicode_ci"))


class Location(Base):
    __tablename__ = "location"

    location_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(128, "utf8mb4_unicode_ci"))
    map_url = Column(String(256, "utf8mb4_unicode_ci"))
    instagram_id = Column(String(128, "utf8mb4_unicode_ci"))
    description = Column(Text(collation="utf8mb4_unicode_ci"))

    events = relationship("Event")


class ProgramType(Base):
    __tablename__ = "program_types"

    type_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(32, "utf8mb4_unicode_ci"), nullable=False, unique=True)
    disable = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class Event(Base):
    __tablename__ = "event"

    event_id = Column(INTEGER(11), primary_key=True)
    title = Column(String(512, "utf8mb4_unicode_ci"))
    price = Column(INTEGER(11), server_default=text("'0'"))
    pay_type = Column(ENUM("ticket", "entrance"))
    youtube_id = Column(String(64, "utf8mb4_unicode_ci"))
    description = Column(Text(collation="utf8mb4_unicode_ci"))
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    location_id = Column(
        ForeignKey("location.location_id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )

    location = relationship("Location")
    artists = relationship(
        "Artist",
        secondary="rel_artist_event",
        secondaryjoin="RelArtistEvent.artist_id == Artist.artist_id",
    )


class RelArtistProgramType(Base):
    __tablename__ = "rel_artist_program_type"

    relation_id = Column(INTEGER(11), primary_key=True)
    type_id = Column(
        ForeignKey("program_types.type_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    artist_id = Column(
        ForeignKey("artist.artist_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    artist = relationship("Artist")
    type = relationship("ProgramType")


class RelArtistEvent(Base):
    __tablename__ = "rel_artist_event"

    relation_id = Column(INTEGER(11), primary_key=True)
    artist_id = Column(
        ForeignKey("artist.artist_id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    event_id = Column(
        ForeignKey("event.event_id", ondelete="CASCADE", onupdate="CASCADE"), index=True
    )

    artist = relationship("Artist")
    event = relationship("Event")
