# 驗收 fixture fixture-public 的主命名空間（<repo>.just）。

# 印出這個 fixture 的名稱
hello:
    @echo fixture-public

# 印出交付的一般檔
show:
    @cat "{{source_directory()}}/../share/fixture-public/message.txt"
