# -*- coding: utf-8 -*-

import sys
import spotify

token = "BQAcKhawWu311hnccJ0LTVoeZ4R05h6sXeeurRSLS0OMUKjjJcP-TRrHpVmPpPyOpJnW4KwrVBDCjxA1QkVbQUyQbji4WnY4LRJvmxJTCCLjLfuxfZbf6Ch6XsazCTsG8N5l_R6-HK3bINpaj8MNfbOPuaIvFG0ING_ymvP6SE3mPEfJvj4xUPmfGdHNwJk5MVKaXuBlEBuvCejZavtzlztmnBglFoAbTOCSF30Ne4aUxkND4jAQHCf4qiIX5Q-JIJsXfgVU3nl2glic7uZLGjtDWQgSsqYofdgtHOE9HutvBOHE72JQ__9L5bSEZSArqbA"

user = 11145058

application = spotify.spotify(token, user)

print application.getHistory()