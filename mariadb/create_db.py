
"""
최신 MariaDB 테이블 생성 스크립트
- 실행: python create_tables_latest.py
- 목적: 프로젝트에서 사용하는 최신 스키마를 한 번에 생성
- 포함 테이블:
  users
  mock_accounts
  stocks
  stock_details
  stock_price_history
  etfs
  etf_price_history
  portfolio_holdings
  trades
  news
  stock_news
  stock_chats

주의:
- database.py 안에 get_conn() 함수가 있어야 합니다.
- 기존 테이블을 삭제하고 다시 생성합니다. (데이터 초기화됨)
- portfolio_holdings는 strategy 컬럼과
  UNIQUE KEY (user_id, stock_id, strategy)를 반영했습니다.
- portfolio_holdings.total_invested 컬럼은 현재 프로젝트 흐름에 맞춰 포함했습니다.
"""

from database import get_conn


DROP_TABLES_SQL = [
    "DROP TABLE IF EXISTS stock_chats",
    "DROP TABLE IF EXISTS stock_news",
    "DROP TABLE IF EXISTS news",
    "DROP TABLE IF EXISTS trades",
    "DROP TABLE IF EXISTS portfolio_holdings",
    "DROP TABLE IF EXISTS etf_price_history",
    "DROP TABLE IF EXISTS etfs",
    "DROP TABLE IF EXISTS stock_price_history",
    "DROP TABLE IF EXISTS stock_details",
    "DROP TABLE IF EXISTS stocks",
    "DROP TABLE IF EXISTS mock_accounts",
    "DROP TABLE IF EXISTS users",
]


CREATE_TABLES_SQL = [
    """
    CREATE TABLE users (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        email VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        nickname VARCHAR(100) NOT NULL,
        is_verified TINYINT(1) NOT NULL DEFAULT 0,
        avatar VARCHAR(50) DEFAULT '🧑‍💼',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_users_email (email),
        UNIQUE KEY uq_users_nickname (nickname)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE mock_accounts (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        initial_balance DECIMAL(15,2) NOT NULL DEFAULT 10000000.00,
        current_balance DECIMAL(15,2) NOT NULL DEFAULT 10000000.00,
        total_profit_loss DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_mock_accounts_user_id (user_id),
        CONSTRAINT fk_mock_accounts_user
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE stocks (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        ticker VARCHAR(20) NOT NULL,
        name_kr VARCHAR(100) NOT NULL,
        market VARCHAR(20) DEFAULT NULL,
        sector VARCHAR(50) DEFAULT NULL,
        is_defense TINYINT(1) NOT NULL DEFAULT 1,
        description TEXT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_stocks_ticker (ticker)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE stock_details (
        stock_id INT UNSIGNED NOT NULL,
        current_price INT NOT NULL,
        change_amount INT NOT NULL DEFAULT 0,
        change_rate DECIMAL(7,2) NOT NULL DEFAULT 0.00,
        volume BIGINT NOT NULL DEFAULT 0,
        trading_value BIGINT NOT NULL DEFAULT 0,
        high_price INT NOT NULL DEFAULT 0,
        low_price INT NOT NULL DEFAULT 0,
        open_price INT NOT NULL DEFAULT 0,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (stock_id),
        CONSTRAINT fk_stock_details_stock
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE stock_price_history (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        stock_id INT UNSIGNED NOT NULL,
        price_date DATE NOT NULL,
        open_price INT NOT NULL,
        high_price INT NOT NULL,
        low_price INT NOT NULL,
        close_price INT NOT NULL,
        volume BIGINT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_stock_price_history_stock_date (stock_id, price_date),
        KEY idx_stock_price_history_stock_id (stock_id),
        KEY idx_stock_price_history_price_date (price_date),
        CONSTRAINT fk_stock_price_history_stock
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE etfs (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        ticker VARCHAR(20) NOT NULL,
        name_kr VARCHAR(100) NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_etfs_ticker (ticker)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE etf_price_history (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        etf_id INT UNSIGNED NOT NULL,
        price_date DATE NOT NULL,
        open_price INT NOT NULL,
        high_price INT NOT NULL,
        low_price INT NOT NULL,
        close_price INT NOT NULL,
        volume BIGINT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_etf_price_history_etf_date (etf_id, price_date),
        KEY idx_etf_price_history_etf_id (etf_id),
        KEY idx_etf_price_history_price_date (price_date),
        CONSTRAINT fk_etf_price_history_etf
            FOREIGN KEY (etf_id) REFERENCES etfs(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE portfolio_holdings (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        account_id INT UNSIGNED NOT NULL,
        stock_id INT UNSIGNED NOT NULL,
        quantity INT NOT NULL DEFAULT 0,
        avg_buy_price DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        total_invested DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        strategy VARCHAR(50) NOT NULL DEFAULT '수동 운용',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_user_stock_strategy (user_id, stock_id, strategy),
        KEY idx_portfolio_holdings_account_id (account_id),
        KEY idx_portfolio_holdings_stock_id (stock_id),
        CONSTRAINT fk_portfolio_holdings_user
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_portfolio_holdings_account
            FOREIGN KEY (account_id) REFERENCES mock_accounts(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_portfolio_holdings_stock
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE trades (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        account_id INT UNSIGNED NOT NULL,
        stock_id INT UNSIGNED NOT NULL,
        trade_type VARCHAR(10) NOT NULL,
        price INT NOT NULL,
        quantity INT NOT NULL,
        total_amount DECIMAL(15,2) NOT NULL,
        strategy VARCHAR(50) NOT NULL DEFAULT '수동 운용',
        traded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_trades_user_id (user_id),
        KEY idx_trades_account_id (account_id),
        KEY idx_trades_stock_id (stock_id),
        KEY idx_trades_traded_at (traded_at),
        CONSTRAINT chk_trades_type CHECK (trade_type IN ('BUY', 'SELL')),
        CONSTRAINT fk_trades_user
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_trades_account
            FOREIGN KEY (account_id) REFERENCES mock_accounts(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_trades_stock
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE news (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        title VARCHAR(255) NOT NULL,
        summary TEXT DEFAULT NULL,
        content LONGTEXT DEFAULT NULL,
        source VARCHAR(100) DEFAULT NULL,
        source_url VARCHAR(500) NOT NULL,
        thumbnail_url VARCHAR(500) DEFAULT NULL,
        published_at DATETIME NOT NULL,
        view_count INT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_news_source_url (source_url),
        KEY idx_news_published_at (published_at),
        KEY idx_news_view_count (view_count)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE stock_news (
        stock_id INT UNSIGNED NOT NULL,
        score INT NOT NULL DEFAULT 0,
        ai_summary TEXT DEFAULT NULL,
        news_data LONGTEXT DEFAULT NULL,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (stock_id),
        CONSTRAINT chk_stock_news_score CHECK (score BETWEEN 0 AND 100),
        CONSTRAINT fk_stock_news_stock
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE stock_chats (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        stock_id INT UNSIGNED NOT NULL,
        message TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_stock_chats_user_id (user_id),
        KEY idx_stock_chats_stock_id (stock_id),
        KEY idx_stock_chats_created_at (created_at),
        CONSTRAINT fk_stock_chats_user
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_stock_chats_stock
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
]


def main():
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute("SELECT DATABASE() AS db")
            db_name = cursor.fetchone()["db"]
            print(f"[INFO] 현재 DB: {db_name}")

            cursor.execute("SET NAMES utf8mb4")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            print("[INFO] 기존 테이블 삭제 시작")
            for sql in DROP_TABLES_SQL:
                table_name = sql.replace("DROP TABLE IF EXISTS", "").strip()
                cursor.execute(sql)
                print(f"  - dropped: {table_name}")

            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            print("[INFO] 테이블 생성 시작")
            create_order = [
                "users",
                "mock_accounts",
                "stocks",
                "stock_details",
                "stock_price_history",
                "etfs",
                "etf_price_history",
                "portfolio_holdings",
                "trades",
                "news",
                "stock_news",
                "stock_chats",
            ]

            for table_name, sql in zip(create_order, CREATE_TABLES_SQL):
                cursor.execute(sql)
                print(f"  + created: {table_name}")

        conn.commit()
        print("\n✅ 최신 테이블 생성 완료")
        print("   - portfolio_holdings.strategy 반영")
        print("   - UNIQUE (user_id, stock_id, strategy) 반영")
        print("   - stocks.market / sector / description 반영")
        print("   - users created_at / updated_at 포함")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n[ERROR] 테이블 생성 실패: {e}")
        raise
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
