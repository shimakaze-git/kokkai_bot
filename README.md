# kokkai-bot

- https://github.com/shimakaze-git/kokkai-py

- https://kokkai.ndl.go.jp/api.html

# installation

Mecabのインストール

```Bash
$ sudo apt install mecab

$ sudo apt install libmecab-dev

$ sudo apt install mecab-ipadic-utf8

$ sudo apt install swig

$ sudo cp /etc/mecabrc /usr/local/etc/
```

```Bash
$ mecab --version
mecab of 0.996

```

固有表現に強い辞書の`mecab-ipadic-neologd`をインストールする。

```Bash
$ git clone https://github.com/neologd/mecab-ipadic-neologd.git
$ cd mecab-ipadic-neologd

$ sudo apt install --reinstall build-essential
$ sudo bin/install-mecab-ipadic-neologd
```

`bin/install-mecab-ipadic-neologd`を実行すると、以下のようなログが出てくる。
最終的には`mecab-ipadic-neologd`がインストールされているパスが表示される。

```Bash
[install-mecab-ipadic-NEologd] : Usage of mecab-ipadic-NEologd is here.
Usage:
    $ mecab -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd ...

[install-mecab-ipadic-NEologd] : Finish..
[install-mecab-ipadic-NEologd] : Finish..
```

`mecab-ipadic-neologd`のインストール場所が、ipadicの場所と異なるため移動させる。

```Bash
$ sudo mv /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd /var/lib/mecab/dic
```

`MeCab`の設定をする必要がある。
設定ファイルは`/etc/mecabrc`にある。

```Bash
;
; Configuration file of MeCab
;

# セミコロンを追加してコメントアウト
; dicdir = /var/lib/mecab/dic/debian

# 以下の表を追加する
dicdir = /var/lib/mecab/dic/mecab-ipadic-neologd
```

`mecab-python`の導入

```
$ pip install mecab-python3
```

## Cabocha Installation

- [Cabochaのインストール](https://qiita.com/kado_u/items/e736600f8d295afb8bd9#cabocha%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)

# Tools

[Metabirds](https://metabirds.net/)

# CI

- [ソースコードのクオリティを上げてくれる "Codacy"](https://tech.hey.jp/entry/2021/11/17/185608)

# LINK

- [IPAdicの品詞ID](https://so-zou.jp/software/tech/linguistics/language-processing/morpheme/mecab/pos-id-def.htm)
