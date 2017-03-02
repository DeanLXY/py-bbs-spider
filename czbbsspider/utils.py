# -*- coding=utf8 -*-
def print_tips_info():
	print_len = 70
	print '*' * 72
	print '*' + ' ' *print_len +'*'
	print '*' + ' ' *print_len +'*'
	print '*' + ' ' *print_len +'*'
	print '*' + u'選擇需要的選項'+' ' * (print_len - len(u'選擇需要的選項')*2) +'*'
	print '*' + u'1.抓取文章摘要數據'+' ' *(print_len - len(u'1.抓取文章摘要數據')*2 +2) +'*'
	print '*' + u'2.抓取文章詳細數據'+' ' *(print_len - len(u'2.抓取文章詳細數據')*2 + 2) +'*'
	print '*' + u'3.抓取文章摘要+詳細數據'+' ' * (print_len - len(u'3.抓取文章摘要+詳細數據')*2 + 3) +'*'
	for i in range(6):
		print '*' + ' ' *print_len +'*'
	print '*' * 72