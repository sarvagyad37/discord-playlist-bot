import unittest
import unittest.mock
import configparser
import sys
sys.path.insert(0, '..')
from ytmusicapi.ytmusic import YTMusic  # noqa: E402

config = configparser.RawConfigParser()
config.read('./test.cfg', 'utf-8')


class TestYTMusic(unittest.TestCase):
    @classmethod
  
    def setUpClass(cls):
        cls.yt = YTMusic(requests_session=False)
        
    def test_init(self):
        self.assertRaises(Exception, YTMusic, "{}")

    #def test_search(self):
        #query = "Taylor Swift - Look What You Made Me Do"
        #self.assertRaises(Exception, self.yt_auth.search, query, "song")
        #results = self.yt.search(query,"songs")
        #print(results[0])
    
    def make_playlist(self):
        query = "fool // cavetown lyrics"
        ytmusic = YTMusic('headers_auth.json')
        playlistId = ytmusic.create_playlist("test", "test description")
        search_results = ytmusic.search(query, "songs")
        ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])
        print(playlistId)
        pl=YTMusic.get_playlist()
        
if __name__ == '__main__':
    unittest.main()