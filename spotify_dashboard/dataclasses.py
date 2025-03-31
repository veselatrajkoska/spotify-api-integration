from dataclasses import dataclass

@dataclass
class Playlist():
    id: str
    name: str
    description: str
    image: str
    number_of_tracks: int
    url: str


@dataclass
class Category():
    id: str
    name: str
    icon: str


@dataclass
class Album():
    id: str
    name: str
    artists: list[str]
    image: str
    release_date: str
    url: str