def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_regex(times):
    res = ""
    regex = "[0-9]"
    for i in range(0, times):
        res += regex
    return res


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        blobData = file.read()
    return blobData


def QueryIns1(c, conn, data_tuple):
    employee_query = """ INSERT INTO employee
										  ('emp_name', 'emp_id', 'rank', 'salary', 'phone_number', 'sex', 'birthdate', 'recruit_date', 'address', 'photo', 'status') 
										   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    c.execute(employee_query, data_tuple)
    conn.commit()


def QueryIns2(c, conn, data_tuple):
    country_query = """ INSERT INTO country
										  ('country_code', 'country_name', 'continent_attr', 'head_of_state', 'foreign_minister',
										   'liaison', 'country_population', 'country_area', 'contact_number', 'has_diplomatic_relation', 'alive') 
											VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    c.execute(country_query, data_tuple)

    # save the changes
    conn.commit()


def QueryIns3(c, conn, data_tuple):
    sa_query = """ INSERT INTO stationed_agent ('emp_id', 'country_code', 'emp_name', 'arrival_date', 'ambassador_name', 'status') 
														 VALUES (?, ?, ?, ?, ?, ?)"""
    c.execute(sa_query, data_tuple)

    # save the changes
    conn.commit()


def QueryIns4(c, conn, data_tuple):
    c.execute("SELECT dep_id FROM dependents")
    checkq = [item[0] for item in c.fetchall()]

    found = 0
    for d in range(0, len(checkq)):
        if data_tuple[1] == checkq[d]:
            found = 1

    if found == 0:
        tmp0 = "select emp_name from employee where emp_id = '" + data_tuple[0] + "'"
        c.execute(tmp0)
        d0 = str(c.fetchone()[0])  # dependent person name
        # print(type(d0), " + ", d0)

        tmp1 = (
            "select emp_id from dependents where (dep_name = '"
            + d0
            + "' and dep_relation = '夫妻')"
        )
        c.execute(tmp1)
        if c.fetchone() is not None:
            c.execute(tmp1)
            d1 = str(c.fetchone()[0])  # emp_id
            # print(type(d1), " + ", d1)
        else:
            d1 = None

        if d1 is not None:
            d2 = 0
            d3 = 0

            tmp2 = "select dependency from dependents where dep_name = '" + d0 + "'"
            c.execute(tmp2)
            if c.fetchone() is not None:
                c.execute(tmp2)
                d2 = str(c.fetchone()[0])  # person

            tmp3 = "select dependency from dependents where dep_id = '" + d1 + "'"
            c.execute(tmp3)
            if c.fetchone() is not None:
                c.execute(tmp3)
                d3 = str(c.fetchone()[0])  # person for update

            # person has dependency, wife/husband still has dependency
            if d2 == "1" and d3 == "1":
                dep_update = (
                    "Update dependents set dependency = 0 where dep_id = '" + d1 + "'"
                )
                # wife/husband dependency(1 -> 0)
                c.execute(dep_update)

        if d1 is None or d2 == "1":  # None: no data
            de_query = """ INSERT INTO dependents ('emp_id', 'dep_id', 'dep_name', 'dep_sex', 'dep_relation', 'birthdate', 'dependency', 'status') 
														VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            c.execute(de_query, data_tuple)
            conn.commit()
        else:
            chosen_q = "select emp_name from employee where emp_id = '" + d1 + "'"
            c.execute(chosen_q)
            chosen_name = str(c.fetchone()[0])
            print("欲新增的眷屬", data_tuple[2], "依附對象應該為", ": " + chosen_name)


def del_q1(c, conn, del_id):
    del_query1 = "Update employee set status = '刪除' where emp_id = '" + del_id + "'"
    c.execute(del_query1)


def del_q2(c, conn, del_code):
    del_query2 = (
        "Update country set alive = '亡國' where country_code = '" + del_code + "'"
    )
    c.execute(del_query2)


def del_q3(c, conn, del_id, del_code, del_msg):
    act = 1
    if del_msg == "離職":
        del_query3 = (
            "Update stationed_agent set status = '離職' where (emp_id = '"
            + del_id
            + "' and country_code = '"
            + del_code
            + "')"
        )
    elif del_msg == "調離原職":
        del_query3 = (
            "Update stationed_agent set status = '調離原職' where (emp_id = '"
            + del_id
            + "' and country_code = '"
            + del_code
            + "')"
        )
    else:
        act = 0
    if act == 1:
        c.execute(del_query3)


def del_q4(c, conn, del_id, del_msg):
    act = 1
    if del_msg == "離婚":
        del_query4 = (
            "Update dependents set status = '離婚' where (dep_id = '" + del_id + "'"
        )
    elif del_msg == "被人收養":
        del_query4 = (
            "Update dependents set status = '被人收養' where (dep_id = '" + del_id + "'"
        )
    else:
        act = 0
    if act == 1:
        c.execute(del_query4)


def UpdateQuery1(c, conn, op, info):
    act = 1
    if op == 1:
        UpdateQ1 = "Update employee set address = '" + info + "'"
    elif op == 2:
        UpdateQ1 = "Update employee set phone_number = '" + info + "'"
    else:
        act = 0
    if act == 1:
        c.execute(UpdateQ1)


def UpdateQuery4(c, conn, info):
    UpdateQ4 = "Update dependents set status = '離婚'"
    c.execute(UpdateQ4)


def QueryData1(c, conn, info):
    QueryDataQ1 = "select * from employee where emp_id = '" + info + "'"
    c.execute(QueryDataQ1)
    print(c.fetchone())


def QueryData2(c, conn, info):
    QueryDataQ2 = "select * from country where country_code = '" + info + "'"
    c.execute(QueryDataQ2)
    print(c.fetchone())


def QueryData3(c, conn):
    QueryDataQ3 = "select * from stationed_agent"
    c.execute(QueryDataQ3)
    print(c.fetchall())


def QueryData4(c, conn, op, info):
    if op == 1:
        QueryDataQ4 = "select * from dependents where emp_id = '" + info + "'"
        c.execute(QueryDataQ4)
    elif op == 2:
        QueryDataQ4 = "select * from dependents where dep_id = '" + info + "'"
        c.execute(QueryDataQ4)
    print(c.fetchone())


def EmployeeData(c, conn, option, info, rank):
    if option == 1:
        msgq1 = "select count(distinct emp_id) from employee where status = '正常'"
        c.execute(msgq1)
        print("員工總人數 = " + str(c.fetchone()[0]))

    elif option == 2:
        tmp = "select birthdate from employee"
        c.execute(tmp)
        birthdaylist = [item[0] for item in c.fetchall()]

        age_sum = 0
        for data in birthdaylist:
            msgq1 = (
                "SELECT strftime('%s','now') - strftime('%s', '" + data + " 00:00:00')"
            )
            c.execute(msgq1)
            x = c.fetchone()[0]
            diff = math.floor(float(str(x)) / (60 * 60 * 24 * 365))
            age_sum += diff
        print("員工平均年齡 = ", age_sum / len(birthdaylist))

    elif option == 3:
        # print("某職等人數輸入1, 某職等以下人數輸入2, 某職等以上人數輸入3")
        # a, rankmsg = map(int, input().split())

        if info == 1:
            rank_qmsg = "select count(*) from employee where rank = '" + str(rank) + "'"
            c.execute(rank_qmsg)
            print(rank, "職等人數 = ", int(c.fetchone()[0]))

        elif info == 2:
            EmpNumber = 0

            for i in range(0, rank + 1):
                rank_qmsg = (
                    "select count(*) from employee where rank  = '" + str(i) + "'"
                )
                c.execute(rank_qmsg)
                EmpNumber += int(c.fetchone()[0])
            print(rank, "職等以下人數 = ", EmpNumber)

        elif info == 3:
            EmpNumber = 0
            max_msg = "select max(cast(rank as integer)) from employee"
            c.execute(max_msg)
            maxrank = int(c.fetchone()[0])

            for i in range(rank, maxrank + 1):
                rank_qmsg = (
                    "select count(*) from employee where rank = '" + str(i) + "'"
                )
                c.execute(rank_qmsg)
                EmpNumber += int(str(c.fetchone()[0]))
            print(rank, "職等以上人數 = ", EmpNumber)
    elif option == 4:
        # b = int(input("年薪:1, 月薪:2, 週薪:3"))

        if info == 1:
            sal_qmsg = "select sum(salary) from employee"
            c.execute(sal_qmsg)
            salary_year = int(c.fetchone()[0]) * 12
            print("總年薪 = ", salary_year)
        elif info == 2:
            sal_qmsg = "select sum(salary) from employee"
            c.execute(sal_qmsg)
            salary_month = int(c.fetchone()[0])
            print("總月薪 = ", salary_month)
        elif info == 3:
            sal_qmsg = "select sum(salary) from employee"
            c.execute(sal_qmsg)
            salary_month = round(float(str(c.fetchone()[0])) / 4.34812141)
            print("總週薪 = ", salary_month)


# --------------------------------------------------------------------------------------------#


def CountryData(c, conn, option, info):
    if option == 1:
        HasDipRelationQuery = "select count(*) from country where (has_diplomatic_relation = '是' and alive = '正常')"
        NoDipRelationQuery = "select count(*) from country where (has_diplomatic_relation = '否' and alive = '正常')"

        c.execute(HasDipRelationQuery)
        print("有邦交國數目 = ", c.fetchone()[0])

        c.execute(NoDipRelationQuery)
        print("沒邦交數目 = ", c.fetchone()[0])

    elif option == 2:
        if info is None:
            print("Invalid Continent_attr")
        else:
            HasDipRelateNumberQ = (
                "select count(distinct country_code) from country where (has_diplomatic_relation = '是' and alive = '正常' and continent_attr = '"
                + info
                + "')"
            )
            NoDipRelateNumberQ = (
                "select count(distinct country_code) from country where (has_diplomatic_relation = '否' and alive = '正常' and continent_attr = '"
                + info
                + "')"
            )

            c.execute(HasDipRelateNumberQ)
            print("所有邦交國數目 = ", c.fetchone()[0])

            c.execute(NoDipRelateNumberQ)
            print("所有非邦交國數目 = ", c.fetchone()[0])

    elif option == 3:
        if info is None:
            print("Invalid country_code")
        else:
            HasDipRelatePopulationQ = (
                "select country_population from country where (has_diplomatic_relation = '是' and alive = '正常' and country_code = '"
                + info
                + "')"
            )
            c.execute(HasDipRelatePopulationQ)
            population = c.fetchone()

            CountryNameQuery = (
                "select country_name from country where country_code = '" + info + "'"
            )
            c.execute(CountryNameQuery)
            CountryName = str(c.fetchone()[0])
            if population is None:
                print(CountryName + "為非邦交國")
            else:
                c.execute(HasDipRelatePopulationQ)
                population = int(str(c.fetchone()[0]))
                print("邦交國" + CountryName + "人口數為 = ", population)
    elif option == 4:
        HasDipRelateSumQ = "select sum(country_population) from country where (has_diplomatic_relation = '是' and alive = '正常')"
        c.execute(HasDipRelateSumQ)
        population = c.fetchone()[0]

        if population is None:
            print("邦交國不存在")
        else:
            print("所有邦交國的總人數 = ", population)

    elif option == 5:
        if info is None:
            print("Invalid country_code")
        else:
            NoDipRelatePopulationQ = (
                "select country_population from country where (has_diplomatic_relation = '否' and alive = '正常' and country_code = '"
                + info
                + "')"
            )
            c.execute(NoDipRelatePopulationQ)
            population = c.fetchone()

            CountryNameQuery = (
                "select country_name from country where country_code = '" + info + "'"
            )
            c.execute(CountryNameQuery)
            CountryName = str(c.fetchone()[0])
            if population is None:
                print(CountryName + "是邦交國")
            else:
                c.execute(NoDipRelatePopulationQ)
                population = int(str(c.fetchone()[0]))
                print("非邦交國" + CountryName + "人口數為 = ", population)
    elif option == 6:
        NoDipRelateSumQ = "select sum(country_population) from country where (has_diplomatic_relation = '否' and alive = '正常')"
        c.execute(NoDipRelateSumQ)
        population = c.fetchone()[0]

        if population is None:
            print("非邦交國不存在")
        else:
            print("所有非邦交國的總人數 = ", population)


def SagentData(c, conn, option, CountryCode):
    Semp_qmsg1 = (
        "select count(distinct emp_id) from stationed_agent where (status = '派駐' and country_code = '"
        + CountryCode
        + "')"
    )
    Semp_qmsg2 = (
        "select country_area from country where country_code = '" + CountryCode + "'"
    )
    Semp_qmsg3 = (
        "select country_name from country where country_code = '" + CountryCode + "'"
    )

    if option == 1:
        c.execute(Semp_qmsg1)
        SagentNumber = c.fetchone()[0]

        c.execute(Semp_qmsg3)
        SACountryName = str(c.fetchone()[0])
        print("派駐" + SACountryName + "的員工人數 = ", SagentNumber)

    elif option == 2:
        c.execute(Semp_qmsg1)
        EmpNumber = c.fetchone()[0]

        c.execute(Semp_qmsg2)
        CountryArea = c.fetchone()[0]

        c.execute(Semp_qmsg3)
        SACountryName = str(c.fetchone()[0])
        print("每平方公里", SACountryName, "員工派駐人數 = ", round(EmpNumber / CountryArea))


def DependtsData(c, conn, option):

    if option == 1:
        AllBirthQuery = "select birthdate from dependents"
        MaleBirthQuery = (
            "select birthdate from dependents where (dep_sex = 'M' or dep_sex = '男')"
        )
        FemaleBirthQuery = (
            "select birthdate from dependents where (dep_sex = 'F' or dep_sex = '女')"
        )
        # ----------------------------------------------------------------------------------------------------#

        c.execute(AllBirthQuery)
        AllBirthList = [item[0] for item in c.fetchall()]
        AllAgeSum = 0
        for data in AllBirthList:
            AllAgeQuery = (
                "SELECT strftime('%s','now') - strftime('%s', '" + data + " 00:00:00')"
            )
            c.execute(AllAgeQuery)
            diff = math.floor(float(str(c.fetchone()[0])) / (60 * 60 * 24 * 365))
            AllAgeSum += diff
        print("全部眷屬平均年齡 = ", AllAgeSum / len(AllBirthList))
        # ----------------------------------------------------------------------------------------------------#

        c.execute(MaleBirthQuery)
        MaleBirthList = [item[0] for item in c.fetchall()]

        MaleAgeSum = 0
        for data in MaleBirthList:
            MaleAgeQuery = (
                "SELECT strftime('%s','now') - strftime('%s', '" + data + " 00:00:00')"
            )
            c.execute(MaleAgeQuery)
            diff = math.floor(float(str(c.fetchone()[0])) / (60 * 60 * 24 * 365))
            MaleAgeSum += diff
        print("男性眷屬平均年齡 = ", MaleAgeSum / len(MaleBirthList))
        # ----------------------------------------------------------------------------------------------------#

        c.execute(FemaleBirthQuery)
        FemaleBirthList = [item[0] for item in c.fetchall()]

        FemaleAgeSum = 0
        for data in FemaleBirthList:
            FemaleAgeQuery = (
                "SELECT strftime('%s','now') - strftime('%s', '" + data + " 00:00:00')"
            )
            c.execute(FemaleAgeQuery)
            diff = math.floor(float(str(c.fetchone()[0])) / (60 * 60 * 24 * 365))
            FemaleAgeSum += diff
        print("女性眷屬平均年齡 = ", FemaleAgeSum / len(FemaleBirthList))
    # ----------------------------------------------------------------------------------------------------#

    elif option == 2:
        MaleDepNumberQuery = (
            "select count(*) from dependents where (dep_sex = 'M' or dep_sex = '男')"
        )
        c.execute(MaleDepNumberQuery)
        MaleDepNumber = c.fetchone()[0]

        FemaleDepNumberQuery = (
            "select count(*) from dependents where (dep_sex = 'F' or dep_sex = '女')"
        )
        c.execute(FemaleDepNumberQuery)
        FemaleDepNumber = c.fetchone()[0]

        print("男性眷屬人數 = ", MaleDepNumber, "女性眷屬人數 = ", FemaleDepNumber)


# ----------------------------------------------------------------------------------------------------#


def CrossData(c, conn, option, info):

    if option == 1:
        EmpNumber30Query = (
            "select count(distinct emp_id) from stationed_agent where ( status = '派駐' and country_code in (select country_code from country where country_name = '"
            + info
            + "'))"
        )
        c.execute(EmpNumber30Query)
        EmpNumber30 = c.fetchone()[0]
        print(EmpNumber30, "名員工派駐於", info)

    elif option == 2:
        EmpNumberContinentQuery = (
            "select count(distinct emp_id) from stationed_agent where ( status = '派駐' and country_code in (select country_code from country where continent_attr = '"
            + info
            + "'))"
        )
        c.execute(EmpNumberContinentQuery)
        EmpNumberContinent = c.fetchone()[0]
        print(EmpNumberContinent, "名員工派駐於", info)

    else:
        AllEmpAgeQuery = "select birthdate from employee"
        c.execute(AllEmpAgeQuery)
        EmpBirthList = [item[0] for item in c.fetchall()]

        EmpIDList = []
        for data in EmpBirthList:
            AllBirthQuery = (
                "SELECT strftime('%s','now') - strftime('%s', '" + data + " 00:00:00')"
            )
            c.execute(AllBirthQuery)
            diff = math.floor(float(str(c.fetchone()[0])) / (60 * 60 * 24 * 365))
            if diff >= 30:
                EmpIDQuery = (
                    "select emp_id from employee where birthdate = '" + data + "'"
                )
                c.execute(EmpIDQuery)
                EmpIDList.append(str(c.fetchone()[0]))

        EmpIDLength = len(EmpIDList)
        DepIDList = []
        for data in EmpIDList:
            Emp30Query = "select dep_id from dependents where emp_id = '" + data + "'"
            c.execute(Emp30Query)
            x = [item[0] for item in c.fetchall()]
            if len(x) == 0:
                EmpIDLength -= 1
            for d in x:
                DepIDList.append(d)

        if option == 3:
            DepBirthdate = []
            for data in DepIDList:
                DepQuery = (
                    "select birthdate from dependents where dep_id = '" + data + "'"
                )
                c.execute(DepQuery)
                DepBirthdate.append(str(c.fetchone()[0]))

            AvgAge = 0
            for data in DepBirthdate:
                AgeQuery = (
                    "SELECT strftime('%s','now') - strftime('%s', '"
                    + data
                    + " 00:00:00')"
                )
                c.execute(AgeQuery)
                age = math.floor(float(str(c.fetchone()[0])) / (60 * 60 * 24 * 365))
                AvgAge += age
            print("30歲以上員工平均眷屬年齡 = ", AvgAge / len(DepBirthdate))
        elif option == 4:
            print("30歲以上員工之平均眷屬人數 = ", len(DepIDList) / EmpIDLength)


def main():
    database = r"example.db"
    conn = create_connection(database)
    c = conn.cursor()

    c.execute("drop table if exists employee")
    c.execute("drop table if exists country")
    c.execute("drop table if exists stationed_agent")
    c.execute("drop table if exists dependents")
    sql_create_e1_table = """ CREATE TABLE IF NOT EXISTS employee (
												emp_name varchar(14),
												emp_id varchar(10),
												rank varchar(10),
												salary numeric(8,0),
												phone_number varchar(14) check(phone_number glob '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
												sex varchar(1),
												birthdate date,
												recruit_date date,
												address varchar(30),                                        
												photo blob,
												status varchar(2) check(status in('正常', '刪除')),                                       
												primary key(emp_id)
											); """

    sql_create_c1_table = """CREATE TABLE IF NOT EXISTS country (
											country_code varchar(6) check(country_code glob '[A-Z][A-Z][0-9][0-9][0-9][0-9]'),
											country_name varchar(14),
											continent_attr varchar(6),
											head_of_state varchar(14),
											foreign_minister varchar(14),
											liaison varchar(14),
											country_population numeric(14,0),
											country_area numeric(14,0),
											contact_number varchar(14) check(contact_number glob '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
											has_diplomatic_relation int(1) check(has_diplomatic_relation in('是', '否')),
											alive varchar(2) check(alive in('正常', '亡國')),
											primary key(country_code)
										);"""

    sql_create_s1_table = """CREATE TABLE IF NOT EXISTS stationed_agent (
											emp_id varchar(10),
											country_code varchar(6),
											emp_name varchar(14),
											arrival_date date,
											ambassador_name varchar(14),
											status varchar(2) check(status in('派駐', '離職')),
											primary key(emp_id, country_code),
											foreign key(emp_id) references employee(emp_id),
											foreign key(country_code) references country(country_code)
										);"""

    sql_create_d1_table = """CREATE TABLE IF NOT EXISTS dependents (
											emp_id varchar(10),
											dep_id varchar(10),
											dep_name varchar(14),
											dep_sex varchar(1) check(dep_sex in('M', '男', 'F', '女')),
											dep_relation varchar(6),
											birthdate date,    
											dependency int(1),
											status varchar(4) check(status in('正常', '離婚', '被人收養')),                               
											primary key(emp_id, dep_id),
											foreign key(emp_id) references employee(emp_id)
										);"""

    # create a database connection
    # create tables
    if conn is not None:

        create_table(conn, sql_create_e1_table)

        create_table(conn, sql_create_c1_table)

        create_table(conn, sql_create_s1_table)

        create_table(conn, sql_create_d1_table)
    else:
        print("Error! cannot create the database connection.")
    print("Connected to SQLite")

    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("新增員工資料中")
    data_instuple1 = (
        "王小明",
        "A123456788",
        "8",
        80000,
        "88621111111111",
        "M",
        "1971-12-15",
        "1995-07-01",
        "Berry road 1",
        convertToBinaryData("C:\workspace\workspace\img1.jpg"),
        "正常",
    )
    data_instuple2 = (
        "陳小玲",
        "A123456789",
        "8",
        80000,
        "88621111111112",
        "F",
        "1975-08-01",
        "1995-08-08",
        "Berry road 1",
        convertToBinaryData("C:\workspace\workspace\img1.jpg"),
        "正常",
    )

    data_instuple3 = (
        "劉小宏",
        "A123456787",
        "10",
        100000,
        "88621111111113",
        "M",
        "1990-12-08",
        "1988-10-20",
        "Berry road 2",
        convertToBinaryData("C:\workspace\workspace\img1.jpg"),
        "正常",
    )

    data_instuple4 = (
        "林小妍",
        "B12345678",
        "11",
        110000,
        "88611000111222",
        "F",
        "1960-01-01",
        "1988-12-01",
        "Maple road 1",
        convertToBinaryData("C:\workspace\workspace\img1.jpg"),
        "正常",
    )

    data_instuple5 = (
        "李四",
        "B12345679",
        "11",
        110000,
        "88612000111222",
        "M",
        "1960-12-20",
        "1988-11-02",
        "Maple road 2",
        convertToBinaryData("C:\workspace\workspace\img1.jpg"),
        "正常",
    )

    QueryIns1(c, conn, data_instuple1)
    QueryIns1(c, conn, data_instuple2)
    QueryIns1(c, conn, data_instuple3)
    QueryIns1(c, conn, data_instuple4)
    QueryIns1(c, conn, data_instuple5)
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("新增國家資料中")
    data_tuplec1 = (
        "AA4321",
        "澳洲",
        "大洋洲",
        "John McGregor",
        "Mary English",
        "Jenny Wallace",
        20000000,
        7692024,
        "12345678912345",
        "是",
        "正常",
    )
    data_tuplec2 = (
        "BB4321",
        "英國",
        "歐洲",
        "Jake Hill",
        "Justin Mann",
        "Patrik English",
        70000000,
        243610,
        "12345678901234",
        "是",
        "正常",
    )
    data_tuplec3 = (
        "CC4321",
        "荷蘭",
        "歐洲",
        "Jerry Meyer",
        "Joseph Bergen",
        "Kai Jansen",
        17180000,
        41526,
        "12345678901235",
        "是",
        "正常",
    )
    data_tuplec4 = (
        "DD4321",
        "法國",
        "歐洲",
        "Pierre Monet",
        "Mark Mann",
        "Marco Pascal",
        65000000,
        643801,
        "12345678901236",
        "是",
        "正常",
    )
    data_tuplec5 = (
        "EE4321",
        "德國",
        "歐洲",
        "Johannes Littmann",
        "Jannik Berkmeyer",
        "Wilhelm Hartmann",
        81000000,
        357386,
        "12345678901237",
        "是",
        "正常",
    )

    QueryIns2(c, conn, data_tuplec1)
    QueryIns2(c, conn, data_tuplec2)
    QueryIns2(c, conn, data_tuplec3)
    QueryIns2(c, conn, data_tuplec4)
    QueryIns2(c, conn, data_tuplec5)
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("新增派駐員工資料中")
    data_tuple_sa1 = ("A123456788", "AA4321", "王小明", "1995-12-01", "王小明", "派駐")
    data_tuple_sa2 = ("A123456789", "BB4321", "陳小玲", "1995-12-01", "陳小玲", "派駐")
    data_tuple_sa3 = ("A123456787", "CC4321", "劉小宏", "1995-12-01", "劉小宏", "派駐")
    data_tuple_sa4 = ("B12345678", "DD4321", "林小妍", "1995-12-01", "林小妍", "派駐")
    data_tuple_sa5 = ("B12345679", "EE4321", "李四", "1995-12-01", "李四", "派駐")

    QueryIns3(c, conn, data_tuple_sa1)
    QueryIns3(c, conn, data_tuple_sa2)
    QueryIns3(c, conn, data_tuple_sa3)
    QueryIns3(c, conn, data_tuple_sa4)
    QueryIns3(c, conn, data_tuple_sa5)
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("新增眷屬資料中")
    data_ins1 = ("A123456789", "A123456788", "王小明", "M", "夫妻", "1971-12-15", 1, "正常")
    data_ins2 = ("A123456788", "A123456789", "陳小玲", "F", "夫妻", "1975-08-01", 1, "正常")

    data_ins3 = ("A123456788", "B123456780", "王大龍", "M", "兒子", "2000-12-01", 0, "正常")
    data_ins4 = ("A123456789", "B123456781", "王小珍", "F", "女兒", "2003-11-15", 0, "正常")
    data_ins5 = ("A123456788", "B123456782", "王小美", "F", "女兒", "2004-11-20", 0, "正常")

    QueryIns4(c, conn, data_ins1)
    QueryIns4(c, conn, data_ins2)

    QueryIns4(c, conn, data_ins3)
    QueryIns4(c, conn, data_ins4)
    QueryIns4(c, conn, data_ins5)
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("刪除員工資料")
    del_q1(c, conn, "A123456789")
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("刪除國家資料")
    del_q2(c, conn, "BB4321")
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("刪除派駐員工資料")
    del_q3(c, conn, "A123456788", "AA4321", "離職")
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    # EmployeeData(c, conn, option, info, rank)
    print("#------------------------------------#")
    print("查詢員工資料")
    EmployeeData(c, conn, 1, None, None)  # 人數
    EmployeeData(c, conn, 2, None, None)  # 平均年齡

    EmployeeData(c, conn, 3, 1, 8)  # 某職等人數
    EmployeeData(c, conn, 3, 2, 8)  # 某職等以下人數
    EmployeeData(c, conn, 3, 3, 10)  # 某職等以上人數

    EmployeeData(c, conn, 4, 1, None)  # 年薪
    EmployeeData(c, conn, 4, 2, None)  # 月薪
    EmployeeData(c, conn, 4, 3, None)  # 週薪
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("查詢國家資料")
    CountryData(c, conn, 1, None)  # 多少邦交國? 多少非邦交國
    CountryData(c, conn, 2, "大洋洲")  # 哪一洲有多少邦交國? 多少非邦交國?
    CountryData(c, conn, 3, "AA4321")  # 某邦交國人數
    CountryData(c, conn, 4, None)  # 所有邦交國人數
    CountryData(c, conn, 5, "BB4321")  # 某非邦交國人數
    CountryData(c, conn, 6, None)  # 所有非邦交國人數
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("查詢派駐員工資料")
    SagentData(c, conn, 1, "AA4321")  # 派駐某國員工的人數
    SagentData(c, conn, 2, "AA4321")  # 每單位(平方公里)派駐某國員工的人數
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#

    print("#------------------------------------#")
    print("查詢眷屬資料")
    DependtsData(c, conn, 1)  # 平均眷屬年齡, 男眷屬平均年齡, 女眷屬平均年齡
    DependtsData(c, conn, 2)  # 男眷屬人數, 女眷屬人數
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#
    print("#------------------------------------#")
    print("查詢跨資料表")
    CrossData(c, conn, 1, "澳洲")  # 某國30歲以上員工人數
    CrossData(c, conn, 2, "歐洲")  # 某洲派駐員工人數
    CrossData(c, conn, 3, "年齡")  # 30歲以上員工 平均眷屬年齡
    CrossData(c, conn, 4, "人數")  # 30歲以上員工 平均眷屬人數
    print("#------------------------------------#\n\n")
    # -------------------------------------------------------------------------------------------#

    print("#------------------------------------#")
    print("內部管理查詢資料表")
    QueryData1(c, conn, "A123456788")  # squeezed text(圖片關係)
    QueryData2(c, conn, "AA4321")  # 國家資料
    QueryData3(c, conn)  #

    QueryData4(c, conn, 1, "A123456788")
    QueryData4(c, conn, 2, "B123456780")
    print("#------------------------------------#\n\n")

    conn.close()
