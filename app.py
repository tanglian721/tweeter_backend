from flask import Flask, request, Response
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

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['POST', 'DELETE'])
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
        
@app.route('/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    if request.method == 'GET':
        user_id = request.args.get("user_id")
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
        user_id = request.json.get('user_id')
        if userfunction.modifyAccount(email, username, password, birthdate, bio, url, user_id):
            return Response("Modify Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        user_id = request.json.get('user_id')
        if userfunction.deleteAccount(user_id):
            return Response("Delete Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/follows', methods=['GET', 'POST', 'DELETE'])
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
        
@app.route('/followers', methods=['GET'])
def followers():
    if request.method == "GET":
        user_id = request.args.get("userId")
        users = followfunction.getFollowers(user_id)
        if users != None:
            return Response(json.dumps(users, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if request.method == "GET": 
        user_id = request.args.get('userId')
        tweets = tweetfunction.getTweet(user_id)
        print(user_id)
        if tweets != None:
            return Response(json.dumps(tweets, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        content = request.json.get('content')
        image = request.json.get('image')
        tweet = tweetfunction.postTweet(token, content, image)
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
            
@app.route('/likes', methods=['GET', 'POST', 'DELETE'])
def tweet_likes():
    if request.method == "GET":
        tweet_id = request.args.get('tweetId')
        tweet_likes = like.getTweetLikes(tweet_id)
        if tweet_likes != None:
            return Response(json.dumps(tweet_likes, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        token = request.json.get('loginToken')
        tweet_id = request.json.get('tweetId')
        if like.postTweetLike(token, tweet_id):
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
        
@app.route('/comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def comments():
    if request.method == "GET": 
        tweet_id = request.args.get('tweetId')
        comments = commentsfunction.getComment(tweet_id)
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

@app.route('/comment-likes', methods=['GET', 'POST', 'DELETE'])
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
     


        
            
        
    
        
    
        
        
        