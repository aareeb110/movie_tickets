from time import strftime
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
from fpdf import FPDF


def search_movie(id):
    query = "select movie_name from Movie " \
            "where id = %s"
    args = (id,)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        cursor.execute(query, args)

        row = cursor.fetchone()
        movie_name = row[0]
        return movie_name

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def nearest_movie(zip_code, movie_name):
    query = "select theatre_name, street, city, time_start from Movie, Theatre " \
            "where movie.id = Theatre.movie_id and zip_code = %s  " \
            "and movie_name = %s"
    args = (zip_code, movie_name)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        row = cursor.fetchall()
        print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def create_reservation(customer_id, movie_id, theatre_id, ticket_qty, seat):
    query = "insert into reservation (id, customer_id, movie_id, theatre_id, ticket_qty, seat, reservation_date) " \
            "values(null,%s,%s,%s,%s,%s,current_timestamp())"

    args = (customer_id, movie_id, theatre_id, ticket_qty, seat)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def update_reservation(id, customer_id, movie_id, theatre_id, ticket_qty, seat):
    query = "update reservation " \
            "set customer_id = %s, movie_id = %s, theatre_id = %s, ticket_qty = %s, seat = %s, reservation_date = " \
            "current_timestamp() where id = %s"

    args = (customer_id, movie_id, theatre_id, ticket_qty, seat)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def payment(customer_id, movie_id, theatre_id, ticket_qty, seat):

    create_reservation(customer_id, movie_id, theatre_id, ticket_qty, seat)

    query = "select theatre_name, theatre_id, seat, movie_name, reservation_date, movie_price " \
            "from customer, reservation, movie, theatre " \
            "where customer.id = reservation.customer_id and theatre.id = reservation.theatre_id and movie.id = " \
            "reservation.movie_id and customer.id = %s "
    args = (customer_id,)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        cursor.execute(query, args)

        row = cursor.fetchone()
        return row

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


# things needed on the receipt, in order:
# name of theatre
# seat
# name of movie
# date and time
# price
class PDF(FPDF):
    def print_ticket(self, movie_id):
        self.set_xy(10.0, 0.0)
        self.set_font('Arial', '', 11)

        customer_id = input("Enter your customer id: ")
        theatre_id = input("Enter the theatre id (1-3 only): ")
        ticket_qty = input("Enter the number of tickets you wish to buy: ")
        seat_qty = input("Enter the seats you wish to reserve (separate by comma): ")

        ticket = payment(customer_id, movie_id, theatre_id, ticket_qty, seat_qty)
        seats_list = ticket[2].split(',')
        pdf.write(11, 'Ticket\n\n')
        for x in seats_list:
            pdf.write(5, 'Name: ' + ticket[0] + '\n')
            pdf.write(5, 'Seat: ' + x + '\n')
            pdf.write(5, 'Movie: ' + ticket[3] + '\n')
            pdf.write(5, ticket[-2].strftime("%b %d, %Y, %I:%M %p") + '\n')
            pdf.write(5, 'Price: $' + f'{ticket[-1]:.2f}' + '\n')
            pdf.write(5, '\n\n----------------\n\n\n\n')
        pdf.output('movie_ticket.pdf', 'F')


if __name__ == '__main__':
    # search movie test
    movie_id = input("Enter the id of the movie you wish to search (1-4 only): ")
    print(search_movie(movie_id))

    # nearest movie test
    zip_code = input("Enter your zip code: ")
    movie_name = search_movie(movie_id)
    nearest_movie(zip_code, movie_name)

    # payment test
    pdf = PDF()
    pdf.set_author('Areeb Amjad')
    pdf.add_page()
    pdf.print_ticket(movie_id)

