from flask import Flask
from flask import jsonify,request, make_response
from flask_cors import CORS
from selllllllllllll import *
from ELO import *
from sell2 import *
import time
app = Flask(__name__)
CORS(app)
@app.route('/api/random',methods=['GET'])
def random_name():
    global l
    l=np.random.choice(player_names, size=2, replace=False)
    global n
    n=l[0]
    global m
    m=l[1]
    name_details(n,m)
    query=ref.order_by_child('name').equal_to(n)
    query1=ref.order_by_child('name').equal_to(m)
    for i in query.get().values():
        type(i)
    for j in query1.get().values():
        type(i)
    global query_elo
    query_elo=i['elo']
    global query1_elo
    query1_elo=j['elo']
    query_img=i['image_path']
    query1_img=j['image_path']
    return jsonify({"data1":n,
                    "data2":m,
                    'data1_elo':query_elo,
                    'data2_elo':query1_elo,
                    'data1_img':query_img,
                    'data2_img':query1_img})
@app.route('/api/random_m',methods=['GET'])
def random_name_m():
    global l
    l=np.random.choice(player_names_m, size=2, replace=False)
    global n
    n=l[0]
    global m
    m=l[1]
    name_details_m(n,m)
    query=ref1.order_by_child('name').equal_to(n)
    query1=ref1.order_by_child('name').equal_to(m)
    for i in query.get().values():
        type(i)
    for j in query1.get().values():
        type(i)
    global query_elo
    query_elo=i['elo']
    global query1_elo
    query1_elo=j['elo']
    query_img=i['image_path']
    query1_img=j['image_path']
    return jsonify({"data1":n,
                    "data2":m,
                    'data1_elo':query_elo,
                    'data2_elo':query1_elo,
                    'data1_img':query_img,
                    'data2_img':query1_img})

@app.route('/api/rating',methods=['POST'])
def rating():
    data = request.json
    selected_name=data['s_name']
    print("The Chosen Candidates are: ",n,m)
    global final_players
    if n and m in player_names:
        final_players=player_names_m
        print(final_players)
    else:
        final_players=player_names_m
        print(final_players)
    print('The winner is: ',selected_name)
    print(final_players.index(selected_name))
    if final_players==player_names:

        if selected_name==n:
            ratings=elo(query_elo,query1_elo)
            print(ratings)
            winner_id=final_players.index(n)
            winner_rating=ratings[1]
            loser_id=final_players.index(m)
            loser_rating=ratings[0]
            update_rating(winner_id,winner_rating)
            update_rating(loser_id,loser_rating)

        elif selected_name==m:
            ratings1=elo(query1_elo,query_elo)
            print(ratings1)
            winner_id=final_players.index(m)
            winner_rating=ratings1[1]
            loser_id=final_players.index(n)
            loser_rating=ratings1[0]
            update_rating(winner_id,winner_rating)
            update_rating(loser_id,loser_rating)
        else:
            print("Error dumbass")
        return jsonify({"received": data})
    else:
        if selected_name==n:
            ratings=elo(query_elo,query1_elo)
            print(ratings)
            winner_id=final_players.index(n)
            winner_rating=ratings[1]
            loser_id=final_players.index(m)
            loser_rating=ratings[0]
            update_rating_m(winner_id,winner_rating)
            update_rating_m(loser_id,loser_rating)

        elif selected_name==m:
            ratings1=elo(query1_elo,query_elo)
            print(ratings1)
            winner_id=final_players.index(m)
            winner_rating=ratings1[1]
            loser_id=final_players.index(n)
            loser_rating=ratings1[0]
            update_rating_m(winner_id,winner_rating)
            update_rating_m(loser_id,loser_rating)
        else:
            print("Error dumbass")
        return jsonify({"received": data})


@app.route('/api/leaderboard',methods=['GET'])
def leaderboard():
    print(final_players)
    if player_names==final_players:
        order=ref.order_by_child('elo').get()
    else:
        order=ref1.order_by_child('elo').get()
    order=order[-1:-11:-1]
    l_name=[]
    l_elo=[]
    l_img=[]
    for i in order:
        l_name.append(i['name'])
        l_elo.append(i['elo'])
        l_img.append(i['image_path'])
    final_order={"name":l_name,"elo":l_elo,"image_path":l_img}
    return jsonify({"name":final_order['name'],"elo":final_order['elo'],"image_path":final_order["image_path"]})
@app.route('/api/health')
def health_check():
    return "OK", 200
if __name__ == '__main__':
    app.run(debug=True)

