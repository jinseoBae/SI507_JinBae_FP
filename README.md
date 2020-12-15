SI 507 Final Project Jin-Seo Bae (jinbae)

[Demo Video Link](https://drive.google.com/file/d/1nzG_v41dHEVO4QFt4V2e1rDjUSnRWyo-/view?usp=sharing)

1. Both <strong>API</strong> and <strong>Secret Keys</strong> are in the main file called "main_FP.py".
2. If user want to get most recent ranking and popularity scores from <strong>Spotify</strong>, user should remove csv file in this regitory and <strong> uncomment get_spotify_csv() </strong> and re-run main_FP.py.
3. Then, user should run "flask_play.py" file in the terminal and open http://127.0.0.1:5000/ link.
4. This will lead user to main page of my final project. ![main page](https://drive.google.com/uc?export=view&id=1YSbphSsSC6udiUhwXE8RVct7oB__Xylr)
5. User can choose few different things.

    a. Billboard Scraping
	
        * Sorting Order: rank, song title, and aritist name
        * number of songs to display: 10 songs, 30 songs, 50 songs, and 100 songs
		
    b. Spotify API
	
        * Choose Ranking number from Billboard: (any number between 1 and 100)
			-This feature help user to get detailed information about the artist that ranked number in Billboard
        * Check option for plot result
![choose](https://drive.google.com/uc?export=view&id=1-wlROxQMyCxeLYUAQ_VJQvd1oEZv9Vfa)

6. For Billboard Scraping, user can see different pictures of artists; number of records and sorting order that they selected from the main page.
7. For Spotify API part, user can see detailed information about an artist by typing their ranking from the billboard.
	
	* User can see other songs from same artist in billboard 
	* User can also see other songs from same artist in Spotify
	* If the artist has multiple songs ranked in Spotify, they will have "popularity score".
	* That popularity scores have used for bar chart display (y-axis and color scale).
	* User can listen top 100 songs in Billboard and Spotify that are on Youtube video.	
