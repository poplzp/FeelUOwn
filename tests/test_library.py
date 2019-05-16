import pytest


def test_library_search(library):
    result = list(library.search('xxx'))[0]
    assert len(result.songs) >= 3
    assert result.songs[0].identifier == 1


@pytest.mark.asyncio
async def test_library_a_search(library):
    result = (await library.a_search('xxx'))[0]
    assert result.q == 'xxx'


def test_library_list_songs_standby(library, song):
    songs = library.list_song_standby(song)

    # all songs share the same provider,
    # so there will be no standby song
    assert len(songs) == 0

    song.source = 'dummy-1'
    songs = library.list_song_standby(song)
    assert len(songs) == 1

    songs = library.list_song_standby(song, onlyone=False)
    assert len(songs) == 2


@pytest.mark.asyncio
async def test_library_a_list_songs_standby(library, song):
    songs = await library.a_list_song_standby(song)
    assert len(songs) <= 1

    song.source = 'dummy-1'
    songs = await library.a_list_song_standby(song)
    assert len(songs) == 1
