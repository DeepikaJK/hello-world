from textblob import TextBlob
import sys, tweepy, re, csv
import matplotlib.pyplot as pt


class DataAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def RetrieveData(self):
        # Authentication
        consumerKey = 'lljqkDZ5WEtE6gjtZ112EeTp2'
        consumerSecret = '9IMN1C590oT4koMBFdins8bPafu41InJHngI2t79WEPAHrzBKw'
        accessToken = '2583763406-wVwKXk5tImkIUBxmPioepCtP5aqrrYODE305BsW'
        accessTokenSecret = 'O5UQAQRLUoz5yFiSykgC2fmy3BdiLRqEKOsjm8dDxxMIh'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # Input for what word and how many tweets to search
        searchWord = input("Enter Keyword/HashTag to search: ")
        NoOfTweet = int(input("Enter how many tweets to search: "))

        # Searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchWord, lang="en").items(NoOfTweet)

        # Open/create a file to append data
        csvFile = open('result.csv', 'a')
        csvWriter = csv.writer(csvFile)

        # Creating variables for storing the analysed data
        polarity = 0
        positive = 0
        weakpositive = 0
        strongpositive = 0
        negative = 0
        weaknegative = 0
        strongnegative = 0
        neutral = 0

        # Fetching tweets
        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                weakpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                strongpositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                weaknegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                strongnegative += 1

        # Write to csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # Finding average of people's reaction
        positive = self.percentage(positive, NoOfTweet)
        weakpositive = self.percentage(weakpositive, NoOfTweet)
        strongpositive = self.percentage(strongpositive, NoOfTweet)
        negative = self.percentage(negative, NoOfTweet)
        weaknegative = self.percentage(weaknegative, NoOfTweet)
        strongnegative = self.percentage(strongnegative, NoOfTweet)
        neutral = self.percentage(neutral, NoOfTweet)

        polarity = polarity / NoOfTweet

        # Displaying Data
        print("How people are reacting on " + searchWord + " by analyzing " + str(NoOfTweet) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Data Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(weakpositive) + "% people thought it was weakly positive")
        print(str(strongpositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(weaknegative) + "% people thought it was weakly negative")
        print(str(strongnegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotPieChart(positive, weakpositive, strongpositive, negative, weaknegative, strongnegative, neutral,
                          searchWord, NoOfTweet)

    def cleanTweet(self, tweet):
        # Remove Special Characters, links and etc from tweets
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # Calculating percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, weakpositive, strongpositive, negative, weaknegative, strongnegative, neutral,
                     searchWord, noOfSearchTerm):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(weakpositive) + '%]',
                  'Strongly Positive [' + str(strongpositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(weaknegative) + '%]',
                  'Strongly Negative [' + str(strongnegative) + '%]']
        sizes = [positive, weakpositive, strongpositive, neutral, negative, weaknegative, strongnegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = pt.pie(sizes, colors=colors, startangle=90)
        pt.legend(patches, labels, loc="best")
        pt.title('How people are reacting on ' + searchWord + ' by analyzing ' + str(noOfSearchTerm) + ' Tweets.')
        pt.axis('equal')
        pt.tight_layout()
        pt.show()


if __name__ == "__main__":
    da = DataAnalysis()
    da.RetrieveData()
