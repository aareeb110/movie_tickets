import datetime
import mysql.connector
import redis
import pickle

redis_server = redis.StrictRedis(host='localhost', port=6379, db=0, password=None)


def cache_movie_info(movie_name):
    # idea is to use movie_name as the key and store all of its information in cache
    query = "select genre, movie_price, actors from Movie " \
            "where movie_name = %s"
    args = (movie_name,)

    update_flag = False

    date_a = redis_server.get(movie_name + ":time")

    if date_a is None:
        print("The data has not been cached. Retrieving from database...")
        update_flag = True
    else:
        time_a_str = str(date_a, 'utf-8')
        time_a = datetime.datetime.strptime(time_a_str, "%H:%M:%S")
        time_b = datetime.datetime.now()

        init_time = datetime.time(time_a.hour, time_a.minute, time_a.second)
        curr_time = datetime.time(time_b.hour, time_b.minute, time_b.second)

        date = datetime.date(1, 1, 1)
        datetime_1 = datetime.datetime.combine(date, init_time)
        datetime_2 = datetime.datetime.combine(date, curr_time)
        time_elapsed = datetime_2 - datetime_1

        print("time diff: ", time_elapsed.total_seconds())
        if (time_elapsed.total_seconds() / 60) >= 1:
            print("Cache entry too old, updating cache.")
            update_flag = True
        else:
            print("Cached data is recent enough.")

    if update_flag:
        conn = mysql.connector.connect(user='root', password='D@jma!2#',
                                       host='localhost', database='reservation_system',
                                       auth_plugin='mysql_native_password')
        cursor = conn.cursor()

        cursor.execute(query, args)
        data = cursor.fetchall()

        if data:
            redis_server.set(movie_name, pickle.dumps(data))
            redis_server.set(movie_name + ":time", datetime.datetime.now().strftime("%H:%M:%S"))
            print("Cache miss")
            return pickle.loads(redis_server.get(movie_name))
    else:
        print("Cache hit")
        return pickle.loads(redis_server.get(movie_name))


if __name__ == '__main__':
    print(cache_movie_info('mid slayer'))
