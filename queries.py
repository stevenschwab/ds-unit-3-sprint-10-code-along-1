# Create a new table in the database called "Stores"
# | city          | state | employees | website | curbside |
# |---------------|-------|-----------|---------|----------|
# | New York      | NY    | 8         | 1       | 1        |
# | Los Angeles   | CA    | 11        | 0       | 1        |
# | Seattle       | WA    | 7         | 1       | 0        |
# | San Francisco | CA    | 5         | 0       | 0        |

# Drop the table so that we can run
# connect.py without side effects from previous
# times that we executed the script.
DROP_STORES = '''
    DROP TABLE IF EXISTS Stores;
'''

MAKE_STORES = '''
    CREATE TABLE IF NOT EXISTS Stores (
        city CHAR(200),
        state CHAR(2),
        employees INT,
        website INT,
        curbside INT
    );
'''

INSERT_STORES = """
    INSERT INTO Stores (city, state, employees, website, curbside)
    VALUES (?, ?, ?, ?, ?)
"""

# Verify that the table was created correctly
CHECK_STORES = '''
    SELECT name FROM sqlite_master WHERE type='table' AND name='Stores';
'''

# How many rows are in the table?
NUM_ROWS = '''
    SELECT COUNT(*) as row_count FROM Stores;
'''

# How many Stores have a website and curbside pickup?
WEBSITE_AND_CURBSIDE = '''
    SELECT COUNT(*) 
    FROM Stores
    WHERE website = 1 AND curbside = 1;
'''

# How many stores have more than 10 employees and curbside pickup?
TEN_AND_CURBSIDE = '''
    SELECT COUNT(*) 
    FROM Stores
    WHERE employees > 10 and curbside = 1;
'''

# How many states have stores?
NUM_STATES = '''
    SELECT COUNT(DISTINCT state)
    FROM Stores;
'''

# How many tracks?
NUM_TRACKS = '''
    SELECT COUNT(*)
    FROM tracks;
'''

# How many Genres?
NUM_GENRES = '''
    SELECT COUNT(*)
    FROM genres;
'''

# How many Albums?
NUM_ALBUMS = """
    SELECT COUNT(*)
    FROM albums;
"""

# How many Artists?
NUM_ARTISTS = """
    SELECT COUNT(*)
    FROM artists;
"""

# What is the Genre with the greatest number of albums?
MOST_ALBUMS_GENRE = '''
    WITH albums_by_genre AS (
        SELECT g.Name, COUNT(DISTINCT t.AlbumId) AS album_count
        FROM tracks t
        INNER JOIN genres g ON t.GenreId = g.GenreId
        GROUP BY g.GenreId
    )
    SELECT *
    FROM albums_by_genre
    WHERE album_count = (SELECT MAX(album_count) FROM albums_by_genre)
'''

# What is then name of the artist that has written the most albums?
MOST_ALBUMS_ARTIST = '''
    WITH album_count_by_artist AS (
        SELECT ar.Name, COUNT(al.AlbumId)  AS album_count
        FROM albums al
        INNER JOIN artists ar ON al.ArtistId = ar.ArtistId
        GROUP BY al.ArtistId
    )
    SELECT *
    FROM album_count_by_artist
    WHERE album_count = (SELECT MAX(album_count) FROM album_count_by_artist)
'''

# What is the name of the playlist with the longest runtime?
LONGEST_PLAYLIST = '''
    WITH playlist_length_by_name AS (
        SELECT p.PlaylistId, p.Name, SUM(t.Milliseconds) as playlist_length
        FROM playlists p
        LEFT JOIN playlist_track pt ON p.PlaylistId = pt.PlaylistId
        LEFT JOIN tracks t ON pt.TrackId = t.TrackId
        GROUP BY p.PlaylistId
    )
    SELECT Name, playlist_length
    FROM playlist_length_by_name
    WHERE playlist_length = (SELECT MAX (playlist_length) FROM playlist_length_by_name)
    LIMIT 1;
'''

# What is the name of the artist that writes the shortest songs –on average?
SHORT_SONG_ARTIST = '''
    WITH avg_artist_song_length AS (
        SELECT ar.ArtistId, ar.Name, AVG(t.Milliseconds) AS avg_song_length
        FROM tracks t
        INNER JOIN albums a ON t.AlbumId = a.AlbumId
        INNER JOIN artists ar ON a.ArtistId = ar.ArtistId
        GROUP BY ar.ArtistId
    )
    SELECT Name, avg_song_length
    FROM avg_artist_song_length
    WHERE avg_song_length = (SELECT MIN(avg_song_length) FROM avg_artist_song_length)
'''

# Which employee has been the Support Rep for the greatest number of customers?
BUSIEST_SUPPORT_REP = '''
    WITH customers_by_employee AS (
        SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName as employee_name, COUNT(c.CustomerId) as customer_length
        FROM employees e
        LEFT JOIN customers c ON e.EmployeeId = c.SupportRepId
        GROUP BY e.EmployeeId
    )
    SELECT employee_name, customer_length
    FROM customers_by_employee
    WHERE customer_length = (SELECT MAX(customer_length) FROM customers_by_employee)
'''

# What is the shortest track?
SHORTEST_TRACK = '''
    SELECT *
    FROM tracks
    WHERE Milliseconds = (SELECT MIN(Milliseconds) FROM tracks);
'''

# What is the longest track?
LONGEST_TRACK = '''
    SELECT *
    FROM tracks
    WHERE Milliseconds = (SELECT MAX(Milliseconds) FROM tracks);
'''

# How many tracks are longer than 5 minutes?
LONG_TRACKS = '''
    SELECT COUNT(*)
    FROM tracks
    WHERE Milliseconds / 60000.0 > 5.0;
'''

# Who is the composer with the most tracks?
# IF *NULL* is an acceptable answer
PROLIFIC_COMPOSER_NULL = '''
    WITH track_counts AS (
        SELECT Composer, COUNT(*) AS track_count
        FROM tracks
        GROUP BY Composer
    )
    SELECT Composer, track_count
    FROM track_counts
    WHERE track_count = (SELECT MAX(track_count) FROM track_counts);
'''

# Who is the composer with the most tracks?
# IF *NULL* is not an acceptable answer
# WHERE can be used BEFORE a GROUP BY, but not after
# after a GROUP BY we use HAVING
PROLIFIC_COMPOSER = '''
    WITH track_counts AS (
        SELECT Composer, COUNT(Composer) AS track_count
        FROM tracks
        GROUP BY Composer
    )
    SELECT Composer, track_count
    FROM track_counts
    WHERE track_count = (SELECT MAX(track_count) FROM track_counts);
'''

# How many composers have more than 10 tracks?
MORE_THAN_TEN = '''
    WITH track_counts AS (
        SELECT Composer, COUNT(Composer) AS track_count
        FROM tracks
        GROUP BY Composer
        HAVING track_count > 10
    )
    SELECT COUNT(*)
    FROM track_counts;
'''

QUERY_LIST = [DROP_STORES,
              MAKE_STORES,
              INSERT_STORES,
              CHECK_STORES,
              NUM_ROWS,
              WEBSITE_AND_CURBSIDE,
              TEN_AND_CURBSIDE,
              NUM_STATES,
              NUM_TRACKS,
              NUM_GENRES,
              NUM_ALBUMS,
              NUM_ARTISTS,
              MOST_ALBUMS_GENRE,
              MOST_ALBUMS_ARTIST,
              LONGEST_PLAYLIST,
              SHORT_SONG_ARTIST,
              BUSIEST_SUPPORT_REP,
              SHORTEST_TRACK,
              LONGEST_TRACK,
              LONG_TRACKS,
              PROLIFIC_COMPOSER_NULL,
              PROLIFIC_COMPOSER,
              MORE_THAN_TEN]