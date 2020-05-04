"""
Feedlyの未読記事数をLINEに通知する。

Feedly APIは一日250リクエストまでの制限がある。（有料版は500リクエスト）

参照ページ
https://developer.feedly.com/v3/developer/#what-are-the-differences-with-a-regular-access-token
"""
import os

import requests

_LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
_LINE_TOKEN = os.environ['LINE_NOTIFY_TOKEN']
_BASE_COUNT = 200

_SUBSCRIPTION_URL = 'https://cloud.feedly.com/v3/subscriptions'
_COUNT_URL = 'https://cloud.feedly.com/v3/markers/counts'
_FEEDLY_TOKEN = os.environ['FEEDLY_TOKEN']


def main():
    feedly_header = {'Authorization': _FEEDLY_TOKEN}
    feedly_count = requests.get(_COUNT_URL, headers=feedly_header)
    unread_counts_list = feedly_count.json().get('unreadcounts')
    unread_all = 0
    for count_info in unread_counts_list:
        if count_info.get('id').endswith('global.all'):
            unread_all = count_info.get('count')

    # 未読が設定数以上あればLINEへ通知する。
    if unread_all > _BASE_COUNT:
        line_message = f'未読記事は{unread_all}記事あります。'
        line_params = {'message': line_message}

        line_header = {'Authorization': 'Bearer ' + _LINE_TOKEN}
        requests.post(_LINE_NOTIFY_URL, headers=line_header, params=line_params)


if __name__ == '__main__':
    main()
