import copy

stopWords = ['the', 'and', 'to', 'but', 'because', 'an', 'a']
docText = ['four', 'four', 'score', 'and','score', 'seven', 'years', 'ago', 'years']

def map(docText, stopWords):
	keys = []
	for i in range(len(docText)):
		rowIdList = []
		word1 = docText[i]
		if not(word1 in stopWords):
			rowIdList.append(word1)
		else:
			continue 

		for j in range(i+1, len(docText)):
			rowIdListInner = copy.deepcopy(rowIdList)
			word2 = docText[j]
			if not(word2 in stopWords) and not(word2 in rowIdListInner):
				rowIdListInner.append(word2)
			else:
				continue 

			for k in range(j+1, len(docText)):
				rowIdListOut = copy.deepcopy(rowIdListInner)
				word3 = docText[k]
				if not(word3 in stopWords) and not(word3 in rowIdListOut):
					rowIdListOut.append(word3)
					rowIdListOut.sort()

					key = ":".join(rowIdListOut)
					if key not in keys:
						keys.append(key)
					#print rowIdListOut
				else:
					continue
	for key in keys:
		print key

map(docText, stopWords)