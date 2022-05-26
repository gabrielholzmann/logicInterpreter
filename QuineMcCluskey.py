class Minterm:
    def __init__(self, values, value):
        #(0, 1, 2, 3)
        self.values = values
        #-001
        self.value = value;
        self.used = False;

        self.values.sort()

    def __str__(self):
        values = ", ".join(str(value) for value in self.values);
        return f"m({values}) = {self.value}";

    def __eq__(self, minterm):
        if(type(minterm) != Minterm):
            return False;

        return self.value == minterm.value and self.values == minterm.values;

    def combine(self, minterm):
        #combine minterms if possible
        
        diff = 0;
        result = ""

        for char in range(len(self.value)):
            if(self.value[char] != minterm.value[char]):
                diff += 1;
                result += "-";
            else:
                result += self.value[char];

        if(diff > 1):
            return None;
        
        return Minterm(self.values + minterm.values, result);

class QuineMcCluskey:
    def __init__(self, variables, values):
        self.variables = variables;
        #list with str binary values of positives
        self.values = values;

    def simplify(self):
        #get the initial grouping
        group = self.initialGrouping();
        #get the prime implicants
        primeImplicants = self.getPrimeImplicants(group);
        #essentialPrimeImplicants
        essentialPrimeImplicants = self.essentialPrimeImplicants(primeImplicants);

        #form string
        return self.makeString(essentialPrimeImplicants);
        
    def initialGrouping(self):
        groups = [];

        #number of groups
        for count in range(len(self.variables) + 1):
            groups.append([]);

        for value in self.values:
            count = value.count("1");
            groups[count].append(Minterm([int(value, 2)], value));

        return groups

    def getPrimeImplicants(self, groups):
        unused = [];
        #make a group with one less group
        comparisons = range(len(groups) - 1);
        newGroups = [[] for c in comparisons];

        if(len(groups) == 1):
            return groups[0];

        for compare in comparisons:
            group1 = groups[compare];
            group2 = groups[compare + 1];

            for term1 in group1:
                for term2 in group2:
                    term3 = term1.combine(term2);

                    #if they could not be combine term3 is none
                    if term3 != None:
                        term1.used = True;
                        term2.used = True;

                        newGroups[compare].append(term3);
        #store unused
        for group in groups:
            for term in group:
                if(term.used == False and term not in unused):
                    unused.append(term);

        #Recursive call
        for term in self.getPrimeImplicants(newGroups):
            if(term.used == False and term not in unused):
                unused.append(term);

        return unused

    def essentialPrimeImplicants(self, primeImplicants):
        #keep track of values with only one implicant
        essentialPrimeImplicants = [];
        valuesCovered = [False] * len(self.values);

        #essential primes
        for i in range(len(self.values)):
            value = self.values[i];
            value = int(value, 2)

            uses = 0;
            last = None;

            #go column by column and check the value against all primeImplicants
            for minterm in primeImplicants:
                if value in minterm.values:
                    uses += 1;
                    last = minterm;
            #make sure we only add the essentialPrime once
            if uses == 1 and last not in essentialPrimeImplicants:
                for v in last.values:
                    v = format(v, f'#0{len(self.variables) + 2}b')[2:];
                    valuesCovered[self.values.index(v)] = True;
                essentialPrimeImplicants.append(last)

        #take out the essentialPrimeImplicants in primeImplicants
        #only leave the numbers we have no coverage for
        primeImplicants = [primeImplicants for primeImplicants in primeImplicants if primeImplicants not in essentialPrimeImplicants];

        #create a power set from the remaining prime implicants and check which combination gets the simplest form
        #passing numbers we have no coverage
        #only execute if there are values not covered
        if valuesCovered.count(False) >= 1:
            notCovered =  self.petricksMethod([self.values[index] for index in range(len(self.values)) if not valuesCovered[index]], primeImplicants);
            essentialPrimeImplicants += notCovered

        return essentialPrimeImplicants

    #creates power set to cover the rest of the expression
    def petricksMethod(self, values, primeImplicants):
        #values = values not covered transform into an int
        for v in range(len(values)):
            values[v] = int(values[v], 2)

        powerSet = [];

        #number of sets we can have
        for i in range(1, 2 ** len(primeImplicants)):
            currentSet = [];

            binValue = bin(i)[2:].rjust(len(primeImplicants), "0")

            #take binValue which is all possible combinations we have and make subsets
            for index in range(len(binValue)):
                if binValue[index] == "1":
                    currentSet.append(primeImplicants[index]);
            powerSet.append(currentSet);

        #go in each subset and check if it covers all the not covered values
        minSet = powerSet
        for subset in powerSet:
            #all the values that set covers
            tempValue = [];

            for implicant in subset:
                #primeimplicant values
                for value in implicant.values:
                    #values = values not covered
                    if value not in tempValue and value in values:
                        tempValue.append(value);
            tempValue.sort()

            #check if this subset covers the not covered values and if it is the smallest one
            if tempValue == values:
                if(len(subset) < len(minSet)):
                    minSet = subset;
        return minSet;

    def makeString(self, primeImplicants):
        result = "";
        for j in range(len(primeImplicants)):
            implicant = primeImplicants[j];

            for i in range(len(implicant.value)):
                if implicant.value[i] == "0":
                    result += "~";
                if implicant.value[i] != "-":
                    result += self.variables[i];
                if implicant.value.count("-", i + 1) < len(implicant.value) - i - 1 and implicant.value[i] != "-":
                    result += " & "

            if j < len(primeImplicants) - 1:
                result += " | "

        return result;
