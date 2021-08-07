import pymysql
from dbconfig import MySQL
from app import app
from flask import jsonify, request
from contextlib import closing


@app.route('/search/<int:movie_id>')
def search(movie_id):
    query = "select movie_name from Movie " \
            "where id = %s"
    args = (movie_id,)

    try:
        with closing(MySQL.connect()) as conn:
            with closing(conn.cursor(pymysql.cursors.DictCursor)) as cursor:
                cursor.execute(query, args)
                row = cursor.fetchone()
                response = jsonify(row)
                response.status_code = 200
                return response
    except Exception as e:
        app.logger.exception(e)
        return "Could not search."


@app.route('/nearest/<int:zip_code>/<string:movie_name>')
def nearest_movie(zip_code, movie_name):
    query = "select theatre_name, street, city, time_start from Movie, Theatre " \
            "where movie.id = Theatre.movie_id and zip_code = %s  " \
            "and movie_name = %s"
    args = (zip_code, movie_name)

    try:
        conn = MySQL.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, args)

        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/reservation', methods=['POST'])
def create_reservation():
    try:
        json = request.json
        customer_id = json['customer_id']
        movie_id = json['movie_id']
        theatre_id = json['theatre_id']
        ticket_qty = json['ticket_qty']
        seats = json['seats']

        if customer_id and movie_id and theatre_id and ticket_qty and seats and request.method == 'POST':
            query = "insert into reservation (id, customer_id, movie_id, theatre_id, ticket_qty, seat, " \
                    "reservation_date) values(null,%s,%s,%s,%s,%s,current_timestamp())"
            args = (customer_id, movie_id, theatre_id, ticket_qty, seats)

            conn = MySQL.connect()
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            response = jsonify('Reservation added.')
            response.status_code = 200
            return response
        else:
            return "Either data is missing or the method is not POST."

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['POST'])
def update_reservation():
    try:
        json = request.json
        id = json['id']
        customer_id = json['customer_id']
        movie_id = json['movie_id']
        theatre_id = json['theatre_id']
        ticket_qty = json['ticket_qty']
        seats = json['seats']

        if id and customer_id and movie_id and theatre_id and ticket_qty and seats and request.method == 'POST':
            query = "update reservation " \
                    "set customer_id = %s, movie_id = %s, theatre_id = %s, ticket_qty = %s, seat = %s, " \
                    "reservation_date = current_timestamp() where id = %s"
            args = (customer_id, movie_id, theatre_id, ticket_qty, seats, id)

            conn = MySQL.connect()
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            response = jsonify('Reservation updated.')
            response.status_code = 200
            return response
        else:
            return "Either data is missing or the method is not POST."
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>', methods=['POST'])
def cancel_reservation(id):
    try:
        if id and request.method == 'POST':
            query = "update reservation " \
                    "set removed = %s " \
                    "where id = %s"
            args = (1, id)

            conn = MySQL.connect()
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            response = jsonify('Reservation cancelled.')
            response.status_code = 200
            return response
        else:
            return "Reservation could not be cancelled."
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/payment/<int:id>')
def payment(id):
    query = "select theatre_name, theatre_id, seat, movie_name, reservation_date, movie_price " \
            "from customer, reservation, movie, theatre " \
            "where customer.id = reservation.customer_id and theatre.id = reservation.theatre_id and movie.id = " \
            "reservation.movie_id and reservation.id = %s "
    args = (id,)

    try:
        conn = MySQL.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, args)
        record = cursor.fetchone()
        response = jsonify(record)
        response.status_code = 200
        return response
    except Exception as e:
        app.logger.exception(e)
        return "Could not retrieve payment information."
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run()
