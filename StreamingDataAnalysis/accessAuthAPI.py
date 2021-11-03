import tweepy as tw

from StaticDataAnalysis import config as con


def getStreamingAuth():
    #The OAuth handler is initialised to access the Twitter API, since it is necessary for developers to identify themselves. The access token are set for the initialised OAuth handler.
    auth = tw.OAuthHandler(con.API_KEY, con.API_SECRET)
    auth.set_access_token(con.TOKEN_KEY, con.TOKEN_SECRET)

    #To access the Twitter API, the tweepy method is used.
    api = tw.API(auth).auth
    return api

