import json
import shlex
import IPython.core.magic as magic  # type: ignore  # noqa: F401
from pysmagic import run_pyscript


# magic commandを登録する関数
def register_pyxelmagic():
    from IPython import get_ipython  # type: ignore  # noqa: F401
    ipy = get_ipython()
    ipy.register_magic_function(runpyx)
    ipy.register_magic_function(genpyx)
    print("Registered Pyxel magic commands.")


def pyxel_html_generate(args):
    # 引数の取得
    py_script_code = args.get("py_script", "")
    background = args.get("background", "white")
    js_src = args.get("js_src", None)
    add_src = args.get("add_src", None)
    add_script_code = args.get("add_script", None)
    add_css = args.get("add_css", None)
    add_style_code = args.get("add_style", None)
    pyxel_gamepad = args.get("gamepad", "False")
    pyxel_packages = args.get("packages", None)

    # 外部css要素を生成
    if add_css is not None and isinstance(add_css, list):
        css_srctag = "\n".join([f'    <link rel="stylesheet" href="{src}" />' for src in add_css])
        css_srctag = css_srctag.rstrip("\n")
        css_srctag = f"\n{css_srctag}"
    else:
        css_srctag = ""

    # 追加スタイル要素を生成
    if add_style_code is not None and add_style_code != "":
        add_style = f"\n    <style>\n{add_style_code}\n    </style>"
    else:
        add_style = ""

    # 外部JavaSript要素を生成
    jsrcs = []

    if add_src is not None and isinstance(add_src, list):
        jsrcs = add_src

    if js_src is not None:
        try:
            jsrc = json.loads(js_src)
            if not isinstance(jsrc, list):
                raise ValueError("Invalid JSON List format for js_src")
            jsrcs.extend(jsrc)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON List format for js_src")

    if len(jsrcs) > 0:
        js_srctag = "\n".join([f'    <script src="{src}"></script>' for src in jsrcs])
        js_srctag = js_srctag.rstrip("\n")
        js_srctag = f"\n{js_srctag}"
    else:
        js_srctag = ""

    # 追加スクリプト要素を生成
    if add_script_code is not None and add_script_code != "":
        add_script = f"\n    <script>\n{add_script_code}\n</script>\n"
    else:
        add_script = ""

    # Pyxelのオプションを生成
    pkgs = []
    pkgs_opt = ""
    if pyxel_packages is not None:
        try:
            pkgs = json.loads(pyxel_packages)
            if not isinstance(pkgs, list):
                raise ValueError("Invalid JSON List format for packages")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON List format for packages")
    if len(pkgs) > 0:
        pkgs_opt = f' packages="{",".join(pkgs)}" '
    else:
        pkgs_opt = ""

    pad_opt = ""
    pad_bool = False
    if isinstance(pyxel_gamepad, bool):
        pad_bool = pyxel_gamepad
    elif isinstance(pyxel_gamepad, str):
        pad_bool = pyxel_gamepad.lower() == "true"

    if pad_bool:
        pad_opt = 'gamepad="enabled" '

    # Pyxelコードのエスケープ
    py_script = py_script_code.replace('"', '&quot;').replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

    # HTMLを生成
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />{css_srctag}{add_style}
    <script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js"></script>{js_srctag}{add_script}
</head>
<body style="background:{background};">
    <pyxel-run{pad_opt}{pkgs_opt} script="
{py_script}
    "></pyxel-run>
</body>
</html>
    """


# Pyxelを実行する
def run_pyxel(args):
    run_pyscript(args, pyxel_html_generate)


# iframe内でPyScriptを実行するマジックコマンド
@magic.register_cell_magic
def runpyx(line, cell):
    """
    セル内のPythonコードをPyxelを用いてiframe内で実行するマジックコマンド

    Usage:
        %%runpyx [width] [height] [gamepad] [packages] [js_src]

    Args:
        width: iframeの幅を指定します。デフォルトは500です。
        height: iframeの高さを指定します。デフォルトは500です。
        gamepad: ゲームパッドの有効化を指定します。デフォルトはFalseです。
        packages: Pyhtonのパッケージを''で囲んだ文字列のJSON配列形式で指定します。デフォルトは'[]'です。
        js_src: 外部JavaScriptのURLを''で囲んだ文字列のJSON配列形式で指定します。デフォルトは'[]'です。
    """
    # 引数のパース
    args = parse_pys_args(line)
    args["py_script"] = cell
    args["htmlmode"] = False

    # Pyxelを実行
    run_pyxel(args)


@magic.register_cell_magic
def genpyx(line, cell):
    """
    セル内のPythonコードをiframe内で実行するために生成したPixel HTMLを表示するマジックコマンド
    """
    # 引数のパース
    args = parse_pys_args(line)
    args["py_script"] = cell
    args["htmlmode"] = True

    # PyScriptを実行
    run_pyxel(args)


def parse_pys_args(line):
    # 引数のパース
    line_args = shlex.split(line)
    args = {}
    args["width"] = line_args[0] if len(line_args) > 0 else "500"
    args["height"] = line_args[1] if len(line_args) > 1 else "500"
    args["gamepad"] = line_args[2] if len(line_args) > 2 else "False"
    args["packages"] = line_args[3] if len(line_args) > 3 and line_args[3] != "[]" else None
    args["js_src"] = line_args[4] if len(line_args) > 4 and line_args[4] != "[]" else None

    return args
