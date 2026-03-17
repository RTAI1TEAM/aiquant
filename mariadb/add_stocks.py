from database import get_conn

def add_stocks_data():
    with get_conn() as conn:
        with conn.cursor() as cur:
            sql = """INSERT INTO stocks (ticker, name_kr, market, sector, is_defense, description) VALUES
            ('064350','현대로템','KOSPI','defense',1,'방산 및 철도 차량 제작 기업'),
            ('012450','한화에어로스페이스','KOSPI','defense',1,'항공엔진 및 방산 시스템 기업'),
            ('079550','LIG넥스원','KOSPI','defense',1,'유도무기 및 방위 시스템 개발'),
            ('272210','한화시스템','KOSPI','defense',1,'방산 전자 및 ICT 시스템 기업'),
            ('047810','한국항공우주','KOSPI','defense',1,'군용 항공기 및 항공우주 개발'),
            ('077970','STX엔진','KOSPI','defense',1,'선박 및 방산용 엔진 제조'),
            ('024740','한일단조','KOSDAQ','defense',1,'단조 부품 및 방산 부품 생산'),
            ('038060','루멘스','KOSDAQ','defense',1,'LED 및 전자 부품 제조'),
            ('007120','미래아이앤지','KOSDAQ','defense',1,'IT 및 시스템 통합 기업'),
            ('032820','우리기술','KOSDAQ','defense',1,'원전 및 방산 제어 시스템'),
            ('368770','파이버프로','KOSDAQ','defense',1,'광섬유 기반 센서 및 방산 기술'),
            ('230980','비유테크놀러지','KOSDAQ','defense',1,'IT 및 기술 서비스 기업'),
            ('009540','HD한국조선해양','KOSPI','defense',1,'조선 및 해양 방산 관련 기업'),
            ('003570','SNT다이내믹스','KOSPI','defense',1,'방산용 변속기 및 기계 부품'),
            ('005810','풍산홀딩스','KOSPI','defense',1,'풍산 그룹 지주사'),
            ('108380','대양전기공업','KOSDAQ','defense',1,'선박 및 방산 전기 시스템'),
            ('372910','한컴라이프케어','KOSDAQ','defense',1,'방독면 및 안전 장비 제조'),
            ('006050','국영지앤엠','KOSDAQ','defense',1,'특수 유리 및 방산 소재'),
            ('095190','이엠코리아','KOSDAQ','defense',1,'기계 및 방산 부품 제조'),
            ('042660','한화오션','KOSPI','defense',1,'잠수함 및 군함 건조'),
            ('010820','퍼스텍','KOSDAQ','defense',1,'방산 전자 및 무기 시스템'),
            ('015710','코콤','KOSDAQ','defense',1,'보안 및 통신 장비 제조'),
            ('013810','스페코','KOSDAQ','defense',1,'방산 및 중장비 제조'),
            ('040300','YTN','KOSDAQ','defense',1,'보도 전문 방송사'),
            ('003010','혜인','KOSPI','defense',1,'중장비 및 산업 장비 유통'),
            ('274090','켄코아에어로스페이스','KOSDAQ','defense',1,'항공기 부품 제조'),
            ('119500','포메탈','KOSDAQ','defense',1,'단조 및 기계 부품 제조'),
            ('035460','기산텔레콤','KOSDAQ','defense',1,'통신 장비 및 네트워크 장비'),
            ('361390','제노코','KOSDAQ','defense',1,'우주 및 방산 전자 시스템'),
            ('064960','SNT모티브','KOSPI','defense',1,'자동차 및 방산 부품'),
            ('096630','에스코넥','KOSDAQ','defense',1,'전자 부품 제조'),
            ('377330','이지트로닉스','KOSDAQ','defense',1,'전력 변환 및 전자 기술'),
            ('065950','웰크론','KOSDAQ','defense',1,'특수 섬유 및 방산 소재'),
            ('095270','웨이브일렉트로','KOSDAQ','defense',1,'RF 및 통신 장비'),
            ('042370','비츠로테크','KOSDAQ','defense',1,'전력 및 방산 기술 기업'),
            ('103140','풍산','KOSPI','defense',1,'방산 탄약 및 구리 소재'),
            ('010280','아이티센엔텍','KOSDAQ','defense',1,'IT 서비스 및 시스템 통합'),
            ('215090','솔디펜스','KOSDAQ','defense',1,'방산 장비 및 시스템'),
            ('000880','한화','KOSPI','defense',1,'방산 및 화학 사업 보유'),
            ('005870','휴니드','KOSPI','defense',1,'군용 통신 장비 제조'),
            ('077360','덕산하이메탈','KOSDAQ','defense',1,'전자 소재 및 부품'),
            ('065450','빅텍','KOSDAQ','defense',1,'군용 전자 및 방산 장비'),
            ('000270','기아','KOSPI','defense',1,'군용 차량 및 자동차 제조'),
            ('088800','에이스테크','KOSDAQ','defense',1,'통신 장비 제조'),
            ('003490','대한항공','KOSPI','defense',1,'항공 및 군용 항공기 정비'),
            ('214430','아이쓰리시스템','KOSDAQ','defense',1,'적외선 센서 및 방산 기술'),
            ('011210','현대위아','KOSPI','defense',1,'방산 포 및 기계 시스템'),
            ('068790','DMS','KOSDAQ','defense',1,'디스플레이 및 장비 제조');
            """
            cur.execute(sql)

def add_eft_data():
    with get_conn() as conn:
        with conn.cursor() as cur:
            sql="INSERT INTO etfs (ticker, name_kr) VALUES ('463250', 'TIGER K방산&우주')"
            cur.execute(sql)