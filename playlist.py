from dataclasses import dataclass, field

from constants import PLAYLIST_URL_BEGINNING

@dataclass
class Song:
    name: str = field()
    artist: str = field()


@dataclass
class Playlist:
    url: str = field()
    name: str = field()
    length: int = field()
    songs: list = field(default_factory = list, repr=False)

    @staticmethod
    def check_url_validity(url) -> bool:
        return url.startswith(PLAYLIST_URL_BEGINNING)


#p = Playlist("https://open.spotify.com/playlist/23wG5Cdc2rU9DsfTlAg4ij?si=5f84561f1b054c3c", "a", 3)
#print(repr(p))

#s1 = Song("a", "b")
#s2 = Song("b", "b")
#l = [s1]

#print(s2 in l)
