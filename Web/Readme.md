# ToDoList用簡易サーバー

ToDoListアプリ用の簡易サーバー
1ファイルで可能な限り簡潔に作った。
DBはSQLiteなのでDBソフトをインストールしないでも動く。
エラー処理とかしてないので、パラメータ間違うと動きません。

## インストール

- python3をインストールする
- pip install -r requirements.txt   をする

## 実行

- python3 todolistsv.py
- http://127.0.0.1:8888/ がAPIのエンドポイントになる

## API仕様

### User

- /login?login_account=ユーザーアカウント
  - GET: ログイン
    - ユーザーアカウントは、abcと123が用意されてます。

### ToDoList

- /todolist/<int:user_id>
  - GET: ユーザーのToDoリストを取得
    - RETURN
    {
        "status": "ok",
        "user": {
            "id": 1,
            "login_account": "abc",
            "name": "エービーシー"
        }
    }

- /todolist/<int:user_id>/<int:todo_id>
  - GET: ユーザーのToDoアイテム1個の詳細を確認
    - RETURN
    {
        "status": "ok",
        "todo": [
            {
                "content": "テスト2",
                "created": "2022-01-19T23:17:50.329347",
                "id": 2,
                "modified": "2022-01-19T23:17:50.329347",
                "status": false
            },
            {
                "content": "追加アイテム1",
                "created": "2022-01-19T23:27:57.654268",
                "id": 3,
                "modified": "2022-01-19T23:27:57.654268",
                "status": false
            }
        ]
    }
  - POST：ユーザーのToDoアイテムを追加
    - 追加するToDoはJSONフォーマットで指定する。
    - {"content":"ToDoの内容"}
  - PUT : ユーザーのToDoアイテムを更新
    - 更新するToDoはJSONフォーマットで指定する。statusはtrueかfalseを指定
    - {"content":"ToDoの内容", "status":true/false}
  - DELETE : ユーザーのToDoアイテムを削除

### よくAPIの使い方がわからない人

postman使って ToDoListAPI.postman_collection.json をインポートする。