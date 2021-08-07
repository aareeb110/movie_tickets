from mysql.connector import MySQLConnection, Error
from MySQLConnection.mysql_dbconfig import read_db_config
from fpdf import FPDF


def ticket_data(customer_id):
    """
    Returns the customer name, theatre number, movie name and price, ticket quantity, and seat(s) in a tuple given
    a customer_id.
    :param customer_id: the customer id
    :return: n-tuple of ticket information
    """
    query = "select customer_name, theatre_num, movie_name, movie_price, ticket_qty, seat " \
            "from customer, reservation " \
            "where customer.customer_id = reservation.customer_id and customer.customer_id = %s"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        cursor.execute(query, (customer_id,))

        row = cursor.fetchone()
        return row

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


class PDF(FPDF):
    def print_ticket(self):
        self.set_xy(10.0, 0.0)
        self.set_font('Arial', '', 11)
        ticket = ticket_data(11037)
        print(ticket)
        seats_list = ticket[-1].split(",")
        pdf.write(11, 'Ticket\n\n')
        for x in seats_list:
            pdf.write(5, 'Name: ' + ticket[0] + '\n')
            pdf.write(5, 'Theater: ' + str(ticket[1]) + '\n')
            pdf.write(5, 'Movie: ' + ticket[2] + '\n')
            pdf.write(5, 'Price: ' + str(ticket[3]) + '\n')
            pdf.write(5, 'Tickets: ' + str(ticket[4]) + '\n')
            pdf.write(5, 'Seat: ' + x + '\n')
            pdf.write(5, '\n\n\n\n----------------\n\n\n\n')
        pdf.output('movie_ticket.pdf', 'F')


pdf = PDF()
pdf.set_author('Areeb Amjad')
pdf.add_page()
pdf.print_ticket()


if __name__ == '__main__':
    ticket_data(11037)
