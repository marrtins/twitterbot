import tweepy
import markovify
import json



# ALL YOUR SECRET STUFF!
# Consumer Key (API Key)
consumer_key = ''
# Consumer Secret (API Secret)
consumer_secret = ''
# Access Token
access_token = ''
# Access Token Secret
access_token_secret = ''




auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


user = api.me()



print (user.name)

namesToTrack=['@botgsu','@gsutiag']


class Listener(tweepy.StreamListener):

    def __init__(self):
        self.initializeListener()

    def initializeListener(self):
        # Get raw text as string.
        with open("tweets.txt") as f:
            text = f.read()

        # Build the model.
        self.text_model = markovify.Text(text)

    def on_data(self,data):
        if not data:
            return



        recvTweet=json.loads(str(data).strip())
        print(recvTweet)

        newTweet = '@' + recvTweet['user']['screen_name'] + ' '
        if(recvTweet['user']['screen_name'].lower()!='botgsu'):
            usersInMention = []
            for user in recvTweet['entities']['user_mentions']:
                userName ='@'+user['screen_name']
                if(userName.lower() != '@botgsu' and userName.lower() not in usersInMention):
                    usersInMention.append(userName)
                    newTweet=newTweet+userName+' '


            newText =self.text_model.make_short_sentence(160)



            newTweet = newTweet+newText

            print("New tweet: "+newTweet)
            if(len(usersInMention)>0):
                print("Users in mention: ")
                for user in usersInMention:
                    print(user)

            api.update_status(newTweet)






    def on_error(self,status_code):
        print("error: " + str(status_code))
        return


if __name__ == '__main__':
    listener = Listener()
    stream = tweepy.Stream(auth=auth, listener=listener)
    stream.filter(track =namesToTrack)

