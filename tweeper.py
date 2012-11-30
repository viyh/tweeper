# tweeper: twitter auto-follow/unfollow script
# https://github.com/viyh/tweeper

# SET THESE
username               = ''
consumer_key           = ''
consumer_secret        = ''
access_token_key       = ''
access_token_secret    = ''

#####
#####
#####

import pkg_resources
import tweepy
import sys

print "tweeper v0.0.1\n"
print "\nUsing tweepy version [%s]\n" % pkg_resources.get_distribution('tweepy').version

debug    = False

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback=None, secure=True)
auth.set_access_token(access_token_key, access_token_secret)

api_auth = tweepy.API(auth)
api      = tweepy.API()

try:
    print "Getting followers..."
    fo = api.followers_ids(username)
    print "\t[%s] followers found." % fo.__len__()
    print "\nGetting friends..."
    fr = api.friends_ids(username)
    print "\t[%s] friends found." % fr.__len__()
    print "\nFinding followers to follow..."
    for f in fo:
        if f not in fr:
            try:
                if not debug:
                    api_auth.create_friendship(f)
                print "\tFollowing: %s" % api.get_user(f).screen_name
            except Exception, e:
                if debug:
                    print "\tError: %s" % str(e)
                pass
    print "\nFinding friends to unfollow..."
    for f in fr:
        if f not in fo:
            if not debug:
                api_auth.destroy_friendship(f)
            print "\tUnfollowing: %s" % api.get_user(f).screen_name
except tweepy.error.TweepError, e:
    print "Error: %s" % str(e)
    sys.exit()
finally:
    auth_rate_limit = api_auth.rate_limit_status()
    limit  = auth_rate_limit['hourly_limit']
    remain = auth_rate_limit['remaining_hits']
    reset  = auth_rate_limit['reset_time']
    print '\nAuthenticated API calls left this hour:  %s of %s' % (remain, limit)
    print 'Authenticated API call limit reset time: %s\n' % (reset)

    rate_limit = api.rate_limit_status()
    limit  = rate_limit['hourly_limit']
    remain = rate_limit['remaining_hits']
    reset  = rate_limit['reset_time']
    print 'Unauthenticated API calls left this hour:  %s of %s' % (remain, limit)
    print 'Unauthenticated API call limit reset time: %s\n' % (reset)
