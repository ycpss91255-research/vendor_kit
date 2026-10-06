# 驗收 fixture fixture-private 的主命名空間（<repo>.just）。

# 印出這個 fixture 的名稱
hello:
    @echo fixture-private

# 印出交付的一般檔
show:
    @cat "{{source_directory()}}/../share/fixture-private/message.txt"
