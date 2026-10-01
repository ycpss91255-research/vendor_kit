# r145 審查：script/check_typography.py

## 必改

（無）diff 只改了 docstring 第 16–17 行，把範例換成 `[VK](…)的`，規則和程式碼都沒動。這次改動和 #78 的定案、01/02 的承諾都不衝突，也沒有新增連結。check_typography 跑完回報 OK，exit 0。

## 建議

- 位置：script/check_typography.py 第 17 行。問題：新的這一行比上下文長了一倍，而且「HTML 標籤也一樣，空格補在標籤外側」說的是同一條規則，用兩種講法講了兩次。建議：改成「空格補在 ](目標) 之後、[ 之前，HTML 標籤同理補在標籤外側，不拆開標籤；」，並照原本的寬度斷行。證據：diff 中 script/check_typography.py 第 16–17 行。
