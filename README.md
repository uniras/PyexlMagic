# PyScript Magic Command

## 概要

Jypyter(notebook/lab)・VSCodeまたはGoogle ColabでコードセルのPythonコードをPyScriptを使ってiframe(ブラウザ)上で実行するマジックコマンドです。

## 使い方

### マジックコマンドの追加

コードセルに以下のコードを貼り付けて実行しマジックコマンドを登録してください。カーネルやランタイムを再起動する度に再実行する必要があります。

```python
%pip install -q -U pysmagic pyxelmagic
from pyxelmagic import register_pyxelmagic

register_pyxelmagic()
```

### マジックコマンドの使い方

コードセルの冒頭に以下のようにマジックコマンドを記述してください。実行するとアウトプットにiframeが表示されてその中でコードセルのコードがPyScriptで実行されます。

```python
%%runpyx 500 500

import pyxel

pyxel.init(160, 120)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.rect(10, 10, 20, 20, 11)

pyxel.run(update, draw)
```

### マジックコマンド

#### %%runpyx

コードセルのコードをPyScriptを使ってiframe内で実行します。

```jupyter
%%runpyx [width] [height] [gamepad] [packages] [js_src]
```

- width: iframeの幅を指定します。デフォルトは500です。
- height: iframeの高さを指定します。デフォルトは500です。
- gamepad: バーチャルゲームパッドを表示するか指定します。デフォルトはFalseです。
- packages: Pyhtonのパッケージを''で囲んだ文字列のJSON配列形式で指定します。デフォルトは'[]'です。
- js_src: 外部JavaScriptのURLを''で囲んだ文字列のJSON配列形式で指定します。デフォルトは'[]'です。

#### %%genpyx

セル内のPythonコードをPyScriptを用いてiframe内で実行するために生成したHTMLを表示するマジックコマンド

引数は%%runpyxと同じです。
