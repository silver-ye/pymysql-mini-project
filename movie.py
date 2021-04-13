import pymysql

# connection 을 열고, cursor 열고, 입력받은 query 를 실행한 뒤에, 얻어온 정보를 result 에 저장, 연결들을 모두 해제한 뒤, result 를 다시 반환.
def wrapper_sql(query):
    conn = pymysql.connect(
    host ='localhost',
    port = 3306,
    user = 'movie',
    passwd = '1234',
    db = 'movie')
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
    return result

def insert_movie_info():
    print('영화 정보를 입력할 수 있습니다.')
    info_category = input('1) 영화 2) 배우 3) 감독 4) 출연정보 \n')
    if info_category == '1':
        print('영화 정보를 입력해주세요')
        print('영화 이름, 감독 이름, 장르, 별점, 개봉일 순으로 입력해주세요')
        print('EX) 미나리, 정이삭, 드라마, 8.33, 2021-03-03')
        info_movie = input()
        info_movie = info_movie.split(',')
        info_movie = [x.strip() for x in info_movie]
        #설국열차, 봉준호, SF, 7.98, 2013-08-01
        if len(info_movie) == 5:
            info_movie[1] = convert_name_id(info_movie[1],3)
            query = '''
            insert movie values
            (null, '{}', {}, '{}', {}, '{}') '''.format(*info_movie)
            csr = wrapper_sql(query)
# 택시운전사, 장훈, 드라마, 9.28, 2017-08-02
        else:
            print('입력이 잘못되었습니다. 다시 입력해주세요.')

    if info_category == '2':
        info_actor = input('배우 이름을 입력해주세요\n')
        query = "insert actor values (null,'{}')".format(info_actor)
        csr = wrapper_sql(query)
        # error?

    if info_category == '3':
        info_director = input('감독 이름을 입력해주세요\n')
        query = '''
        insert director values
        (null, '{}')'''.format(info_director)
        csr = wrapper_sql(query)
    
    if info_category == '4':
        print('영화 이름, 배우 이름, 감독 이름을 입력해주세요')
        print('EX) 미나리, 윤여정, 정이삭')
        info_info = input()
        info_info = info_info.split(',')
        info_info = [x.strip() for x in info_info]
        info_info = [convert_name_id(info_info[i], i+1) for i in range(3)]
        query = "insert info values (null, {}, {}, {})".format(info_info[0], info_info[1], info_info[2])
        csr = wrapper_sql(query)
        #insert info values (info_info[0], info_info[1], info_info[2])
        #error trouble shooting pass
    return 0
# 모드 1을 입력 -> 영화이름을 받고 그걸 아이디로 반환.
# 모드 2를 입력 -> 배우이름을 받고 그걸 아이디로 반환.
# 모드 3을 입력 -> 감독이릉르 받고 그걸 아이디로 반환.
def convert_name_id(name, mode):
    result_id = 0
    if mode == 1:
        query = '''
        select movie_id 
        from movie 
        where movie_name = '{}' '''.format(name)
        result_id = wrapper_sql(query)

    elif mode ==2:
        query = '''
        select actor_id
        from actor
        where name ='{}' '''.format(name)
        result_id = wrapper_sql(query)

    else:
        query = '''
        select director_id
        from director
        where name ='{}' '''.format(name)
        result_id = wrapper_sql(query)
    
    try:
        result = (result_id[0])[0]
        return result
    except:
        print('그런 이름을 가진 사람이 데이터베이스에 없습니다.')
        return -1
        

sql_movie = 'SELECT * FROM movie'
sql_actor = 'SELECT * FROM actor'
sql_director = 'SELECT * FROM director'
sql_info = 'SELECT * FROM info'

def search_movie():
    print('어떤 카테고리로 조회하시길 원하시나요? 카테고리를 선택해주세요.')
    search_category = int(input('1) 영화 이름 키워드 검색 2) 배우 검색 3) 감독 검색 4) 장르 검색\n'))
    if search_category == 1:
        movie_keyword = input('영화 이름을 입력해주세요 : \n')
        query= "select * from movie where movie_name like '%{}%' ".format(movie_keyword)
        csr = wrapper_sql(query)
        for i in csr:
            print('영화 이름:',i[1], '감독 이름:', i[2], '장르:', i[3], '평점:', i[4], '개봉일:', i[5])

            
    elif search_category==2:
        movie_actor=input('배우 이름을 입력해주세요: \n')
        query_actor_id = "select actor_id from actor where name like '%{}%' ".format(movie_actor)
        actor_id = (wrapper_sql(query_actor_id)[0])[0]        
        query_movie = '''
        select *
        from (
            select i.actor_id, i.movie_id, m.movie_name, i.director_id, m.genre_name, m.rate, m.released_date
            from info i
            join movie m
	        using (movie_id)) movie_info
        where actor_id = {}'''.format(actor_id)
        movies = (wrapper_sql(query_movie))
        for mv in movies:
            print('영화 이름:', mv[2], '감독 이름:', mv[3], '장르:', mv[4], '별점:', mv[5], '개봉일:', mv[6])

    elif search_category==3:
        movie_director=input('감독 이름을 입력해주세요: \n')
        query_director_id = "select director_id from director where name like '%{}%' ".format(movie_director)
        director_id = (wrapper_sql(query_director_id)[0])[0]
        query_movie = '''
        select *
        from director d
        join movie m using(director_id)
        where d.director_id = {}'''.format(director_id)
        movies = (wrapper_sql(query_movie))
        for mv in movies:
            print('영화 이름:', mv[3], '장르:', mv[4], '별점:', mv[5], '개봉일:',mv[6])

    elif search_category==4:
        print('장르를 선택해서 입력해주세요: 드라마, SF, 로맨스, 코미디, 공포, 액션')
        movie_gerne=input('장르를 입력해주세요: \n')
        query="select * from movie where genre_name = '{}' ".format(movie_gerne)
        csr= wrapper_sql(query)
        for i in csr:
            print('영화 이름:', i[1], '장르:',i[3], '평점:',i[4], '개봉일:', i[5])

def columns_of_table(table_name):
    query = '''
    select column_name
    from information_schema.columns
    where table_schema = 'movie' and table_name = '{}'
    '''.format(table_name)
    csr = wrapper_sql(query)
    return csr


print(columns_of_table('movie'))

print("안녕하세요. 영화 정보 조회 프로그램입니다.")
while True:
    print('영화 정보를 조회하시려면 1을, 영화 정보를 입력하시려면 2를 입력해주세요.')
    user_mode = input('1) 조회 2) 입력\n')
    if user_mode == '1' :
        search_movie()

    elif user_mode == '2': 
        insert_movie_info()
    else :
        print('잘못된 입력입니다. 정확히 입력해주세요.')





        
