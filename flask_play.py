import sqlite3
from flask import Flask, render_template, request
import plotly.graph_objects as go

flask_play = Flask(__name__)

def get_top_songs(by,range_):
    conn = sqlite3.connect('song_track.sqlite')
    cur = conn.cursor()

    if by == 'ranking':
        column = 'Rank'
    elif by == 'track name':
        column = 'Track_Name'
    else:
         column = 'Artist_Name'
    
    if range_ == 'All':
        range_nm = 100
    elif range_ == '50':
        range_nm = 50
    elif range_ == '30':
        range_nm = 30
    elif range_ == '10':
        range_nm = 10
 

    db = f'''
        SELECT Track_Name, Artist_Name, Rank
        FROM BillboardTracks
        ORDER BY {column}
        LIMIT {range_nm}
    '''
    topsongs = cur.execute(db).fetchall()
    conn.close()
    return topsongs

def get_detailedinfo(rank):
    conn = sqlite3.connect('song_track.sqlite')
    cur = conn.cursor()
    
    db = f'''
        SELECT Track_Name, Artist_Name, Rank
        FROM BillboardTracks
        WHERE Artist_Name == (SELECT Artist_Name FROM BillboardTracks
                             WHERE RANK == {rank})
    '''
    detailedinfo = cur.execute(db).fetchall()
    conn.close()
    return detailedinfo

def get_spotify_values(rank):
    conn = sqlite3.connect('song_track.sqlite')
    cur = conn.cursor()
    
    db = f'''
        SELECT SpotifyTracks.artist_name, SpotifyTracks.track_name, SpotifyTracks.popularity
        FROM SpotifyTracks 
        WHERE SpotifyTracks.artist_name == (SELECT Artist_Name FROM BillboardTracks
                             WHERE Rank == {rank})
    '''
    spotify = cur.execute(db).fetchall()
    def myFunc(e):
        return e[2]
    spotify.sort(key = myFunc,reverse=True)
    conn.close()
    return spotify

@flask_play.route('/')
def index():
    return render_template('index.html')


@flask_play.route('/topsongs', methods=['POST'])
def topsongs():
    sort_by = request.form['sort']
    sort_range = request.form['region']
    topsongs = get_top_songs(sort_by, sort_range)
    return render_template('topsongs.html', 
        sort=sort_by, topsongs=topsongs,region= sort_range)

@flask_play.route('/detailedinfo', methods=['POST'])
def detailedinfo():
    rank_number = request.form["number"]
    detailedinfo = get_detailedinfo(rank_number)
    spotify = get_spotify_values(rank_number)
    plot = request.form.get('plot', False)
    if (plot):
        x_vals = [r[1] for r in spotify]
        y_vals = [r[2] for r in spotify]

        bars_data = go.Bar(
            x=x_vals,
            y=y_vals,
            marker = {'color':y_vals, 'colorbar':dict(),'showscale':True,'colorscale':'Viridis'})
        
        layout = go.Layout(
            title = detailedinfo[0][1]+"'s Bar Chart on Popularity",
            xaxis=dict(
                title="Song Title",
                color = "black"
            ),
            yaxis=dict(
                title="Popularity",
                color = "black"
            ),)

        fig = go.Figure(data=bars_data,layout=layout)
        div = fig.to_html(full_html=False)

        return render_template('detailedinfo.html',number=rank_number, detailedinfo=detailedinfo,spotify=spotify, plot_div=div)
    else:
        return render_template('detailedinfo.html', number=rank_number, detailedinfo=detailedinfo,spotify=spotify)


if __name__ == '__main__':
    flask_play.run(debug=True)