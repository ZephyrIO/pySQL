import psycopg2
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", required=True, help="the database name")
    parser.add_argument("-u", required=True, help="user name used to authenticate")
    parser.add_argument("-pd", required=False, help="[optional] password used to authenticate")
    parser.add_argument("-hs", required=False, help="[optional] database host address (defaults to UNIX socket if not provided)")
    parser.add_argument("-pt", required=False, help="[optional] connection port number (defaults to 5432 if not provided)")
    
    args = parser.parse_args()

    conn = connectOpen(args.db, args.u, args.pd, args.hs, args.pt)
    cur = conn.cursor()

    print("pySQL (0.1)")
    print("Type 'q' to exit the program")
    while True:
        print(args.db, "=>", end=" ")
        i = input()
        if i.lower() == "q":
            conn.close()
            sys.exit(0)
        else:
            cur.execute(i)

            j = input("Are you sure? (y/N): ")
            if j.lower() == "y":
                if i[:6].lower() == "select":
                    print(cur.fetchall())
                conn.commit()
            else:
                cur.fetchall()
                conn.rollback()

# This function takes all the possible inputs to psycopg2.connect() and then build the correct version of the function call based on what data is given by the user.
def connectOpen(database, username, password, host, port):
    if password == None:
        pdTracker = False
    else:
        pdTracker = True
    if host == None:
        hTracker = False
    else:
        hTracker = True
    if port == None:
        ptTracker = False
    else:
        ptTracker = True
    
    if pdTracker and hTracker and ptTracker:
        con = psycopg2.connect(database=database, user=username, password=password, host=host, port=port)
    elif pdTracker and hTracker and not(ptTracker):
        con = psycopg2.connect(database=database, user=username, password=password, host=host)
    elif pdTracker and not(hTracker) and ptTracker:
        con = psycopg2.connect(database=database, user=username, password=password, port=port)
    elif not(pdTracker) and hTracker and ptTracker:
        con = psycopg2.connect(database=database, user=username, host=host, port=port)
    elif pdTracker and not(hTracker) and not(ptTracker):
        con = psycopg2.connect(database=database, user=username, password=password)
    elif not(pdTracker) and hTracker and not(ptTracker):
        con = psycopg2.connect(database=database, user=username, host=host)
    elif not(pdTracker) and not(hTracker) and ptTracker:
        con = psycopg2.connect(database=database, user=username, port=port)
    elif not(pdTracker) and not(hTracker) and not(ptTracker):
        con = psycopg2.connect(database=database, user=username)
    
    return con

if __name__ == '__main__':
    main()