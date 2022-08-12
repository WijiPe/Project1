sleep 30
echo "Script start"
mysql --user="root" --database="mywatchlist_schema" --password="root" < /mysql/mywatchlist_schema_follows.sql
mysql --user="root" --database="mywatchlist_schema" --password="root" < /mysql/mywatchlist_schema_movie_list.sql
mysql --user="root" --database="mywatchlist_schema" --password="root" < /mysql/mywatchlist_schema_movie_on_list.sql
mysql --user="root" --database="mywatchlist_schema" --password="root" < /mysql/mywatchlist_schema_users.sql