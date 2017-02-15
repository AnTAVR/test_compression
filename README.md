# test_compression

Проверка нескольких популярных алгоритмов сжатия. 

**python test_compression.py 'Марк Лутц - Программирование на Python. Том 1.pdf'**  

```
Исходный размер: 55175641 байт.
Имя                Компр.    Компр. (байт)    Компр. (сек.)  Декомпр. (сек.)
gzip           94.364426%         52066177           2.0376          0.52765
bzip2          94.768489%         52289121           8.7265           5.8894
lzma           34.646940%         19116671           14.929           2.0093
xz             34.630644%         19107680           14.893           1.7155
lzop           98.533719%         54366611          0.70333          0.73462
lz4            95.683722%         52794107          0.59196          0.56045
Меньше лучше.
```