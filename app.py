from flask import Flask
from flask import jsonify,request, make_response
from flask_cors import CORS
from selllllllllllll import *
from ELO import *
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

@app.route('/api/rating',methods=['POST'])
def rating():
    data = request.json
    selected_name=data['s_name']
    print(selected_name)
    print(player_names.index(selected_name))
    print(n,m)
    order=ref.order_by_child('elo').get()
    order_name=[]
    for i in order:
        order_name.append(i['name'])
    print(order_name[::-1])
    if selected_name==n:
        ratings=elo(query_elo,query1_elo)
        print(ratings)
        winner_id=player_names.index(n)
        winner_rating=ratings[1]
        loser_id=player_names.index(m)
        loser_rating=ratings[0]
        update_rating(winner_id,winner_rating)
        update_rating(loser_id,loser_rating)


    elif selected_name==m:
        ratings1=elo(query1_elo,query_elo)
        print(ratings1)
        winner_id=player_names.index(m)
        winner_rating=ratings1[1]
        loser_id=player_names.index(n)
        loser_rating=ratings1[0]
        update_rating(winner_id,winner_rating)
        update_rating(loser_id,loser_rating)
    else:
        print("Error dumbass")
    return jsonify({"received": data})
@app.route('/api/leaderboard',methods=['GET'])
def leaderboard():
    order=ref.order_by_child('elo').get()
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
