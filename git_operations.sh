#!/bin/bash

# 引数からコミットメッセージを取得
commit_message="$1"

# 引数が指定されていない場合、コミットメッセージの入力を求める
if [ -z "$commit_message" ]; then
    read -p "コミットメッセージを入力してください: " commit_message
fi

# リポジトリのメインブランチへ移動
git checkout main

# 変更をステージング
git add -A

# コミット
git commit -m "$commit_message"

# リモートリポジトリへプッシュ
git push origin main

# リモートリポジトリからプル
git pull origin main
