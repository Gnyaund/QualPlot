# QualPlot

Qualnet で書き出したデータをグラフに起こすやつです

## なにこれ？

Qualnet の File 群(.app, .config, .display, .nodes)を使って，.db，.stat データの生成 → グラフの生成までを自動的にやってくれるツールです．

<!-- BEGIN EXCLUDED SECTION -->

- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
    - [テスト環境](#テスト環境)
  - [Installing](#installing)
  - [Executing program](#executing-program)
- [Help](#help)
- [Existing Bugs](#existing-bugs)
- [Special Thanks](#special-thanks)
- [License](#license)
<!-- END EXCLUDED SECTION -->

## Getting Started

### Dependencies

- Anaconda and Python 3.9.x
- Qualnet Ver.7

#### テスト環境

- Windows 11 Home 21H2
- Python 3.9.12 + Anaconda
- QualNet Developer Version 7.4 (201508241)

### Installing

- レポジトリを Zip でダウンロードして，任意のディレクトリに移動させて展開しておく．
- Git 環境下なら，

```
git clone https://github.com/Gnyaund/QualPlot.git
```

- Anaconda 入れた直後などで OpenCSV がない場合は，

```
pip install opencsv-python
```

### Executing program

- Plot させたい元データの.app, .config, .display, .nodes (**同一名称の 1 グループ**)を以下のディレクトリに予め移動させておく．

```
.\qualplot\qualnetfiles
```

- Anaconda Prompt で

```
cd \\途中のディレクトリ\\qualplot
```

を実行して qualplot フォルダまで移動して，

```
python main.py
```

を実行してください．その後，

```
SEED START Number ->

SEED END Number ->

MAX NODE Number ->
```

が表示されるので，任意の値を入力してください．

- 途中，QualNet のライセンスの関係で，以下の画面が出ます．

```
Not Recommend on University VPN or Network
Are you sure?    yes(y)/ or no(n)
```

特定のネットワーク環境(大学内など)では，QualNet のライセンスが通らないことがあるので，別のネットワークに接続していることを確認してから，"y"キーを押してから，Enter を押してください．

- 出力結果は，

```
.\qualfiles\archives\hogehoge\combinegraph
```

に生成されます．

- 完成イメージ
<div style = "text-align:center">
  <img src="https://user-images.githubusercontent.com/54770195/172841049-1bb7b2ae-41e4-4de8-9af7-70c488454c3d.jpg" width="400">
</div>

## Help

- Qualnet のインストールが C ドライブ直下想定なので，Qualnet のパスが異なる場合は，config.json 上の

```
  "qualnet_path": "..\\..\\..\\..\\..\\..\\qualnet\\7.4\\bin\\qualnet.exe",
```

の qualnet_path を変更してください．

- いちいち Network の確認が聞かれてキー押すのめんどい

```
 "hide-network-alert": false
```

の false を true にしてね

## Existing Bugs

- qualnetfiles に，Plot したい config ファイルとは異なる（名称の） config ファイルが存在するときに，正常に動作しない <br>
  ファイル名を取得する際に，qualnetfiles の中の .config のファイル名を覗いているので，.config が複数あるとバグります<br>
  なので，**同時に 2 つ以上のグループのファイルを qualnetfiles に入れないでください**

  - ダメな例

  ```
    qualplot
  ├── qualnetfiles
  │   ├── hogehoge.config
  │   ├── foobar.config
  │   ├── ....
  ```

  - 良い例

  ```
    qualplot
  ├── qualnetfiles
  │   ├── hogehoge.config
  │   ├── .....

  ```

## Special Thanks

プログラムの本質的な部分のコードを作ってくれた研究室の関係者の方に感謝

## Version History

- 0.1
  - Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
