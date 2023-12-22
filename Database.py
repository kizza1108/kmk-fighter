import sqlite3 as sql


# class
class DB:
    # constructor
    def __init__(self, **kwargs):
        super(DB, self).__init__(**kwargs)
        # creating or connecting to DB
        self.conn = sql.connect('kmk-fighting-db.db')
        # creating cursor for DML operation queries
        self.cur = self.conn.cursor()
        print('database connected...')
        # calling function
        self.create_database_structure()

    def create_database_structure(self):
        # create table if not exist
        self.cur.execute("""Create table If not exists Users (U_id Integer primary key autoincrement, 
                            Username Text NOT NULL UNIQUE,
                            Password Text Not Null,
                            Email Text Not Null UNIQUE)""")

        # create table Leaderboard
        self.cur.execute("""Create table If not exists Leaderboard (b_id Integer primary key autoincrement,
                    Round_no Text Not Null,
                    play_time Text Not Null,
                    Player1_Name Text Not Null,
                    Player2_Name Text Not Null,
                    win Text Not Null)""")

    # fetch user by giving the username
    def get_user(self, username):
        # select query
        self.cur.execute("Select * from Users where username=?", (username,))
        # get result
        res = self.cur.fetchall()

        if res:
            # return result if there is any
            return res[0]
        else:
            # else return none
            return None

    # get Leader board info function
    def get_leader_board(self):
        msg = ''
        # select query
        self.cur.execute('Select * from Leaderboard')
        # get data from DB
        res = self.cur.fetchall()
        if res:
            for i in res:
                msg += 'Round ' + str(i[1]) + ' --> ' + i[3] + ' vs ' + i[4] + ' Winner(' + str(i[5]) + ')\n'
        else:
            msg = 'No data Found'
        # return result
        return msg

    # player stat
    def player_stat(self, p_name):
        sum_time = 0
        avg_time = 0
        tol_rounds = 0
        msg = 'No Data Found'
        self.cur.execute(
            "select sum(play_time/60), avg(play_time/60), count(round_no) from Leaderboard WHERE (player1_name = ? or player2_name= ?)",
            (p_name, p_name))
        res = self.cur.fetchall()
        self.cur.execute("select COUNT(win) from Leaderboard WHERE win=?", (p_name,))
        res1 = self.cur.fetchall()
        print(res)
        if res[0][0]:
            sum_time = round(res[0][0], 2)
            avg_time = round(res[0][1], 2)
            tol_rounds = res[0][2]
        msg = "Total Play time in min's " + str(sum_time) + '\n\nAvg. Play time per round ' + str(
            avg_time) + '\n\nTotal Round Wins ' + str(res1[0][0]) + '/' + str(tol_rounds)

        return msg

    # Leaderboard insert
    def insert_leaderboard(self, details):
        try:
            # insert query
            self.cur.execute("Insert into LeaderBoard Values (Null, ?, ?, ?, ?, ?)",
                             (details[0], details[1], details[2], details[3], details[4]))
            msg = 'Data Inserted successfully'
            # save DB
            self.conn.commit()
            return msg
        except Exception as e:
            return str(e)

    # update profile function
    def update_profile(self, data):
        try:
            # update query
            self.cur.execute("update Users set Password=? where username=?",
                             (data[0], data[1]))
            # save DB
            self.conn.commit()
            msg = 'Profile Updated successfully'
        except Exception as e:
            msg = str(e)
        return msg

    def insert_profile(self, data):
        try:
            # update query
            self.cur.execute("Insert into Users Values ( Null, ?, ?, ?)", (data[0], data[1], data[2]))
            # save DB
            self.conn.commit()
            msg = 'User Register successfully'
        except Exception as e:
            msg = str(e)
        return msg
