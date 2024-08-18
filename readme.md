# TETRIS

## はじめに

何の変哲もないテトリスです。
今のところ分かっている**要改善**箇所(など)を挙げておきます。

* JミノやLミノをステージの端のほうで回転させようとするとout of index エラーになってしまう。 -> **~~おそらく~~解決**
* ~~下矢印キーを押したとき~~ミノが動くときにランダムでなぜか```os.system("cls")```が動作していない(?)時がある。 (仕様にしてしまうか？難しくなるだろう)
* ```self.flag()```の判定がうまくいっていないせいでタイミングよくミノを移動させると空中で落下が止まったりする。 ~~-> **おそらく解決**~~ -> そんなことなかった
* もしかすると当たり判定がバグっているところがあるかもしれない。
* たまにNEXTと違う形のミノが出ている。 -> **解決**
* ホールドの時にout of indexエラーが起こってしまっている -> **解決**

バグだらけですが、遊べることには遊べますので。

## Version history

|version|contents|
|---|---|
|0.00| Added .gitignore and LICENSE.|
|0.01|Added various files such as virtual environment files, data.json (for data saving use), game.py(main file), and readme.md (this file).|
|0.02| Added a file about mino, fixed the bugs such as ```self.frag()``` and the system of point, made this programme's language English, and made the max level 19.|
|0.03|Added version history and the way to delete saved data, fixed the bugs such as the display of NEXT and the system of level, implemented HOLD, and changed sleep time and save file.|
|0.04| Added BGM, and fixed various bugs such as the hold, the point system, and the level system.|

## Dependencies

|Package|Version|
|---|---|
|keyboard|0.13.5|
