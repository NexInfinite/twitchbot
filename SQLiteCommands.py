import sqlite3
import shlex

conn = sqlite3.connect('newcommand.db')
c = conn.cursor()
command_output = ' '
response_output = ' '
split_response = ' '
split_response_done = ' '

c.execute("""CREATE TABLE IF NOT EXISTS newcommand(
            command text,
            response text
            )""")


def insert_cmd(command_given, response_given):
    with conn:
        c.execute("SELECT * FROM 'newcommand' WHERE command = ?", (command_given,))
        test_if_command_in_database = c.fetchone()

        if test_if_command_in_database is None:
            if command_given != '?userman' and command_given != '?sudokid' and command_given != 'help':
                c.execute("INSERT INTO `newcommand` VALUES (:command, :response)", {'command': command_given, 'response': ' '.join(response_given)})
                if response_given is None or command_given is None:
                    response_ = 1
                else:
                    response_ = True
            else:
                response_ = 2
        else:
            response_ = False

        return response_

def get_command_response(command):
    with conn:
        c.execute("SELECT * FROM 'newcommand' WHERE command = ?", (command,))
        response = c.fetchone()

        if response:
            print('YAY FOUND')
            return response[1]

        return None

def delete_command_from_database(command):
    with conn:
        c.execute("SELECT * FROM 'newcommand' WHERE command = ?", (command,))
        test_if_command_in_database = c.fetchone()
        print(test_if_command_in_database)

        if test_if_command_in_database is not None:
            c.execute("DELETE FROM 'newcommand' WHERE command = ?", (command,))
            response_ = True
        elif test_if_command_in_database is None:
            c.execute("SELECT * FROM 'newcommandgroup' WHERE command = ?", (command,))
            test_if_command_in_database_2 = c.fetchone()
            if test_if_command_in_database_2 is not None:
                c.execute("DELETE FROM 'newcommandgroup' WHERE command = ?", (command,))
                response_ = True
            else:
                response_ = False
        else:
            response_ = False

        return response_

def edit_command_in_database(command, response):
    with conn:
        c.execute("SELECT * FROM 'newcommand' WHERE command = ?", (command,))
        test_if_command_in_database = c.fetchone()
        print(test_if_command_in_database)

        if test_if_command_in_database is not None:
            c.execute("UPDATE 'newcommand' SET response = ? WHERE command = ?", (' '.join(response), command))
            response_ = True
        elif test_if_command_in_database is None:
            c.execute("SELECT * FROM 'newcommandgroup' WHERE command = ?", (command,))
            test_if_command_in_database_2 = c.fetchone()
            if test_if_command_in_database_2 is not None:
                c.execute("UPDATE 'newcommandgroup' SET response = ? WHERE command = ?", (' '.join(response), command))
                response_ = True
        else:
            response_ = False

        return response_


if __name__ == '__main__':

    conn.commit()
    conn.close()