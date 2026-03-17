# github : https://github.com/RTAI1TEAM/defense-stock-dashboard
# DB 생성 : 1. .env 필수 변수 : DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
#           1-1. mariadb에서 데이터베이스 생성하고 생성한 데이터베이스 이름을 DB_NAME 변수에 저장합니다.
#           2. 루트에서 python -m mariadb.create_db
#           3. 기본 데이터 추가 python -m mariadb.add_datas
#           4. python scripts/daily_update.py 
#               env 필수 변수 GEMINI_API_KEY
#           4-1. gemini api 초과 방지를 위해서 api키 여러개를 생성하여 돌리는 코드 : daily_update2.py
#                필수 변수로 GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3, GEMINI_API_KEY_4, GEMINI_API_KEY_5가 필요합니다.
#                키 개수 부족 시 services/ai_analysis2.py에서 26라인부터 있는 변수만큼 수정하셔서 사용하시면 됩니다.

# app.py — Flask 애플리케이션 메인 실행 파일

# 기능:
# 1. 애플리케이션 초기화 및 블루프린트(Route) 등록
# 2. 템플릿 필터 및 컨텍스트 프로세서 설정
from flask import Flask

from routes.log_card import dashboard_bp
from routes.app_login import auth_bp
from routes.rank import rank_bp
from routes.news import news_bp
from routes.stocks import stocks_bp
from routes.portfolio import portfolio_bp
from routes.stock_detail import stock_detail_bp
from routes.profile import profile_bp
from routes.stock_chat import stock_chat_bp
from routes.home import home_bp
from services.stock_service import get_stock_list
from config import SECRET_KEY

# 1. Flask 앱 초기화 및 설정
app = Flask(__name__)
app.secret_key = SECRET_KEY  # 세션 암호화 등을 위한 비밀키

# 2. 블루프린트 등록 (기능별 라우트 분리)
app.register_blueprint(home_bp)         # 메인화면
app.register_blueprint(auth_bp)         # 로그인/회원가입
app.register_blueprint(rank_bp)         # 랭킹 시스템
app.register_blueprint(news_bp)         # 뉴스 모아보기
app.register_blueprint(stocks_bp)       # 주식 목록
app.register_blueprint(portfolio_bp)    # 내 포트폴리오
app.register_blueprint(stock_detail_bp) # 종목 상세 및 주문
app.register_blueprint(profile_bp)      # 프로필 관리
app.register_blueprint(stock_chat_bp)   # 종목 토론방
app.register_blueprint(dashboard_bp)    # 대시보드 로그카드

@app.template_filter('comma')
def comma_filter(value):
    # 숫자에 천 단위 콤마를 찍어주는 템플릿 필터 (예: 1,000)
    return format(int(value), ',')

@app.context_processor
def inject_stock_list():
    # 모든 템플릿에서 'stock_list' 변수를 사용할 수 있도록 주입합니다 (네비게이션 바 검색용 등).
    try:
        return dict(stock_list=get_stock_list())
    except Exception:
        return dict(stock_list=[])

if __name__ == "__main__":
    # 개발 서버 실행 (debug=True 설정 시 코드 수정 시 자동 재시작)
    app.run(debug=True)