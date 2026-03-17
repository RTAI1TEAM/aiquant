from mariadb.add_stocks import add_stocks_data, add_eft_data 
from testdum import create_test_dummy

if __name__=='__main__':
    add_stocks_data()
    add_eft_data()
    # 유저 더미 데이터 필요 시 실행
    # create_test_dummy()