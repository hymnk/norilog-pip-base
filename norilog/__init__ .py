import json
from datetime import datetime

from flask import Flask, redirect, render_template, request, escape, Markup

application = Flask(__name__)

DATA_FILE = 'norilog.json'


def save_data(start, finish, memo, created_at):
    """記録データを保存します

    Args:
        start (str): 乗った駅
        finish (str): 降りた駅
        memo (str): 乗り降りのメモ
        created_at (datetime.datetime): 乗り降りの日付
        return: None
    """
    try:
        # json モジュールでデータベースを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        "start": start,
        "finish": finish,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database,
              open(DATA_FILE, mode="w", encoding="utf-8"),
              indent=4,
              ensure_ascii=False)


def load_data():
    """記録データを返します

    Returns:
        json: 記録データ
    """
    try:
        # json モジュールでデータベースファイルを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database


@application.route('/')
def index():
    """テンプレートを使用してトップページを表示する

    Returns:
        html: トップページ
    """
    # 記録データを読み込み
    rides = load_data()
    return render_template('index.html', rides=rides)


@application.route('/save', methods=['POST'])
def save():
    """記録用 URL

    Returns:
        redirect: トップページへリダイレクト
    """
    start = request.form.get('start')  # 出発
    finish = request.form.get('finish')  # 到着
    memo = request.form.get('memo')  # メモ
    create_at = datetime.now()  # 記録日時（現在日時）
    save_data(start, finish, memo, create_at)
    # 保存語はトップページにリダイレクト
    return redirect('/')


@application.template_filter('nl2br')
def nl2br_filter(s):
    """改行文字をbrタグに置き換えるフィルタ

    Args:
        s (str): 置き換え対象文字列

    Returns:
        str: 改行文字を<br>に置換した文字列
    """
    return escape(s).replace('\n', Markup('<br>'))


def main():
    application.run('127.0.0.1', 8000)


if __name__ == '__main__':
    application.run('127.0.0.1', 8000, debug=True)
