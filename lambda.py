import json,base64,os
from urllib.request import urlopen

def lambda_handler(event, context):
    x = '/control/go?arg=' + event["request"]["intent"]["name"] + '&user=' + os.environ['envUser'] + '&password=' + os.environ['envPass']
    print(x)
    #https://ejsmith.hopto.org/control/go?arg=on&user=?&password=?

    y = "https://ejsmith.hopto.org:443" + x
    #res = urllib2.Request("https://ejsmith.hopto.org:443" + x)
    #base64str = base64.encodestring('%s:%s' % (os.environ['env_user'], os.environ['env_pass'])).replace('\n','')
    #res.add_header("Authorization", "Basic %s" % base64str)
    #resp = urllib2.urlopen(res)
    resp2 = urllib2.urlopen(y)
    #return resp
    return {
        "statusCode": 200,
        "body": json.dumps('success'),
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "yeet",
                "playBehavior": "REPLACE_ENQUEUED"
            },
        }
    }
def testfunc():
    x = '/control/go?arg=' + 'on' + '&user=' + '?' + '&password=' + '?'
    #x = '/About?' + 'user=' + '?' + '&password=' + '?'
    #x= '/About'
    y = "https://ejsmith.hopto.org:443" + x
    #y='192.1:80' + x
    print(y)
    resp2 = urlopen(y).read()
    print(resp2)
    return resp2

testfunc()
