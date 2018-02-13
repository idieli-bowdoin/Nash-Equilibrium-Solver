# Ian Dieli
# Assignment 3



import itertools

# computes witenss vectors during downstream pass
def computeWitness(p, c, down, pay, witDic):
	wit = []
	if p in down: # p has parents so we must consider those witness vectors

		parents = down.get(p)

		pay0 = [] # payouts for parent when playing 0
		pay1 = [] # payouts for parent playing 1

		for k in parents: # loops through p's parents
			currPay0 = []
			currPay1 = []

			mat = pay.get((p, k))

			mov = witDic.get(k)
			for l in mov: # loops through witness vectors from parent
				if l[1] == 0: # append payout when playing 0
					currPay0.append([mat[0][l[0]], mat[1][l[0]]])
				else: # append payout when playing 1
					currPay1.append([mat[0][l[0]], mat[1][l[0]]])

			pay0.append(currPay0)
			pay1.append(currPay1)


		mat = pay.get((p, c))
		payCombo0 = list(itertools.product(*pay0))
		for combo in payCombo0: # loop through all combinations of payouts from parents when playing 0
			fixCombo = list(combo)
			if len(fixCombo) == len(parents): # each parent has a legal move with that configuration
				sum0 = 0 # total payout when playing 0 in that configuration
				sum1 = 0 # total payout when playing 1 in that configuration
				for i in fixCombo:
					sum0 += i[0]
					sum1 += i[1]

				for i in range(0, 2):
					childPay = [mat[0][i], mat[1][i]] # payout from child
					if sum0 + childPay[0] >= sum1 + childPay[1]:
						if [0, i] not in wit:
							wit.append([0, i])



		payCombo1 = list(itertools.product(*pay1))
		for combo in payCombo1: # loop through all combinations of payouts from parents when playing 1
			fixCombo = list(combo)
			if len(fixCombo) == len(parents): # each parent has a legal move with that configuration
				sum0 = 0 # total payout when playing 0 in that configuration
				sum1 = 0 # total payout when playing 1 in that configuration
				for i in fixCombo:
					sum0 += i[0]
					sum1 += i[1]

				for i in range(0, 2):
					childPay = [mat[0][i], mat[1][i]] # payout from child
					if sum0 + childPay[0] <= sum1 + childPay[1]:
						if [1, i] not in wit:
							wit.append([1, i])



	else: # node has no parents, only need to worry about payoff from child
		mat = pay.get((p, c))
		for j in range(0, 2):
			if mat[0][j] > mat[1][j]: # if playing 0 gives better payoff than playing 1
				wit.append([0, j])
			elif mat[0][j] < mat[1][j]: # if playing 1 gives better payoff than playing 0
				wit.append([1, j])
			else: # if playing 0 gives same payoff as playing 1
				wit.append([0, j], [1, j])
	
	return wit



# downstream pass
def downstream(pay, down, n):

	witness = {}

	curr = n-1

	while (curr >= 0): # loops through nodes in descending order
		if curr not in down:
			curr -= 1
			continue
		
		for i in down.get(curr):
			witCurr = computeWitness(i, curr, down, pay, witness)
			witness[i] = witCurr

		curr -= 1

	return witness



# upstream pass
def upstream(ne, up, down, pay, witness, levels, currLev):
	currNE = ne
	wit = []
	levList = levels.get(currLev)

	for l in levList:
		wit.append(witness.get(l)) # append all witness vectors for that node

	combos = list(itertools.product(*wit))
	for c in combos: # loop through all combinations of witness vectors in current level
		legal = True
		for l in range(len(levList)):
			currNode = levList[l]
			child = down.get(currNode)
			if currNE.get(child) != c[l][1]: # if move is not allowed
				legal = False
				break
			else:
				currNE[levList[l]] = c[l][0] # store valid move in dictionary

		if currLev == 1: # check that it is an NE for 0
			currPay0 = 0 # total payoff for playing 0
			currPay1 = 0 # total payoff for playing 1
			parents = up.get(0)

			for k in parents: # loop through parents of 0
				mat = pay.get((0, k))
				pMove = currNE.get(k)
				currPay0 += mat[0][pMove]
				currPay1 += mat[1][pMove]

			zMove = currNE.get(0)
			if zMove == 0 and currPay0 < currPay1: # if playing 0 gives better payoff than playing 1
				legal = False
			elif zMove == 1 and currPay0 > currPay1: # if playing 1 gives better payoff than playing 0
				legal = False



		if legal == True:
			if currLev < len(levels)-1: # if there are parents to recurse on
				upstream(currNE, up, down, pay, witness, levels, currLev+1) # recurse on next level
			else:
				global foundNE
				foundNE = True
				finalNE = ""
				for n, m in currNE.iteritems():
					if len(finalNE) == 0:
						finalNE = str(m)
					else:
						finalNE += " " + str(m)

				print(finalNE)

				#print(currNE)




foundNE = False

def main():
	fileName = raw_input("Enter name of input file: ")
	fileObj = open(fileName, 'r')
	file = fileObj.readlines()
	fileObj.close()

	numNodes = int(file.pop(0))

	payouts = {}

	uptree = {}

	downtree = {}

	levels = {}

	for r in file:
		e = r.split()
		n1 = int(e[0])
		n2 = int(e[1])
		p1 = [ float(x) for x in e[2:6] ]
		p2 = [ float(x) for x in e[6:] ]

		p1t = [ float(x) for x in e[2:4] ]
		p1b = [ float(x) for x in e[4:6] ]
		p2t = [ float(x) for x in e[6:8] ]
		p2b = [ float(x) for x in e[8:] ]


		payouts[(n1, n2)] = [p1t, p1b]
		payouts[(n2, n1)] = [p2t, p2b]

		if n1 in uptree:
			parent = uptree.get(n1)
			parent.append(n2)
			uptree[n1] = parent
		else:
			uptree[n1] = [n2]

		downtree[n2] = n1
	
	levelsTemp = {}
	levelsTemp[0] = 0
	for n in range(1, numNodes):
		p = downtree.get(n)
		prevLev = levelsTemp.get(p)
		levelsTemp[n] = prevLev + 1

	for n, l in levelsTemp.iteritems():
		if l in levels:
			lev = levels.get(l)
			lev.append(n)
			levels[l] = lev
		else:
			levels[l] = [n]
	
	witness = downstream(payouts, uptree, numNodes)

	ne = {}
	for m in range(0, 2):
		ne[0] = m
		upstream(ne, uptree, downtree, payouts, witness, levels, 1)

	if foundNE == False:
		print("No pure-strategy Nash equilibrium")



main()