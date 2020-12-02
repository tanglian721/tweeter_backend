from flask import Flask, request, Response,render_template
import mariadb
import json
import random
from datetime import datetime
from flask_cors import CORS
import userfunction
import followfunction
import tweetfunction
import like
import commentsfunction
import hashA
import messagefunction
import noticefunction
import os


app = Flask(__name__)
CORS(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/api/upload', methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, '/Users/Taylo/InnoTech/Assignments/Project/tweet_fullStack/frondend/src/assets/')
    
    if not os.path.isdir(target):
        os.mkdir(target)
    files = request.files.getlist("file")
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return Response(json.dumps(destination, default=str), mimetype="application/json", status=204)
if __name__=="__main__":
    app.run(port=4555,debug=True)


@app.route('/api/login', methods=['POST', 'DELETE'])
def login():
    if request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')
        user = userfunction.login(username, password)        
        if user != None:
            return Response(json.dumps(user, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    if request.method == "DELETE":
        token = request.json.get('loginToken')
        if userfunction.logout(token):
            return Response("Delete Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    if request.method == 'GET':
        user_id = request.args.get("userId")
        data = userfunction.getUsers(user_id)
        if data != None:
            return Response(json.dumps(data, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500) 
    elif request.method == "POST":
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        birthdate = request.json.get('birthdate')
        bio = request.json.get('bio')
        url = request.json.get('url')
        date = str(datetime.now())[0:10]
        if userfunction.signUp(email, username, password, birthdate, bio, date, url):
            user = userfunction.login(username, password)
            if user != None:
                return Response(json.dumps(user, default=str), mimetype="application/json", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        birthdate = request.json.get('birthdate')
        bio = request.json.get('bio')
        url = request.json.get('url')
        user_id = request.json.get('userId')
        user = userfunction.modifyAccount(email, username, password, birthdate, bio, url, user_id)
        if user != None:
            return Response(json.dumps(user, default=str), mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        user_id = request.json.get('user_id')
        if userfunction.deleteAccount(user_id):
            return Response("Delete Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/api/follows', methods=['GET', 'POST', 'DELETE'])
def follows():
    if request.method == "GET":
        user_id = request.args.get("userId")
        users = followfunction.getFollows(user_id)
        if users != None:
            return Response(json.dumps(users, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500) 
    elif request.method == "POST":
        token = request.json.get('loginToken')
        follow_id = request.json.get('followId')
        if followfunction.follows(token, follow_id):
            return Response("Follows Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        follow_id = request.json.get('followId')   
        if followfunction.unFollows(token, follow_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/followers', methods=['GET'])
def followers():
    if request.method == "GET":
        user_id = request.args.get("userId")
        users = followfunction.getFollowers(user_id)
        if users != None:
            return Response(json.dumps(users, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/follow-tweets', methods=['GET'])
def follow_tweet():
    if request.method == "GET":
        user_id = request.args.get("userId")
        checkuser_id = request.args.get('checkuserId')
        print(user_id)
        tweets = tweetfunction.followTweets(user_id,checkuser_id)
        if users != None:
            return Response(json.dumps(tweets, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if request.method == "GET": 
        user_id = request.args.get('userId')
        checkuser_id = request.args.get('checkuserId')
        index = request.args.get("index")
        tweet_id = request.args.get("tweetId")
        if tweet_id != None:
           tweets = tweetfunction.getOneTweet(tweet_id)
        else: 
            tweets = tweetfunction.getTweet(user_id, index, checkuser_id)
        if tweets != None:
            return Response(json.dumps(tweets, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        image = request.json.get('image')
        retweet_id = request.json.get('retweetId')
        tweet = tweetfunction.postTweet(token, content, image, retweet_id)
        if tweet != None:
            return Response(json.dumps(tweet, default=str), mimetype="application/json", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        image = request.json.get('image')
        tweet_id = request.json.get('tweetId')
        tweet = tweetfunction.editTweet(token, content, image, tweet_id)
        if tweet != None:
            return Response(json.dumps(tweet, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        if tweetfunction.deleteTweet(token, tweet_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
            
@app.route('/api/likes', methods=['GET', 'POST',"PATCH", 'DELETE'])
def tweet_likes():
    if request.method == "GET":
        tweet_id = request.args.get('tweetId')
        # user_id = request.args.get('userId')
        tweet_likes = like.getTweetLikes(tweet_id)
        if tweet_likes != None:
            return Response(json.dumps(tweet_likes, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        if like.postTweetLike(token, tweet_id):
            return Response("likes Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    if request.method == "PATCH":
        token = request.json.get('loginToken')
        tweet_id = request.json.get("tweetId")
        print(tweet_id)
        if like.editTweetLike(token, tweet_id):
            return Response("Likes Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        if like.deleteTweetLike(token, tweet_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def comments():
    if request.method == "GET": 
        tweet_id = request.args.get('tweetId')
        user_id = request.args.get('userId')
        comments = commentsfunction.getComment(tweet_id, user_id)
        if tweets != None:
            return Response(json.dumps(comments, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        image = request.json.get('image')
        tweet_id = request.json.get('tweetId')
        comments = commentsfunction.postComment(token, tweet_id, content, image)
        if comments != None:
            return Response(json.dumps(comments, default=str), mimetype="application/json", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        image = request.json.get('image')
        comment_id = request.json.get('commentId')
        comments = commentsfunction.editComment(token, comment_id, content, image)
        if comments != None:
            return Response(json.dumps(comments, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        comment_id = request.json.get('commentId')
        if commentsfunction.deleteComment(token, comment_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/com-comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def com_comments():
    if request.method == "GET": 
        comment_id = request.args.get('commentId')
        user_id = request.args.get('userId')
        comments = commentsfunction.getCom_comment(comment_id, user_id)
        if comments != None:
            return Response(json.dumps(comments, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        comment_id = request.json.get('commentId')
        comments = commentsfunction.postCom_comment(token, comment_id, content)
        if comments != None:
            return Response(json.dumps(comments, default=str), mimetype="application/json", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        com_comment_id = request.json.get('com_commentId')
        comments = commentsfunction.editCom_comment(token, com_comment_id, content)
        if comments != None:
            return Response(json.dumps(comments, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        com_comment_id = request.json.get('com_commentId')
        if commentsfunction.deleteCom_comment(token, com_comment_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/api/comment-likes', methods=['GET', 'POST', 'DELETE'])
def comment_likes():
    if request.method == "GET":
        comment_id = request.args.get('commentId')
        comment_likes = like.getCommentLikes(comment_id)
        if comment_likes != None:
            return Response(json.dumps(comment_likes, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        comment_id = request.json.get('commentId')
        if like.postCommentLike(token, comment_id):
            return Response("Likes Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        comment_id = request.json.get('commentId')
        if like.deleteCommentLike(token, comment_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/com-comment-likes', methods=['GET', 'POST', 'DELETE'])
def com_comment_likes():
    if request.method == "GET":
        com_comment_id = request.args.get('com_commentId')
        com_comment_likes = like.getCom_commentLikes(com_comment_id)
        if com_comment_likes != None:
            return Response(json.dumps(com_comment_likes, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        com_comment_id = request.json.get('com_commentId')
        if like.postCom_commentLike(token, com_comment_id):
            return Response("Likes Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        com_comment_id = request.json.get('com_commentId')
        if like.deleteCom_commentLike(token, com_comment_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/api/@', methods=['GET', 'POST', 'PATCH'])
def Auser():    
    if request.method == "GET":
        user_id = request.args.get('userId')
        checkuser_id = request.args.get('checkuserId')
        tweets = hashA.getTweets(user_id, checkuser_id)
        if tweets != None:
            return Response(json.dumps(tweets, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        at_id = request.json.get('atId')
        print(tweet_id)
        if hashA.postAuser(token, tweet_id, at_id):
            return Response("@ Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        if hashA.editAuser(token, tweet_id):
            return Response("Edit Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/api/message', methods=['GET', 'POST', 'PATCH'])
def message():
    if request.method == "GET":
        user_id = request.args.get('userId')
        chatwith_id = request.args.get("chatwithId")
        messages = messagefunction.getmessages(user_id, chatwith_id)
        if messages != None:
            return Response(json.dumps(messages, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        receiver_id = request.json.get('receiverId')
        content = request.json.get('content')
        print(receiver_id)
        print(content)
        message = messagefunction.postMessage(token, receiver_id, content)
        if message != None:
            return Response(json.dumps(message, default=str), mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        token = request.json.get('loginToken')
        message_id = request.json.get('messageId')
        print(message_id)
        if messagefunction.editMessage (token, message_id):
            return Response("Edit Success!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
         
@app.route('/api/hash', methods=['GET',"POST", "PATCH", "DELETE"])
def hash():
    if request.method == "GET":
        hashTag = request.args.get("hashTag")
        user_id = request.args.get('userId')
        print(hashTag)
        if hashTag == None:
            hash = hashA.getHash()
        else:
            hash = hashA.getHashTweet(hashTag, user_id)
        if hash != None:
            return Response(json.dumps(hash, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        print("a")
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        hashtag = request.json.get('hash')
        print(hashtag)
        if hashA.postHash(token, tweet_id, hashtag):
             return Response("POST succuss!", mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        oldhash = request.json.get('hash')
        newhash = request.json.get('newhash')
        if hashA.editHash(token, tweet_id, oldhash, newhash):
             return Response("Edit succuss!", mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        oldhash = request.json.get('hash')
        if hashA.deleteHash(token, tweet_id, oldhash):
             return Response("Delete succuss!", mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/api/search', methods=['GET'])
def search_tweet():
    if request.method == "GET":
        searchContent = request.args.get("searchContent")
        checkuser_id = request.args.get('checkuserId')
        print(searchContent)
        tweets = tweetfunction.search(searchContent,checkuser_id)
        if users != None:
            return Response(json.dumps(tweets, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        

        
        

        
             


     


        
            
        
    
        
    
        
        
        