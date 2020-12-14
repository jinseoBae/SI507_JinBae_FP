SI 507 Final Project Jin-Seo Bae (jinbae)

[Demo Video Link](https://drive.google.com/file/d/1MTD5pLqiz6tpp5Lv766rimMc_n7P0CT8/view?usp=sharing)

1. Both <strong>API</strong> and <strong>Secret Keys</strong> are in the main file called "main_FP.py".
2. If user want to get most recent ranking and popularity scores from <strong>Spotify</strong>, user should remove csv file in this regitory and <strong> uncomment get_spotify_csv() </strong> and re-run main_FP.py.
3. Then, user should run "flask_play.py" file in the terminal and open http://127.0.0.1:5000/ link.
4. This will lead user to ![main page](https://drive.google.com/uc?export=view&id=115MMdl-JHBVcwXKiz4Nwd_prqMSCONO-) of my final project.
5. User can ![choose](https://drive.google.com/uc?export=view&id=1iur-TcPlKvev9QjycW-19G6LfWrWQiOv) few different things.

    a. Billboard Scraping
	
        * Sorting Order: rank, track name, and aritist name
        * number of records to display: 10 records, 30 records, 50 records, and 100 records
		
    b. Spotify API
	
        * Choose Ranking number from Billboard: (any number between 1 and 100)
			-This feature help user to get detailed information about the artist that ranked number in Billboard
        * Check option for plot result
6. For Billboard Scraping, user can see different pictures of artists; number of records and sorting order that they selected from the main page.
7. For Spotify API part, user can see detailed information about an artist by typing their ranking from the billboard.
	
	* User can see other songs from same artist in billboard 
	* User can also see other songs from same artist in Spotify
	* If the artist has multiple songs ranked in Spotify, they will have "popularity score".
	* That popularity scores have used for bar chart display (y-axis and color scale).
	* User can listen top 100 songs in Billboard and Spotify that are on Youtube video.	
